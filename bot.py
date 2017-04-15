#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,Todo
import redis,os,json
import cook
from password import password

#REDIS_URL = password.redis['url']  #os.environ['REDIS_URL']
REDIS_CHAN = 'chat'
#redis = redis.from_url(REDIS_URL)
r = redis.StrictRedis(host=password.redis['host'], port=password.redis['port'], db=1)


class Bot():
    def __init__(self):
        self.c_todo = Todo.Todo()
        self.c_alias = Todo.Todo(1)
        self.c_cook = cook.Cook()

    def ping(self):
        return 'pong'

    """
    def generate_hash(self):
        cmd = self.conv_ascii(self.command)
        data = self.conv_ascii(self.data)
        self.hash = hex(cmd+data).replace('0x','')
        return self.hash

    def conv_ascii(self, chr):
        ascii = ''
        for s in chr:
            ord_num = ord(s)
            ascii += (str(ord_num))
        scientific = str(self.scientificNotation(int(ascii)))
        hash = scientific.split('.')[-1].replace('e+','')
        return int(hash)

    def scientificNotation(self, num):
        data = "%.16e" % num
        result = data if (int(data.split("e+")[1]) > 20) else num
        return result
    """

    def todo(self, data,flag=0):
        print 'todo:',data
        try:
            command, text = data.split(' ', 1)
        except:
            command = data
            text = ''

        if flag == 0:
            c_todo = self.c_todo
        else:
            c_todo = self.c_alias
        if command == 'add':
            text = c_todo.add(text)
        elif command == 'delete':
            text = c_todo.delete(text)
        elif command == 'list':
            print 'todo list in'
            text = c_todo.todo_list()
        else:
            print 'false:',command,text
            return False

        return text

    def cook(self,data):
        print 'cook',data
        try:
            command, text = data.split(' ', 1)
        except:
            command = data
            text = ''

        c_cook = self.c_cook
        if command == 'set':
            ingredients = text.split(' ')
            text = c_cook.set_ingredients(ingredients)
        elif command == 'search':
            ingredients = text.split(' ')
            text = c_cook.search_query(ingredients)
        elif command == 'remain':
            r.publish(REDIS_CHAN, json.dumps({'data':'"%s"を消費できる料理を検索します．'%(data.replace('remain ',''))}))
            ingredients = text.split(' ')
            text = c_cook.search(ingredients)
        elif command == 'trends':
            r.publish(REDIS_CHAN, json.dumps({'data':'現在人気の食材を使った料理を検索します．'}))
            text = c_cook.search_trends()

        print text
        return text



if __name__ == '__main__':
    message = sys.argv[1]
    if message.startswith('bot '):
        res = False
        messages = message.split(' ',2)
        print (messages)
        command, data = messages[1],messages[-1]
        b = Bot()
        #print ('com',command, 'data', data)
        if command == 'ping':
            res = b.ping()
        elif command == 'todo':
            res = b.todo(data)
        elif command == 'cook':
            res = b.cook(data)

        print res
