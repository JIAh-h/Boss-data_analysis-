import json
from django.shortcuts import render, redirect
from myApp.models import User
from .utils.error import *
import hashlib
from .utils import getHomeData
from .utils import getSelfInfo
from .utils import getChangePasswordData
from .utils import getTableData
from .utils import getHistoryTableData
from .utils import getSalaryCharData
from .utils import getCompanyCharData
from .utils import getEducationalCharData
from .utils import getCompanyStatusCharData
from .utils import getAddressCharData
from django.core.paginator import Paginator
from urllib.parse import unquote


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pwd.encode())
        pwd = md5.hexdigest()
        try:
            user = User.objects.get(username=uname, password=pwd)
            request.session['username'] = user.username
            return redirect('/myApp/home')
        except:
            return errorResponse(request, '用户名或密码出错！')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        checkpwd = request.POST.get('checkPassword')
        try:
            User.objects.get(username=uname)
        except:
            if not uname or not pwd or not checkpwd:
                return errorResponse(request, '不允许为空！')
            if checkpwd != pwd:
                return errorResponse(request, '第二次密码与第一次不符，请重新输入！')
            # 对密码进行加密
            md5 = hashlib.md5()
            md5.update(pwd.encode())
            pwd = md5.hexdigest()
            User.objects.create(username=uname, password=pwd)
            return redirect('/myApp/login')
        return errorResponse(request, '该用户名已被注册！')


def logOut(request):
    request.session.clear()
    return redirect('login')


