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


parent_url = '父级下载地址'

url = '下载地址'


# 浏览器请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# group = (14,15,16,49,114,21)
group = ('15', '16', '21', '49')
for g in group:
    print(g)
    group_url = url + g
    for i in range(10, 11):
        # 分类页翻页
        cur_url = group_url + '&page=' + str(i)
        response = requests.get(cur_url)
        # response = requests.get(url, headers = headers)
        response.encoding = 'utf-8'

        # 分类页
        result = re.findall('<a href="html_data/(.*?)" id="', response.text)
        print(len(result))
        print(result)
        for r in result:
            # 详情页
            page_url = parent_url + "html_data/" + r
            page_response = requests.get(page_url)
            page_response.encoding = 'utf-8'
            # print(page_response.text)
            title = re.findall('<span id="subject_tpc">(.*?)</span>', page_response.text)
            print(title)
            img_result = re.findall('<img src="(.*?)" border="0"', page_response.text)
            print(img_result)
            for img in img_result:
                # 图品
                path = '/image/' + g + '/' + str(i) + '/' + str(title) + '/'
                name = img.split('/')[-1]
                name = str.replace(name, '\'', '')
                response_image = requests.get(img)
                response_image.encoding = 'utf-8'
                save(response_image.content, path + name)
                # break

