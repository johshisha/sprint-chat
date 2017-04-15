#coding:utf-8
import redis,os,re
from password import password

class Todo():
    def __init__(self, flag=0):
        self.r = redis.StrictRedis(host=password.redis['host'], port=password.redis['port'], db=flag)
        if flag == 0:
            self.command = 'todo'
        else:
            self.command = 'alias'



    def add(self, data):
        try:
            if self.command == 'todo':
                name, content = data.split(' ',1)
            else:
                name, content = map(lambda x: x.replace("'",""),re.findall(ur"'.*?'",data))
                print name, content
            flag = self.r.set(name, content)

            if flag:
                return '%s added'%self.command

            return False
        except:
            print 'adding error'

    def delete(self, name):
        if name == '-all':
            flag = self.r.flushdb()
        else:
            flag = self.r.delete(name)

        if flag:
            return '%s deleted'%self.command

        return False

    def todo_list(self):
        r = self.r
        if r.keys() == []:
            str = '%s empty'%self.command
            print 'empty'
        else:
            str = ''
            print 'not empty'

        for key in r.keys():
            str+=key+' '
            str+=r.get(key)
            str+='\n'


        return str.rsplit('\n',1)[0]

