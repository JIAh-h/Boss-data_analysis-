import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import os
import time
import pandas as pd
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Boss直聘数据可视化.settings')
django.setup()
from myApp.models import JobInfo


# 广州：101280100  深圳：101280600  杭州：101210100  北京：101010100  上海：101020100  西安：101110100  苏州：101190400
# 天津：101030100  武汉：101200100  厦门：101230200  长沙：101250100  成都：101270100  郑州：101180100  重庆：101040100
class spider(object):
    def __init__(self, jobType, page):
        self.jobType = jobType
        # self.city = city
        self.page = page
        self.spiderUrl = 'https://www.zhipin.com/web/geek/job?query=%s&city=101190400&page=%s'

    def startBrowser(self):
        service = Service('./chromedriver.exe')
        option = webdriver.ChromeOptions()
        # option.add_experimental_option('debuggerAddress', 'localhost:9222')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(service=service, options=option)
        return browser

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'w', newline='', encoding='utf-8') as wf:
                writer = csv.writer(wf)
                writer.writerow(['title', 'address', 'jobType', 'educational', 'workExperience', 'workTag', 'salary',
                                 'salaryMonth', 'companyTag', 'hrWork', 'hrName', 'practice', 'companyTitle',
                                 'companyAvatar', 'companyNature', 'companyStatus', 'companyPeople', 'detailUrl',
                                 'companyUrl', 'dist',
                                 ])

    def save_to_csv(self, rowData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)

    def main(self, page):
        if self.page > page:
            return
        browser = self.startBrowser()
        print("正在爬取页码路径:" + self.spiderUrl % (self.jobType, self.page))
        browser.get(self.spiderUrl % (self.jobType, self.page))
        time.sleep(15)
        job_list = browser.find_elements(by=By.XPATH, value='//ul[@class="job-list-box"]/li')
        print(f"找到{len(job_list)}个职位")
        for index, job in enumerate(job_list):
            try:
                print("正在爬取第%d个数据" % (index + 1))
                # title
                title = job.find_element(by=By.XPATH,
                                         value='.//div[@class="job-title clearfix"]/span[@class="job-name"]').text
                # address
                addresses = job.find_element(by=By.XPATH, value='.//div[@class="job-title clearfix"]/span['
                                                                '@class="job-area-wrapper"]/span['
                                                                '@class="job-area"]').text.split('·')
                address = addresses[0]
                # dist
                if len(addresses) != 1:
                    dist = addresses[1]
                else:
                    dist = ''
                # jobType
                jobType = self.jobType
                # educational
                # workExperience
                tag_list = job.find_elements(by=By.XPATH,
                                             value='.//div[@class="job-info clearfix"]/ul[@class="tag-list"]/li')
                if len(tag_list) == 2:
                    educational = tag_list[1].text
                    workExperience = tag_list[0].text
                else:
                    educational = tag_list[2].text
                    workExperience = tag_list[1].text
                # hrName
                # hrWork
                hrInfo = job.find_element(by=By.XPATH,
                                          value='.//div[@class="job-info clearfix"]/div[@class="info-public"]').text
                hrWork = job.find_element(by=By.XPATH,
                                          value='.//div[@class="job-info clearfix"]/div[@class="info-public"]/em').text
                hrName = hrInfo.replace(hrWork, '')
                # workTag
                workTag_list = job.find_elements(by=By.XPATH,
                                                 value='.//div[@class="job-card-footer clearfix"]/ul[@class="tag-list"]/li')
                # workTag = json.dumps(list(map(lambda x: x.text, workTag)))
                workTag_Data = []
                for tag in workTag_list:
                    workTag_Data.append(tag.text)
                workTag = '|'.join(workTag_Data)
                # practice
                # salary
                # salaryMonth
                practice = False
                salaries = job.find_element(by=By.XPATH,
                                            value='.//div[@class="job-info clearfix"]/span[@class="salary"]').text
                if salaries.find('K') != -1:
                    salaries = salaries.split('·')
                    if len(salaries) == 1:
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = '0薪'
                    else:
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = salaries[1]
                elif salaries.find('元/月') != -1:
                    salary = list(map(lambda x: int(x), salaries.replace('元/月', '').split('-')))
                    salaryMonth = '0薪'
                else:
                    salary = list(map(lambda x: int(x), salaries.replace('元/天', '').split('-')))
                    salaryMonth = '0薪'
                    practice = True
                # companyTag
                companyTag = job.find_element(by=By.XPATH,
                                              value='.//div[@class="job-card-footer clearfix"]/div[@class="info-desc"]').text
                if not companyTag:
                    companyTag = "无"
                else:
                    companyTag = json.dumps(companyTag.split('，'), ensure_ascii=False)
                # companyTitle
                companyTitle = job.find_element(by=By.XPATH, value='.//div[@class="job-card-right"]/div['
                                                                   '@class="company-info"]/h3['
                                                                   '@class="company-name"]/a').text
                # companyAvatar
                companyAvatar = job.find_element(by=By.XPATH, value='.//div[@class="job-card-right"]/div['
                                                                    '@class="company-logo"]/a/img').get_attribute("src")
                companyInfos = job.find_elements(by=By.XPATH, value='.//div[@class="job-card-right"]/div['
                                                                    '@class="company-info"]/ul['
                                                                    '@class="company-tag-list"]/li')
                # companyNature
                # companyStatus
                # companyPeople
                if len(companyInfos) == 3:
                    companyNature = companyInfos[0].text
                    companyStatus = companyInfos[1].text
                    companyPeople = companyInfos[2].text
                else:
                    companyNature = companyInfos[0].text
                    companyStatus = "未融资"
                    companyPeople = companyInfos[1].text
                if companyPeople != '10000人以上':
                    companyPeople = list(map(lambda x: int(x), companyPeople.replace('人', '').split('-')))
                else:
                    companyPeople = [0, 10000]
                # detailUrl
                detailUrl = job.find_element(by=By.XPATH,
                                             value='.//div[@class="job-card-body clearfix"]/a').get_attribute(
                    "href")
                # companyUrl
                companyUrl = job.find_element(by=By.XPATH, value='.//div[@class="job-card-right"]/div['
                                                                 '@class="company-info"]/h3/a').get_attribute("href")
                # print(title, address, jobType, educational, workExperience, workTag, salary, salaryMonth,
                #       companyTag, hrName, hrWork, practice, companyTitle, companyAvatar, companyNature, companyStatus,
                #       companyPeople, detailUrl, companyUrl, dist)
                self.save_to_csv(
                    [title, address, self.jobType, educational, workExperience, workTag, salary, salaryMonth,
                     companyTag, hrName, hrWork, practice, companyTitle, companyAvatar, companyNature, companyStatus,
                     companyPeople, detailUrl, companyUrl, dist])
            # break
            except:
                pass
        self.page += 1
        self.main(page)

    def clear_csv(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df['salaryMonth'] = df['salaryMonth'].map(lambda x: x.replace('薪', ''))
        print("总数据为%d" % df.shape[0])
        return df.values

    def save_to_sql(self):
        data = self.clear_csv()
        for job in data:
            JobInfo.objects.create(
                title=job[0],
                address=job[1],
                jobType=job[2],
                educational=job[3],
                workExperience=job[4],
                workTag=job[5],
                salary=job[6],
                salaryMonth=job[7],
                companyTag=job[8],
                hrWork=job[9],
                hrName=job[10],
                practice=job[11],
                companyTitle=job[12],
                companyAvatar=job[13],
                companyNature=job[14],
                companyStatus=job[15],
                companyPeople=job[16],
                detailUrl=job[17],
                companyUrl=job[18],
                dist=job[19],

            )


# 在cmd中以管理员身份输入以下代码打开浏览器登录网页后进行复用
# chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\temp\chrome_profile
if __name__ == '__main__':
    # python java PHP 数据分析 web C++
    spiderObj = spider('数据分析', 1)  # 自行修改职业，位置都是广州，如果需要其他地方，要修改url同时加入循环进行爬取
    # spiderObj.init()
    # spiderObj.main(3)  # 开爬
    # JobInfo.objects.all()
    spiderObj.save_to_sql()  # 存入数据库
