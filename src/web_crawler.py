#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import sys
def web_content(url):
    try:
        content = urllib2.urlopen(url).read()
        return BeautifulSoup(content).get_text().decode('utf-8').encode('utf-8')
    except:
        print "failed"
        return None

def web_name(url):
    return None


if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print web_content("http://www.sina.com.cn")
