import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from pymysql import *
import json


def get_img(field, targetImage, resImageSrc):
    con = connect(host='localhost', port=3306, database='boss', user='root', password='030813', charset='utf8mb4')
    cur = con.cursor()
    sql = f"select {field} from jobinfo"
    cur.execute(sql)
    data = cur.fetchall()
    # print(data)
    text = ""

    # companyTags
    # for i in data:
    #     if i[0] != '无':
    #         companyTagsArr = json.loads(i[0])
    #         for j in companyTagsArr:
    #             text += j

    # title
    for i in data:
        text += i[0]

    cur.close()
    con.close()
    cut = jieba.cut(text, cut_all=False)
    stop_words = []
    with open('./stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if len(line) > 0:
                stop_words.append(line.strip())
    data_result = [x for x in cut if x not in stop_words]
    string = ' '.join(data_result)

    # 图片
    img = Image.open(targetImage)
    img_array = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 关闭坐标轴
    plt.savefig(resImageSrc, dpi=500)  # 保存图片


# get_img('companyTag', '../static/1.png', '../static/companyTags_cloud.png')
get_img('title', '../static/2.png', '../static/title_cloud.png')

