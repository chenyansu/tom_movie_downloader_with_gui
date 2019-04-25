
import requests
import random
import time
from requests.adapters import HTTPAdapter
import logging
import sys

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='downloadplayer.log', level=logging.INFO, format=LOG_FORMAT)

def downloader(url, out):
    """
    下载器
    :param url:
    :param out:
    :return:
    """
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=100))
    s.mount('https://', HTTPAdapter(max_retries=100))
    r = s.get(url, headers=headers, timeout=10)
    with open(out, "ab") as f:
        f.write(r.content)


def loop_download(base_url, out="", amount=1, finish_num=-1, postfix="", prefix=""):
    """
    主程序
    :param base_url:
    :param prefix:
    :param postfix:
    :param amount:
    :param out:
    :param finish_num:
    :return:
    """

    amount = int(amount)
    finish_num = int(finish_num)

    for num in range(amount+1):
        if num > finish_num: # 用来避免重复下载
            num = str(num).zfill(3) # 补位，比如“001”
            url = prefix+base_url+num+postfix
            # downloader(url, outdir+num+postfix)
            # time.sleep(random.randint(1, 3))
            downloader(url, out+postfix)
            print("{}({})下载完成，总进度（{}/{}）,如果中断，请记录完成号码{}方便追加".format(out, url, num, amount,num))
            logging.info("{}({})下载完成 , 总进度（{}/{}）,已完成号码 {} ".format(out, url,num, amount, num))



if __name__ == "__main__":
    # loop_download(base_url="https://www.safjierwe.com/upload/2018-11-27/5af9952fce0ab2d7af2f932280b357bc/m3u8/abc", postfix=".ts", amount=10)
    loop_download(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