def home(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    yer, mon, day = getHomeData.getNowTime()
    userCreateDate = getHomeData.getUserCreateTime()
    top6User = getHomeData.getTop6User()
    job_num, user_num, top_education, max_salary, city = getHomeData.getAllTag()
    data_list = getHomeData.getAllJobInfo()
    # 新增分页数据获取
    page = request.GET.get('page', 1)
    jobs_data = getHomeData.getAll(page=int(page))
    date_data = getHomeData.getDateData()
    return render(request, 'index.html', {
        'userInfo': userInfo,
        'dateInfo': {
            'year': yer,
            'month': mon,
            'day': day
        },
        'userCreateDate': userCreateDate,
        'top6User': top6User,
        'jobInfo': {
            'job_num': job_num,
            'user_num': user_num,
            'top_education': top_education,
            'max_salary': max_salary,
            'city': city
        },
        'data_list': data_list,
        # 新增分页数据传参
        'jobs': jobs_data['jobs'],
        'pagination': jobs_data['pagination'],
        'dateData': json.dumps(date_data)
    })


def selfInfo(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    education, workExperience, joblist = getSelfInfo.getPageData()
    if request.method == 'POST':
        getSelfInfo.changeSelfInfo(request.POST, request.FILES)
        userInfo = User.objects.get(username=uname)
    return render(request, 'selfInfo.html', {
        'userInfo': userInfo,
        'pageData': {
            'education': education,
            'workExperience': workExperience,
            'job': joblist
        }
    })


def changePassword(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    if request.method == 'POST':
        res = getChangePasswordData.changePassword(userInfo, request.POST)
        if res != None:
            return errorResponse(request, res)
        userInfo = User.objects.get(username=uname)
    return render(request, 'changePassword.html', {
        'userInfo': userInfo
    })


def tableData(request):
    # 获取当前登录用户信息
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)

    # 获取所有表格数据
    tableData = getTableData.getTableData()

    # 创建分页器（每页10条数据）
    paginator = Paginator(tableData, 10)

    # 获取当前页码（默认为第1页）
    page_number = int(request.GET.get('page', 1))
    current_page = paginator.page(page_number)  # 获取当前页对象

    # 计算分页导航范围
    visibleNumber = 10  # 最多显示10个页码
    start_page = max(1, page_number - visibleNumber // 2)  # 起始页码（保持居中显示）
    end_page = min(start_page + visibleNumber, paginator.num_pages + 1)  # 结束页码

    # 将数据传递给模板
    return render(request, 'tableData.html', {
        'userInfo': userInfo,  # 用户信息
        'current_page': current_page,  # 当前页数据对象
        'page_range': range(start_page, end_page),  # 页码范围生成器
        'paginator': paginator  # 分页器对象
    })


def historyTableData(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    historyData = getHistoryTableData.getHistoryData(userInfo)
    return render(request, 'historyTableData.html', {
        'userInfo': userInfo,
        'historyData': historyData
    })


def addHistory(request, jobId):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    getHistoryTableData.addHistory(userInfo, jobId)
    return redirect('historyTableData')


def removeHistory(request, hisId):
    getHistoryTableData.removeHistory(hisId)
    return redirect('historyTableData')


def salary(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    educations, workExperiences= getSalaryCharData.getPageData()
    defaultEducation = '不限'
    defaultWorkExperience = '不限'
    if request.GET.get('educational'):
        defaultEducation = request.GET.get('educational')
    if request.GET.get('workExperience'):
        defaultWorkExperience = request.GET.get('workExperience')
    salaryList, barData, legends = getSalaryCharData.getBarData(defaultEducation, defaultWorkExperience)
    pieData = getSalaryCharData.pieData()
    funnelData = getSalaryCharData.getFunnelData()
    return render(request, 'salaryChar.html', {
        'userInfo': userInfo,
        'educational': educations,
        'workExperience': workExperiences,
        'defaultEducation': defaultEducation,
        'defaultWorkExperience': defaultWorkExperience,
        'salaryList': salaryList,
        'barData': barData,
        'legends': legends,
        'pieData': pieData,
        'funnelData': funnelData
    })


def company(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    typeList = getCompanyCharData.getPageData()
    jobType = 'all'
    if request.GET.get('jobType'):
        jobType = request.GET.get('jobType')
    jobType = unquote(jobType)
    rowData, columData = getCompanyCharData.getCompanyBar(jobType)
    pieData = getCompanyCharData.getCompanyPie(jobType)
    companyPeople, lineData = getCompanyCharData.getCompanyPeople(jobType)
    return render(request, 'companyChar.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'jobType': jobType,
        'rowData': rowData,
        'columData': columData,
        'pieData': pieData,
        'companyPeople': companyPeople,
        'lineData': lineData
    })


def companyTags(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    return render(request, 'companyTags.html', {
        'userInfo': userInfo
    })


def educational(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    defaultEducation = '不限'
    if request.GET.get('educational'):
        defaultEducation = request.GET.get('educational')
    educational = getEducationalCharData.getPageData()
    workExperience, charDataColumOne, charDataColumTwo, hasEmpty = getEducationalCharData.getExperienceData(defaultEducation)
    barDataRow, barDataColum = getEducationalCharData.getPeopleData()
    return render(request, 'educationalChar.html', {
        'userInfo': userInfo,
        'educational': educational,
        'defaultEducation': defaultEducation,
        'workExperience': workExperience,
        'charDataColumOne': charDataColumOne,
        'charDataColumTwo': charDataColumTwo,
        'hasEmpty': hasEmpty,
        'barDataRow': barDataRow,
        'barDataColum': barDataColum
    })


def companyStatus(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    defaultType = '不限'
    if request.GET.get('type'):
        defaultType = request.GET.get('type')
    typeList = getCompanyStatusCharData.getPageData()
    technologyRow, technologyColum = getCompanyStatusCharData.getTechnologyData(defaultType)
    companySatusData = getCompanyStatusCharData.getCompanyStatusData()
    return render(request, 'companyStatus.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'defaultType': defaultType,
        'technologyRow': technologyRow,
        'technologyColum': technologyColum,
        'companySatusData': companySatusData
    })


def address(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    defaultAddress = '广州'
    if request.GET.get('address'):
        defaultAddress = request.GET.get('address')
    addressList = getAddressCharData.getPageData()
    salaryList, salaryColum = getAddressCharData.getSalaryData(defaultAddress)
    companyPeopleData = getAddressCharData.getCompanyPeopleData(defaultAddress)
    educationsData = getAddressCharData.getEducationalData(defaultAddress)
    distData = getAddressCharData.getDist(defaultAddress)
    return render(request, 'addressChar.html', {
        'userInfo': userInfo,
        'addressList': addressList,
        'defaultAddress': defaultAddress,
        'salaryRow': salaryList,
        'salaryColum': salaryColum,
        'companyPeopleData': companyPeopleData,
        'educationsData': educationsData,
        'distData': distData
    })
