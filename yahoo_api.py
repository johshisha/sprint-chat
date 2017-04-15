#coding:utf-8
import requests,pickle
from bs4 import BeautifulSoup
from collections import defaultdict
from password import password
import gevent
from gevent import monkey
import time

class NLP:
    def __init__(self):
        self.dict = pickle.load(open('tyomiryo.pkl','rb'))

    def calc_similarity(self, query, ingredients_list):

        # starttime = time.time()
        # # sync
        # hiragana_list = self.hiragana(ingredients_list)
        # endtime = time.time()
        # interval = endtime - starttime
        # #print("sync: " + str(interval) + "秒")

        starttime = time.time()
        # sync
        hiragana_list = self.async_hiragana(ingredients_list)
        endtime = time.time()
        interval = endtime - starttime
        #print("async: " + str(interval) + "秒")


        #print 'end hiragana'
        #print 'start simil'
        simil = self.calculate(query, hiragana_list)
        #print 'end simil'
        """
        for hiragana in hiragana_list:
            print hiragana,
        print simil,
        print ''
        """

        #print 'end calc'
        return simil

    def sentence_to_hiragana(self, sentence):
        url = 'http://jlp.yahooapis.jp/MAService/V1/parse?appid=%s&results=ma,uniq&uniq_filter=%s&sentence=%s'%(password.yahoo['appid'], "9%7C10", sentence)
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')

        results = soup.find('ma_result')
        words = results.find_all('word')

        res = ''
        for text in words:
            if text.find('pos').text == u'名詞':
                res += text.find('reading').text

        return res

    def hiragana(self,sentences):
        res = []

        # sync
        for sentence in sentences:
            res.append(self.sentence_to_hiragana(sentence))

        return res

    def async_hiragana(self, sentences):
        res = []

        # async
        monkey.patch_all()
        jobs = [gevent.spawn(self.sentence_to_hiragana, sentence) for sentence in sentences]
        gevent.joinall(jobs)
        res.extend([j.value for j in jobs])

        return res

    def calculate(self, query, hiragana_list):
        simil = 0
        query = self.async_hiragana(query)
        for q in query:
            self.dict[q] = True

        for hiragana in hiragana_list:
            if self.dict[hiragana]:
                simil += 0.5
            else:
                simil -= 2.0

        return simil

if __name__ == '__main__':

    import cook
    ingredients = ['玉ねぎ','キャベツ','鶏肉']
    print '検索材料名：',
    for ing in ingredients:
        print ing,
    print ''

    c_cook = cook.Cook()
    res = c_cook.search_list(ingredients)

    #res = [u"◎鶏がらスープ"]
    nlp = NLP()
    for sentences in res:
        hiragana_list = nlp.hiragana(sentences)
        for hiragana in hiragana_list:
            print hiragana,
        print nlp.calc_similarity(ingredients, hiragana_list)
        print ''