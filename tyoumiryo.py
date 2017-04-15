#coding:utf-8
import sys,requests,commands,pickle,re
from bs4 import BeautifulSoup
from collections import defaultdict
from yahoo_api import NLP

urls = ["http://spice.kh23.com/flavor/archives/0010/index.html","http://spice.kh23.com/flavor/archives/0020/index.html",
        "http://spice.kh23.com/flavor/archives/0030/index.html","http://spice.kh23.com/flavor/archives/0040/index.html",
        "http://spice.kh23.com/flavor/archives/0050/index.html","http://spice.kh23.com/flavor/archives/0060/index.html",
        "http://spice.kh23.com/flavor/archives/0070/index.html","http://spice.kh23.com/flavor/archives/0080/index.html",
        "http://spice.kh23.com/flavor/archives/0090/index.html","http://spice.kh23.com/flavor/archives/0100/index.html",
        "http://spice.kh23.com/flavor/archives/0200/index.html","http://spice.kh23.com/flavor/archives/0300/index.html",
        "http://spice.kh23.com/flavor/archives/0400/index.html"]

def main():
    nlp = NLP()
    result = defaultdict(bool)
    for url in urls:
        lists = crawler(url)
        lists = nlp.hiragana(lists)
        for l in lists:
            print l
            result[l] = True


    # print result

    f = open('tyomiryo.pkl','wb')
    pickle.dump(result,f)
    f.close()


def crawler(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    lists = map(lambda x: re.sub(ur"（.*）","",x.string),soup.find_all(href=re.compile("post")))
    return lists










if __name__ == '__main__':

    main()
    # lists = crawler(urls[0])
    # for i in lists:
    #     print i
