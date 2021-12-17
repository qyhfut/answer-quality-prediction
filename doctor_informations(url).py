######爬取医生主页对应的URL信息######

# 导入模块
from bs4 import BeautifulSoup     # 网页解析， 获取数据
import re       # 正则表达式， 进行文字匹配
import urllib.request, urllib.error     # 指定URL， 获取网页数据
import xlwt     # 进行excel操作
import sqlite3  # 进行SQLite数据库操作

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from lxml import etree
from copy import deepcopy




def main():
    filename = 'F:/haodf-prediction/2020/2020url/2020url_60001-70000.txt'
    source = open(filename, 'r', encoding='utf-8')
    lines = source.readlines()

    doctor_url_list = []

    for i in range(len(lines)):
        total_doctor_links = []
        baseurl = lines[i]     #咨询详情链接
        print('第{}条:'.format(i), lines[i].replace('\n', ''))

        s = get_session()
        r = s.get(baseurl)
        soup1 = BeautifulSoup(r.content, "lxml")

        # print("soup1", soup1)
        # print(soup1.select('div.doctor-card-btn > a'))

        if soup1.select('div.doctor-card-btn > a') == []:
            total_doctor_links.append(baseurl)
            doctor_href = ''
            print("医生主页连接：", doctor_href)
            print("\n")
            total_doctor_links.append(doctor_href)
        else:
            doctor_href = soup1.select('div.doctor-card-btn > a')[0].get('href')  #医生主页链接
            print("医生主页连接：", doctor_href)
            print("\n")
            total_doctor_links.append(baseurl)
            total_doctor_links.append(doctor_href)
        doctor_url_list.append(total_doctor_links)

    savepath1 = 'F:/haodf-prediction/2020/2020url/2020url_60001-70000.xls'
    saveDoctor_url(lines, doctor_url_list, savepath1)





    que_cnt = 0
    doctorlist = []
    for input_url in doctor_url_list:

        que_cnt += 1
        print('----------------------------------------------------')
        print('que_cnt:', que_cnt)

        if input_url[1] == '':
            a = []
            datalist.extend(a)
        else:
            s1 = get_session()
            r2 = s1.get(input_url[1])
            soup = BeautifulSoup(r2.content, "lxml")
            # print("soup:", soup)
            datalist = []

            # 1 病例链接
            datalist.append(input_url[0])
            # 2 医生主页链接
            datalist.append(input_url[1])

            # 3 医生姓名
            doctor_name = soup.select('div.profile-txt > h1')[0].text.strip()
            print("doctor_name:", doctor_name)
            datalist.append(doctor_name)
            # 4 医生职称
            doctor_level = soup.select('div.profile-txt > span')[0].text.strip()
            print("doctor_level:", doctor_level)
            datalist.append(doctor_level)
            # 5 教授。。。
            if len(soup.select('div.profile-txt > span')) == 2:
                doctor_position = soup.select('div.profile-txt > span')[1].text.strip()
            else:
                doctor_position = ''

            print("doctor_position:", doctor_position)
            datalist.append(doctor_position)
            # 6 所在医院
            hospital = soup.select('ul.doctor-faculty-wrap > li > a')[0].text.strip()
            print("hospital:", hospital)
            datalist.append(hospital)




            # 7 科室
            Department = soup.select('ul.doctor-faculty-wrap > li > a')[1].text.strip()
            print("Department:", Department)
            datalist.append(Department)


            # 8 年度好大夫
            if len(soup.select('div.honor-wrap')) == 0:
                year_haodf = ''
            else:
                # print("soup.select('div.honor-wrap')", soup.select('div.honor-wrap'))
                year_haodf = soup.select('div.honor-wrap')[0].text.strip()

            print("year_haodf:", year_haodf)
            datalist.append(year_haodf)

            # 9 综合推荐热度
            hot = soup.select('ul.profile-statistic > li > span')[1].text.strip()
            print("hot:", hot)
            datalist.append(hot)
            # 10 在线服务满意度
            Satisfaction = soup.select('ul.profile-statistic > li > span')[3].text.strip()
            print("Satisfaction:", Satisfaction)
            datalist.append(Satisfaction)
            # 11 在线问诊量
            num_inquiry = soup.select('ul.profile-statistic > li > span')[5].text.strip()
            print("num_inquiry:",num_inquiry)
            datalist.append(num_inquiry)
            # 12 总访问
            Views = soup.select('div.aside-container > aside > ul > li > span')[1].text.strip()
            print("Views:", Views)
            datalist.append(Views)

            # 13 患者投票
            global Votes
            for i in range(len(soup.select('section.container > header > a'))):
                if soup.select('section.container > header > a')[i].text.strip() == '查看全部投票' not in soup.select('section.container > header > a')[i].text.strip():
                    Votes = ''
                else:
                    Votes = soup.select('main.main-container > section > header > h2 > span > span')[0].text.strip()

            print("Votes:", Votes)
            datalist.append(Votes)


            # 14 总文章
            global articleCount
            for i in range(len(soup.select('section.container > header > a'))):
                if soup.select('section.container > header > a')[i].text.strip() == '查看全部文章' not in soup.select('section.container > header > a')[i].text.strip():
                    articleCount = ''
                else:
                    articleCount = soup.select('main.main-container > section > header > h2 > span > span')[1].text.strip()
            print("articleCount :", articleCount)
            datalist.append(articleCount)



            # 15 诊后服务星
            print(len(soup.select('div.aside-container > aside > ul > li > span')))
            if len(soup.select('div.aside-container > aside > ul > li > span')) <= 26:
                num_star = ''
            else:
                stars = []
                star1 = soup.select('div.aside-container > aside > ul > li > span > img')[0].get('alt')
                stars.append(star1)
                star2 = soup.select('div.aside-container > aside > ul > li > span > img')[1].get('alt')
                stars.append(star2)
                star3 = soup.select('div.aside-container > aside > ul > li > span > img')[2].get('alt')
                stars.append(star3)
                star4 = soup.select('div.aside-container > aside > ul > li > span > img')[3].get('alt')
                stars.append(star4)
                star5 = soup.select('div.aside-container > aside > ul > li > span > img')[4].get('alt')
                stars.append(star5)
                print("stars", stars)

                s = 0
                for star in stars:
                    if star == '金色星星':
                        s += 1
                        num_star = s
            print("num_star:", num_star)
            datalist.append(num_star)


            # 16 诊治后的患者数
            if len(soup.select('div.aside-container > aside > ul > li > span')) <= 26:
                after_patient = ''
            else:
                after_patient = soup.select('div.aside-container > aside > ul > li > span')[29].text.strip()
            print("after_patient:", after_patient)
            datalist.append(after_patient)

            # 17 随访中的患者数
            if len(soup.select('div.aside-container > aside > ul > li > span')) <= 26:
                now_patient = ''
            else:
                now_patient = soup.select('div.aside-container > aside > ul > li > span')[31].text.strip()
            print("now_patient:", now_patient)
            datalist.append(now_patient)

            # 18 收到的礼物
            # gifts = soup.select('div.aside-container > aside > div > div > span')[0].text.strip()
            # print("gifts:", gifts)
            # datalist.append(gifts)
            print("soup.select('div.aside-container > aside > div > div')",
                  soup.select('div.aside-container > aside > div > div'))
            if soup.select('div.aside-container > aside > div > div') == [] or soup.select(
                    'div.aside-container > aside > div > div > span') == []:
                gifts = ''
            else:
                gifts = soup.select('div.aside-container > aside > div > div > span')[0].text.strip()
            print("gifts:", gifts)
            datalist.append(gifts)

            # 19 疗效满意度  # 20 态度满意度
            if len(soup.select('div.satisfaction.clearfix > div > i')) == 0:
                effect_sat = soup.select('div.satisfaction.clearfix > div > span')[0].text.strip()
                attitude_sat = soup.select('div.satisfaction.clearfix > div > span')[1].text.strip()
            else:
                effect_sat = soup.select('div.satisfaction.clearfix > div > i')[0].text.strip()
                attitude_sat = soup.select('div.satisfaction.clearfix > div > i')[1].text.strip()
            print("effect_sat:", effect_sat)
            datalist.append(effect_sat)
            print("attitude_sat:", attitude_sat)
            datalist.append(attitude_sat)

        doctorlist.append(datalist)
        print("doctorlist", doctorlist)



    # 3.1 保存数据到Excel
    savepath = 'F:/haodf-prediction/2019/2019url/2019url_70001-76050好大夫医生主页信息.xls'
    saveData(len(doctorlist), doctorlist, savepath)              # 调用存储函数
   
    # # 3.2 保存数据到数据库
    # dbpath = 'movie.db'
    # saveData2DB(datalist, dbpath)



