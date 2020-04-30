import requests
import time
import datetime
import json
import math
import random

# 初始化，不可修改
baseUrl = 'http://www.cqooc.com'
owner_id = int(0)

# 个人信息，自行修改
username = '111111111111111'   # 用户名
password = '2222222222'        # 密码
xsid = '3333333333333333'      # 登陆的 cookie 信息
course_id = 'xxxxxxxxx'        # 课程 id
cid = 'xxxxxxxx'               # 课程 cid

session = requests.Session()
session.cookies['xsid'] = xsid

# def to_hex(v):
#     arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
#     str = ''
#     str += arr[int(v >> 28 & 0xF)]
#     str += arr[int(v >> 24 & 0xF)]
#     str += arr[int(v >> 20 & 0xF)]
#     str += arr[int(v >> 16 & 0xF)]
#     str += arr[int(v >> 12 & 0xF)]
#     str += arr[int(v >> 8 & 0xF)]
#     str += arr[int(v >> 4 & 0xF)]
#     str += arr[int(v >> 0 & 0xF)]
#     return str

# def login():
#     # 首先需要获取到 nonce 字段
#     nonce_url = 'http://www.cqooc.com/user/login?ts=' + str(round(time.time() * 1000))
#     nonce_str = session.get(nonce_url).json()['nonce']
#     # TOOD: 是否获取到 nonce 字符
#     print('成功获取 nonce: ' + nonce_str)

#     cache_left = math.floor(random.random() * math.pow(2, 32))
#     cache_right = math.floor(random.random() * math.pow(2, 32))
#     cnonce_str = to_hex(cache_left) + to_hex(cache_right)
#     print(hex(password))
#     print('计算 cnonce: ' + cnonce_str)

#     request_url = baseUrl + '/user/login?username=' + username + '&password=' + password + '&nonce=' + nonce_str + '&cnonce=' + cnonce_str
#     post = requests.post(request_url)

#     print(post.text)

def get_time():
    return str(round(time.time() * 1000))

def get_session_id():
    url = 'http://www.cqooc.com/user/session?xsid=' + xsid + '&ts=' + get_time()
    return int(session.get(url).json()['id'])

# 看视频
def watch_video(parentId, sectionId, chapterId):
    head = {
            'Host': 'www.cqooc.com',
            # 'Content-Length': '157',
            'Connection': 'keep-alive',
            'Origin': 'http://www.cqooc.com',
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Referer': 'http://www.cqooc.com/learn/mooc/structure?id=' + course_id,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'player=1; xsid=' + xsid,
    }

    data = {
        "username": username,
        "ownerId": owner_id,
        "parentId": parentId,
        "action": 0,
        "courseId": course_id,
        "sectionId": int(sectionId),
        "chapterId": chapterId,
        "category": 2
    }

    ps = requests.post(url='http://www.cqooc.com/learnLog/api/add', json=data, headers=head, timeout=None)

    if ps.status_code == 200:
        code = ps.json()['code']
        if code == 2:
            print('已经添加，跳过\n')
            return
        if code == 0:
            # 成功
            print(ps.text + '\n')
            time.sleep(3)
            return
        if code == 3:
            # 非法操作
            print('草泥马，非法操作 error, 尝试等10秒再请求 \n')
            time.sleep(10)
            watch_video(parentId, sectionId, chapterId)
            return

# ------------------------

# 论坛

def do_forum(parentId, sectionId, chapterId, forumId):
    head = {
            'Host': 'www.cqooc.com',
            # 'Content-Length': '157',
            'Connection': 'keep-alive',
            'Origin': 'http://www.cqooc.com',
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Referer': 'http://www.cqooc.com/learn/mooc/structure?id=' + course_id,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'player=1; xsid=' + xsid,
    }

    data = {
        'ownerId': owner_id,
        'username': username,
        'status': '1',
        'level': '1',
        'parentId': parentId,
        'courseId': course_id,
        'voteNum': 0,
        'commentNum': 0,
        'category': '2',
        'content': 'hello, hola',
        'forumId': forumId
    }

    ps = requests.post(url='http://www.cqooc.com/json/forum/posts', json=data, headers=head, timeout=None)

    if ps.status_code == 200:
        code = ps.json()['code']

        if code == 0:
            # 成功
            print(ps.text + '\n')
            time.sleep(3)
            return

        if code == 2:
            print('已经添加，跳过\n')
            return

        if code == 3:
            print('提交失败, 重试中' + ps.text)
            time.sleep(3)
            do_forum(parentId, sectionId, chapterId, forumId)
            return

# ------------------------

def fuckTest():
    return

def do_chapter(id):
    url = baseUrl + '/json/mooc/lessons?parentId=' + id + '&limit=100&sortby=selfId&reverse=false&ts=' + get_time()
    head = {
        'Host': 'www.cqooc.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'player=1; xsid=' + xsid,
        'Referer': 'http://www.cqooc.net/learn/mooc/structure?id=' + course_id,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    json = session.get(url, headers=head).json()

    if ('data' in json):
        jsonData = json['data']
    else:
        return

    if len(jsonData) == 0:
        print(id + '为空跳过\n')
        return

    for item in jsonData:
        category = item['category']
        title = item['title']

        # 1 是视频
        if category == '1':
            # print(item['chapter']['title'] + title + ', 是视频, 分类' + category)

            if ('resource' in item):
                resUrl = 'http://www.cqooc.com/json/my/res?id=' + item['resource']['id'] + '&ts=' + get_time()
                res_session = session.get(resUrl)
                print('获取视频资源：' + str(res_session.status_code))

            # learnLogs 读取
            # get_log(item['id'])
            # time.sleep(1)

            watch_video(cid, item['id'], item['parentId'])
        elif category == '2':
            return
            testId = item['testId']
            paperUrl = 'http://www.cqooc.com/json/exam/papers?id=' + testId + '&ts=' + get_time()
            paperSession = session.get(paperUrl)
            paperJson = paperSession.json()

            # 获取测试题
            resourceUrl = 'http://www.cqooc.com/test/api/paper/get?id=' + testId
            resourceSession = session.get(resourceUrl, headers=head)
            resourceJson = resourceSession.json()['body'][0]['questions']

            for item in resourceJson:
                # 题目类型
                # 0是单选题, 1是多选题, 4是判断题
                testType = item['type']

                if testType == '0':
                    print('单选题')
                elif testType == '1':
                    print('多选题')
                elif testType == '4':
                    print('判断题')

            print('\n')

            # print(resourceJson)
            # print('测试id ' +  testId + '\n')

        elif category == '3':
            forumId = item['forumId']
            forumUrl = 'http://www.cqooc.com/json/forum?id=' + forumId + '&ts=' + get_time()
            forumSession = session.get(forumUrl)
            print('论坛提交')
            do_forum(cid, item['id'], item['parentId'], forumId)
            watch_video(cid, item['id'], item['parentId'])

if __name__ == '__main__':
    owner_id = get_session_id()
    print('已经获取到 owner id: ' + str(owner_id))

    url = baseUrl + '/json/chapters?status=1&select=id,title,level&courseId=' + course_id + '&sortby=selfId&reverse=false&limit=200&start=0&ts=' + get_time()
    head = {
        'Host': 'www.cqooc.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'player=1; xsid=' + xsid,
        'Referer': 'http://www.cqooc.net/learn/mooc/structure?id=' + course_id,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    json = session.get(url, headers=head).json()['data']
    id_list = []
    for item in json:
        id_list.append(item['id'])
    # 排序
    id_list.sort()
    for id in id_list:
        do_chapter(id)
