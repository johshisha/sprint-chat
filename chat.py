# -*- coding: utf-8 -*-

import os
import logging
import redis
import gevent
import json
from flask import Flask, render_template
from flask_sockets import Sockets
import bot
from xml.sax.saxutils import *
from password import password
import re

r = redis.StrictRedis(host=password.redis['host'], port=password.redis['port'], db=1)
#REDIS_URL = password.redis['url'] #os.environ['REDIS_URL']
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
#redis = redis.from_url(REDIS_URL)



class ChatBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = list()
        self.pubsub = r.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            print(data)
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)

chats = ChatBackend()
chats.start()
b = bot.Bot()

connected = []

pattern = re.compile(r'(^bot )|(^@bot )|(^bot:)')

@app.route('/')
def hello():
    return render_template('index.html')

@sockets.route('/submit')
def chat(ws):
    chats.register(ws)

    while not ws.closed:
        gevent.sleep(0.1)
        message = ws.receive()
        print message

        if not message:
            continue

        text_tmp = ''
        test_flag = 0

        if message and "{\"text\":" in message:
            message = json.loads(message)['text']
            # test mode
            test_flag = 1
            test_type = 'message'
            text_tmp = '''{
              "success": true,
              "type": "%s",
              "text": "%s"
            }'''

        if '<script' in message:
            message = escape(message)

        if message:
            #app.logger.info(u'Inserting message: {}'.format(message))

            r.publish(REDIS_CHAN, text_tmp%(test_type, message) if test_flag else json.dumps({"data":message}))


            if pattern.match(message):
                test_type = 'bot'
                res = False
                message = pattern.sub('', message)
                messages = message.split(' ',1)
                print (messages)
                command, data = messages[0],messages[-1]
                print ('command',command, 'data', data)

                alias = r.get(command)
                if alias:
                    try:
                        command,temp = alias.split(' ',1)
                        data = temp + ' ' + data
                    except:
                        command = alias

                if command == 'ping':
                    res = b.ping()
                elif command == 'todo':
                    res = b.todo(data)
                elif command == 'cook':
                    res = b.cook(data)
                elif command == '-h' or command == '--help' or command == 'help':
                    help = open('readme.txt','r').read()
                    help = help.replace('\n','<br>')
                    res = help.replace(' ', '&nbsp;')
                    #print res
                elif command == 'alias':
                    res = b.todo(data,1)

                if type(res) == list:
                    # print 'cook list'
                    for text in res:
                        #print text
                        r.publish(REDIS_CHAN, text_tmp%(test_type, text) if test_flag else json.dumps({"data":text}))

                elif res:
                    r.publish(REDIS_CHAN, text_tmp%(test_type, res) if test_flag else json.dumps({"data":res}))
