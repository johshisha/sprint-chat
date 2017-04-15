#coding:utf-8
import sys,requests,commands
from bs4 import BeautifulSoup
import re
from yahoo_api import NLP
from IPython import embed
import gevent
from gevent import monkey
import time

class Cook():
    def __init__(self):
        self.nlp = NLP()
        self.cookpad_root_url = 'https://cookpad.com'

    def search(self, ingredients, pages=1, limit=5):

        def get_sim_title(i):
            url = i.get('href')
            title = i.string
            print url
            ingredients_list = self.search_ingredients(url)
            # print title,':',
            # for ing in ingredients_list:
            #     print ing,
            # print ""
            similarity = self.nlp.calc_similarity(ingredients, ingredients_list)
            # sim_title.append([similarity, "<a href='http://cookpad.com%s' target='_blank'>%s</a>"%(url, title)])
            return [similarity, "<a href='%s%s' target='_blank'>%s</a>"%(self.cookpad_root_url, url, title)]

        for ing in ingredients:
           print ing,
        print ''

        query = '%20'.join(ingredients)
        sim_title = []

        for page in range(pages):
            page += 1
            #print page
            html = commands.getoutput('curl -L %s/search/%s?page=%d'%(self.cookpad_root_url, query,page))
            soup = BeautifulSoup(html, "html.parser")
            res = soup.find_all('a', class_='recipe-title font13  ')

            # starttime = time.time()
            # # sync
            # for i in res:
            #     sim_title.append(get_sim_title(i))
            # endtime = time.time()
            # interval = endtime - starttime
            # print("sync: " + str(interval) + "秒")


            starttime = time.time()
            # async
            monkey.patch_all()
            jobs = [gevent.spawn(get_sim_title, i) for i in res]
            gevent.joinall(jobs)
            sim_title.extend([j.value for j in jobs])

            endtime = time.time()
            interval = endtime - starttime
            print("async: " + str(interval) + "秒")




        sorted_titiles = sorted(sim_title, reverse=True)
        # for i in sorted_titiles:
        #     print i[1],i[0]

        results = map(lambda x: x[1], sorted_titiles)

        if results == []:
            results = [u'これらの組み合わせの料理はありませんでした...']

        print results
        return results[:limit]



    def search_ingredients(self,url):
        title_class = 'recipe-title fn clearfix'
        ingredients_class = 'ingredient_name'
        quantity_class = 'ingredient_quantity amount'

        html = commands.getoutput('curl -L %s%s'%(self.cookpad_root_url, url))
        soup = BeautifulSoup(html, "html.parser")

        #title = soup.find('h1', class_=title_class).string
        ingredients = []
        for ingredient, quantitity in zip(soup.find_all('div', class_=ingredients_class),soup.find_all('div', class_=quantity_class)):
            q = quantitity.string
            if not q:
                continue
            elif u'量' in q or u'少' in q or u'さじ' in q:  #re.search(ur"(量|少|さじ)",q):
                continue
            ingredient = ingredient.find('span', class_='name')
            if not ingredient.string:
                ingredient = ingredient.find('a')

            print ingredient
            ingredients.append(ingredient.string)

        return ingredients


    def search_query(self, ingredients, limit = 5):
        #print ingredients
        query = '%20'.join(ingredients)
        html = commands.getoutput('curl -L %s/search/%s'%(self.cookpad_root_url, query))

        soup = BeautifulSoup(html, "html.parser")

        res = soup.find_all('a', class_='recipe-title font13  ')

        urls = []
        for i in res[:limit]:
            urls.append("<a href='%s' target='_blank'>%s</a>"%(i.get('href'), i.string))

        return urls

    def search_list(self, ingredients):
        query = '%20'.join(ingredients)
        html = commands.getoutput('curl -L %s/search/%s'%(self.cookpad_root_url, query))

        soup = BeautifulSoup(html, "html.parser")

        ingredient_list = soup.find_all('div', class_='material ingredients')


        results = []
        for res in ingredient_list:
            text = res.get_text()
            texts = text.split('\n')
            texts = texts[2].split(u'、')
            results.append(texts)

        return results

    def search_trends(self, limit=5):
        url = '%s/trend_keyword'%self.cookpad_root_url
        html = commands.getoutput('curl -L %s'%url)
        soup = BeautifulSoup(html, "html.parser")
        rank_and_keyword = soup.find_all('div', class_='trend_keyword_recipe_wrapper')
        trends = []
        for rank in rank_and_keyword:
            keyword = rank.find('h2', class_='keyword').find('a').string
            recipe = rank.find('a', class_='recipe_title')
            title = recipe.string
            href = recipe.get('href')
            trends.append('%s : <a href="%s/%s">%s</a>'%(keyword, self.cookpad_root_url, href, title))

        #print trends
        return trends[:limit]



if __name__ == '__main__':
    ingredients = ['玉ねぎ','人参','きゅうり']
    #print ingredients
    cook = Cook()
    res = cook.search(ingredients, pages=1)
    #res = cook.search_trends()

    for i in res:
        print i


    """
    res = cook.search_query(ingredients)
    for t in res:
        print t

    res = cook.search_list(ingredients)
    for t in res:
        for r in t:
            print r
    """