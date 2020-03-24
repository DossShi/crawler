import requests
import re
import os


def save(html, path):
    '''
    以文件形式保存数据
    :param html: 要保存的数据
    :param path: 要保存数据的路径
    :return:
    '''
    # 判断目录是否存在
    if not os.path.exists(os.path.split(path)[0]):
        # 目录不存在创建，makedirs可以创建多级目录
        os.makedirs(os.path.split(path)[0])
    try:
        # 保存数据到文件
        with open(path, 'wb') as f:
            f.write(html)
        print('保存成功')
    except Exception as e:
        print('保存失败', e)


url = '要爬的网址'
# 浏览器请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
# 请求网址
response = requests.get(url)
# response = requests.get(url, headers = headers)
response.encoding = 'utf-8'

# 打印网页中的数据
# print(response.text)
# 下载图片

result = re.findall('<a href="html_data/(.*?)" id="', response.text)
print(len(result))
print(result)
for r in result:
    page_url = parent_url + "html_data/" + r
    page_response = requests.get(page_url)
    page_response.encoding = 'utf-8'
    # print(page_response.text)
    title = re.findall('<span id="subject_tpc">(.*?)</span>', page_response.text)
    print(title)
    img_result = re.findall('<img src="(.*?)" border="0"', page_response.text)
    print(img_result)
    for img in img_result:
        path = '/image/' + str(title) + '/'
        name = img.split('/')[-1]
        response_image = requests.get(img)
        response_image.encoding = 'utf-8'
        # with open(name, mode="wb") as f:
        #     f.write(response_image.content)
        save(response_image.content, path + name)
        break

# 提取图片的下载地址
# title = re.findall('<span id="subject_tpc">(.*?)</span>', response.text)
# print(title)
# result = re.findall('<img src="(.*?)" border="0"', response.text)
# print(len(result))
# print(result)
# for r in result:
#     print(r)
#     # 从链接中取出图片的名字
#     path = '/image/' + str(title) + '/'
#     name = r.split('/')[-1]
#     print(name)
#     response_image = requests.get(r)
#     # response_image = requests.get(r, headers = headers)
#     # with open(path + name, mode="wb") as f:
#     #     f.write(response_image.content)
#     save(response_image.content, path+name)
#     # break

# 提取页面
# page_urls = re.findall('<')
# for i in range(1,10):
#     print(i)
#     cur_page_url = parent_url + 'thread.php?fid=16&page=' + str(i)
#     print(cur_page_url)
