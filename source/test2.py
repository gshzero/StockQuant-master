import requests

import os
for i in range(1, 3):
    url = "https://img2.wnacg.org/data/0801/68/00%s.jpg" % str(i)

    d = 'F:\\B\\'

    path = d + url.split('/')[-1]

    # try:

    if not os.path.exists(d):
        os.mkdir(d)

    if not os.path.exists(path):

        r = requests.get(url)

        r.raise_for_status()

        with open(path, 'wb') as f:

            f.write(r.content)

            f.close()

            print("图片保存成功")

    else:

        print("图片已存在")

    # except:
    #
    #     print("图片获取失败")
