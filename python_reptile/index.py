from django.shortcuts import render
from django.http import HttpResponse
import urllib
from urllib import request as req
from pyquery import PyQuery as pq
import time
import os
import random
from ArticleModel.models import ArticleModel
isRun = False
writeCount = 1 #写入文章的数目

def run(req):
    tagname = req.GET.get('tagname')
    begin = int(req.GET.get('begin'))
    num = int(req.GET.get('num'))
    global isRun
    if not isRun :
        isRun = True
    else:
        return print('爬虫未结束，拒绝再次访问')
    print('爬虫开始')
    links = getListPage(tagname, begin, num)
    pagelinks = []
    for item in links:
        pagelinks.extend(getListUrl(item))
    successNum = 0
    for pitem in pagelinks:
        result = getPageContent(pitem)
        if(result): successNum+= 1
    
    print('爬虫结束')
    print('列表数：'+ str(len(links)))
    print('文章数：'+ str(len(pagelinks)))
    print('成功写入：'+ str(successNum))
    isRun = False
    return HttpResponse('爬虫结束')

def read(url):
    result = {
        'status': 200,
        'html': ''
    }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UA = user_agent_list[random.randint(0, len(user_agent_list)-1)]
    try:
        _req = req.Request(url, headers={
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
        html = req.urlopen(_req).read()
        html = html.decode('gb2312', 'ignore')
        result['html'] = html
    except urllib.error.URLError as e:
        print(url)
        print(e)
        result['status'] = e
    return result

'''
获取爬取的所有链接地址

返回 [{
        'tagId': 标签id,
        'url_type': 标签类型，例如qinggan,
        'tagName': 标签名称,
        'link': 列表页链接
        }]
'''
def getListPage(tagName, start_page, end_page):
    print(tagName, start_page, end_page)
    listPages = []
    types = {
        'redu':{
            'url_type': 'redu',
            'tagName': '热读',
            'type_id': 1
        },
        'wenyuan':{
            'url_type': 'wenyuan',
            'tagName': '文苑',
            'type_id': 2
        },
        'qinggan':{
            'url_type': 'qinggan',
            'tagName': '情感',
            'type_id': 3
        },
       'shehui':{
            'url_type': 'shehui',
            'tagName': '社会',
            'type_id': 4
        },
        'shenghuo':{
            'url_type': 'shenghuo',
            'tagName': '生活',
            'type_id': 5
        },
        'rensheng':{
            'url_type': 'rensheng',
            'tagName': '人生',
            'type_id': 6
        },
        'renwu':{
            'url_type': 'renwu',
            'tagName': '人物',
            'type_id': 7
        },
        'lizhi':{
            'url_type': 'lizhi',
            'tagName': '励志',
            'type_id': 8
        },
        'shiye':{
            'url_type': 'shiye',
            'tagName': '视野',
            'type_id': 9
        },
        'xinling':{
            'url_type': 'xinling',
            'tagName': '心灵',
            'type_id': 10
        },
        'xiaoyuan':{
            'url_type': 'xiaoyuan',
            'tagName': '校园',
            'type_id': 11
        },
        'zhichang':{
            'url_type': 'zhichang',
            'tagName': '职场',
            'type_id': 12
        }
    }
    match = types.get(tagName)
    if(match):
        pageNum = end_page - start_page
        url_type = match['url_type']
        type_id = match['type_id']
        tagName = match['tagName']
        while(pageNum> 0):
            listPages.append({
                'tagId': type_id,
                'url_type': url_type,
                'tagName': tagName,
                'link': "http://www.ledu365.com/"+ url_type +"/list_"+ str(type_id) +"_"+ str(pageNum) +".html"
            })
            pageNum-=1
    return listPages


'''
从列表中获取文章的链接和缩略图链接
返回 {
    'tagId': 标签id,
    'link': 文章链接,
    'tagName': 标签名称,
    'url_type': 标签类型，例如qinggan,
    'pSrc': pSrc: 缩略图链接
}
'''
def getListUrl(liItem):
    pageList = []
    result = read(liItem['link'])
    if(result['status'] != 200):
        print('错误链接列表地址：'+ liItem['link'] )
    else:
        document = pq(result['html'])
        links = document(".listbox li")
        for item in links:
            pic = document(item).find('img')
            if not pic:
                break #没有图片就跳过，不要无缩略图的文章
            pSrc = pq(pic).attr('src') #缩略图链接
            link = document(item).find('.title').attr('href') #文章链接
            if (pSrc.find('http') == -1) :
                pSrc = 'http://www.ledu365.com' + pSrc
            
            pageList.append({
                'tagId': liItem.get('tagId'),
                'link': link,
                'tagName': liItem.get('tagName'),
                'url_type': liItem.get('url_type'),
                'pSrc': pSrc
            } )
    return pageList

'''
获取文章的内容，写入图片，写入数据库
返回 Boolean
'''        
def getPageContent(pageItem):
    global writeCount
    url = pageItem['link']
    if (url.find('http') == -1) :
        url = 'http://www.ledu365.com' + pageItem['link']
    result = read(url)

    if(result['status'] != 200):
        return False
    else:
        document = pq(result['html'])
    
    url_type = pageItem['url_type']
    smallImg = pageItem['pSrc']

    #需要从文章中获取 title、date、source、writer、bigImg（文章中的图片）
    title = document('.title h2').text()
    content = document('.content').find('p')
    bigImg = pq(document('.content div img')).attr('src')
    if not bigImg:
        return False
    bigImg = str(bigImg)
    if (bigImg.find('http') == -1):
        bigImg = 'http://www.ledu365.com' + bigImg

    date = ''
    source = ''
    writer = ''
    info = document('.info').text()
    splitArray = info.split(' ')
    if(len(splitArray)> 0):
         date = len(splitArray[0].split('时间:'))>1 and splitArray[0].split('时间:')[1]
         source = len(splitArray[1].split('来源:'))>1 and splitArray[1].split('来源:')[1]
         writer = len(splitArray[2].split('作者:'))>1 and splitArray[2].split('作者:')[1] 
    
    #检查图片目录，大图写入images，小图写入images/cut
    if not(os.path.exists(os.getcwd()+'/images/')):
        os.mkdir(os.getcwd()+'/images/')
    if not(os.path.exists(os.getcwd()+'/images/cut/')):
        os.mkdir(os.getcwd()+'/images/cut/')

    extName = '.jpg'
    smallName = 'cut/'+url_type + '_' + str(int(time.time()))  + '!cut' + extName
    smallResult =  writeImg(smallImg, smallName)
    if not smallResult:
        return False
    bigName = url_type + '_' + str(int(time.time()))  + extName
    bigResult = writeImg(bigImg, bigName)
    if not bigResult: 
        return False

    article = ArticleModel(
        title=title,
        writer=writer,
        content=content,
        source=source,
        date=date,
        tagId= int(pageItem.get('tagId')),
        tagName= pageItem.get('tagName'),
        img= bigImg,
        cutImg= smallImg,
    )
    try:
        article.save()
    except:
        print('写入数据库失败：')
        return False
    print('正在写入第'+str(writeCount)+'篇：'+ title)
    writeCount+=1
    return True

  
def writeImg(url, pname):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom' +
                'e/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    cutResponse = ''
    try:
        _req = req.Request(url, headers=headers)
        cutResponse = req.urlopen(_req).read()
    except urllib.error.URLError as e:
        print('获取图片失败:'+url ,e)
        return False

    try:
        with open(os.getcwd()+'/images/'+pname, 'wb') as f:
            f.write(cutResponse)
    except IOError as e:
        print('写入图片失败：'+ e)
        return False
    return True







