# -*coding=utf-8*-
#货架扫码
#By:王大融
import sys
import webbrowser
import os
import tkinter
from tkinter import filedialog
import time
from pyzbar import pyzbar
from PIL import Image
import winreg

'''浏览器列表'''
browser_regs = {
    '360': r"SOFTWARE\Clients\StartMenuInternet\360Chrome\DefaultIcon",
    'edge': r"SOFTWARE\Clients\StartMenuInternet\Microsoft Edge\DefaultIcon",
    'chrome': r"SOFTWARE\Clients\StartMenuInternet\Google Chrome\DefaultIcon",
    'firefox': r"SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon",
    'IE': r"SOFTWARE\Clients\StartMenuInternet\IEXPLORE.EXE\DefaultIcon",
}

def getbrowserpath():
    path_li = []
    for i in browser_regs:
        try:
            key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,browser_regs[i])
            value, _type = winreg.QueryValueEx(key, "")
            path_li.append(value.split(",")[0])
        except FileNotFoundError:
            pass
    if path_li == []:
        print("没有可用的浏览器！")
        for i in range(5, 0, -1):
            print("\r{}秒后退出".format(i), end="")
            time.sleep(1)
        exit()
    else: return path_li
def getbrowsername():
    path = getbrowserpath()[0]
    name = path.split("\\")[-1]
    return name
def 访问网页(url):
    path = getbrowserpath()[0]
    name = getbrowsername()    #浏览器可执行文件名
    print("使用【{}】执行任务".format(name))
    webbrowser.register('liulanqi', None, webbrowser.BackgroundBrowser(path))
    for i in range(5):
        webbrowser.get('liulanqi').open(url, new=1, autoraise=True)
        time.sleep(1)
        i += 1
    time.sleep(5)
    os.system('taskkill /F /IM {}'.format(name))
def welcome():
    print("\n{:-^50}".format("<智慧货架刷扫码量,By:咸鱼网友>"))
    print("使用说明：")
    print("选择含有二维码的图片，输入需要刷的次数，回车即可\n")
def getFile_Path():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path == "":
        print("没有选择图片，即将退出")
        for i in range(5, 0, -1):
            print("\r{}秒后退出".format(i), end="")
            time.sleep(1)
        sys.exit()
    else:
        return file_path
def QrToLink(file_path):
    try:
        img = Image.open(file_path)  # 打开文件路径，将值赋给img
        data_list = pyzbar.decode(img)  # 解码后赋值给data
        # 从解码结果中提取出链接
        for link_text in data_list:
            link_text = link_text.data.decode("utf-8")
            if link_text == None:
                print("二维码解析失败！")
                for i in range(5, 0, -1):
                    print("\r{}秒后退出".format(i), end="")
                    time.sleep(1)
                sys.exit()
            else:
                return link_text
    except:
        print("无法解析该图片！")
        for i in range(5, 0, -1):
            print("\r{}秒后退出".format(i), end="")
            time.sleep(1)
        sys.exit()
def main():
    try:
        welcome()
        print("请选择图片")
        file_path = getFile_Path()
        print("图片路径为：{}".format(file_path))
        url = QrToLink(file_path)
        print("二维码解析成功，解析后网址为：{}".format(url))
        cishu = int(round(eval(input("请输入需要访问的次数："))/5,0))
        if cishu > 10:
            print("输入的次数较多，可能会耗费较长时间...期间请勿锁屏或关机")
        print("任务开始")
        #访问网页(url)
        start = time.perf_counter()
        for i in range(cishu):
            访问网页(url)
            print("已模拟访问{}次".format((i+1)*5))
        end = time.perf_counter()
        print("\n任务完成，已模拟访问{}次,共耗时{:.2f}分钟。".format((i+1)*5,(end-start)/60))
        input("按任意键退出")
    except (NameError,SyntaxError):
        print("次数应为正整数！")
        input("按任意键退出")

if __name__ == '__main__':
    main()