def get_session():
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    requests.DEFAULT_RETRIES = 15  # 增加重试连接次数
    s.keep_alive = False  # 关闭多余连接
    # s.verify = False
    return s



def askURL(url):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"}
    # print("url:", url)
    req = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        # print("response",response)

        # print(response.url)

        if response.url == 'https://www.haodf.com/':
            html = None
        else:
            html = response.read().decode('utf-8')
            # print("html", html)
    except urllib.error.URLError as e:
        pass
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html




def saveData(lines, doctorlist, savepath):
    print('正在保存.......')
    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    # 创建工作表
    sheet = book.add_sheet('好大夫医生主页信息 ', cell_overwrite_ok=True)

    # 创建一个列的元组
    col = ('1病例链接', '2医生主页链接', '3医生姓名', '4医生职称', '5教授', '6所在医院', '7科室',
           '8年度好大夫',  '9综合推荐热度', '10在线服务满意度', '11在线问诊量',
           '12总访问', '13患者投票', '14总文章', '15诊后服务星', '16诊治后的患者数', '17随访中的患者数',
           '18收到的礼物', '19疗效满意度', '20态度满意度')

    for i in range(0, 20):
        # 写入数据， 第一行参数为‘行’， 第二行参数为‘列’， 第三行参数为内容
        sheet.write(0, i, col[i])   # 写入列的数据

    # for i in range(2):
    for i in range(lines):
        print(f'正在写入第{i+1}条')
        data = doctorlist[i]     # 因为datalist是列表的嵌套，所以要一个信息的传
        print(data)
        # 传第单个信息
        for j in range(0, 20):
            sheet.write(i+1, j, data[j])    # 保存数据

    # 保存数据表
    book.save(savepath)


def saveDoctor_url(lines, doctorlist, savepath):
    print('正在保存.......')
    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    # 创建工作表
    sheet = book.add_sheet('好大夫医生主页链接 ', cell_overwrite_ok=True)

    # 创建一个列的元组
    col = ('1病例链接', '2医生主页链接')

    for i in range(0, 2):
        # 写入数据， 第一行参数为‘行’， 第二行参数为‘列’， 第三行参数为内容
        sheet.write(0, i, col[i])   # 写入列的数据

    # for i in range(2):
    for i in range(len(lines)):
        print(f'正在写入第{i+1}条')
        data = doctorlist[i]     # 因为datalist是列表的嵌套，所以要一个信息的传
        print(data)
        # 传第单个信息
        for j in range(0, 2):
            sheet.write(i+1, j, data[j])    # 保存数据

    # 保存数据表
    book.save(savepath)




if __name__ == "__main__":
    main()

    print('爬取完成！')