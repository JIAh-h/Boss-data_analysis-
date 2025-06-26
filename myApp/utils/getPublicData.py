from myApp.models import *

monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']

educationList = {'博士': 1, '硕士': 2, '本科': 3, '大专': 4, '高中': 5, '中专/中技': 6, '初中及以下': 7, '学历不限': 8}
workExperience = ['在校/应届', '1-3年', '3-5年', '5-10年', '10年以上', '经验不限']
salaryList = ['10k以下', '10k-20k', '20k-30k', '30k-40k', '40k以上']
companyPeople = ['20人以下', '100人以下', '500人以下', '1000以下', '1万人以下', '1万人以上']


def getAllUser():
    return User.objects.all()


def getAllJob():
    return JobInfo.objects.all()
