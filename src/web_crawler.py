#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, sys, zlib, re, urlparse
from urlparse import urlparse
id = 0
findex = open("../data/index.txt","w")
datas = {}
status = {}
def web_content(url):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    opener = urllib2.build_opener()
    response = opener.open(request)
    html = response.read()
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    content = BeautifulSoup(html)
    [s.extract() for s in content('script')]
    [s.extract() for s in content('style')]
    original = content.get_text().split('\n')
    filtered = filter(lambda x:  not re.match(r'^\s*$', x), original)
    #get urls
    urls = []
    for item in content('a'):
        if item.has_attr('href'):
            url = item['href']
            if url.startswith('http'):
                urls.append(url)
    return urls, '\n'.join(filtered)

def web_name(url):
    s = urlparse(url)
    return s.netloc

def parse_web(url, deeps):
    global status
    if url in status:
        return web_name(url)
    status[url]=True
    if deeps==3:
        return web_name(url)
    print "parsing ",url,"......",
    global id, findex, datas
    try:
        web_root = web_name(url)
        web_urls, web_text = web_content(url)
        with open("../data/file"+str(id),"w") as fout:
            print >>fout, web_text.encode('utf-8')
    except:
        print "failed"
        return web_root
    datas[id]= {"website":url,"root":web_root,"urls":[]}
    print "ok"
    tmp_id = id
    id += 1
    web_urls = web_urls[:100]
    datas[id - 1]['urls'] = [web_name(web_url) for web_url in web_urls]
    for sub_url in web_urls:
        try:
            sub_webroot = parse_web(sub_url, deeps + 1)
        except:
            continue
        if sub_webroot is None:
            continue
    return web_root

def output_index():
    for (k, v) in datas.items():
        print >>findex, k, v["website"], v['root'],
        for v1 in v['urls']:
            try:
                print >>findex, v1.encode('utf-8'),
            except:
                print "ERROR"
        print >>findex


if __name__=="__main__":
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    #urls, content = web_content("http://www.sina.com.cn")
    with open("seed1") as fin:
        seeds = [l.strip() for l in fin]
    for root in seeds:
        parse_web(root,0)
    #print web_name("http://news.sina.com.cn")
    output_index()
    findex.close()

