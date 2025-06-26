from .getPublicData import *
import time
from django.core.paginator import Paginator, EmptyPage


def getNowTime():
    timeFormat = time.localtime()
    yer = timeFormat.tm_year
    mon = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return yer, monthList[mon - 1], day


def getUserCreateTime():
    user = getAllUser()
    data = {}
    for u in user:
        if data.get(str(u.createTime), -1) == -1:
            data[str(u.createTime)] = 1
        else:
            data[str(u.createTime)] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return result


def getTop6User():
    user = getAllUser().order_by('-createTime')[:6]
    result = []
    for u in user:
        result.append({
            'username': u.username,
            'password': u.password,
            'createTime': u.createTime,
            'avatar': u.avatar
        })
    return result


def getAllTag():
    job = getAllJob()
    user = getAllUser()

    # 数据总量和用户数量统计
    job_num = job.count()
    user_num = user.count()

    # 直接获取所有学历并过滤有效值
    existing_educations = job.values_list('educational', flat=True).distinct()
    # 转换为带编号的元组并排序
    education_with_code = [
        (edu, educationList[edu])
        for edu in existing_educations
        if edu in educationList
    ]
    # 获取最高学历（编号最小）
    sorted_educations = sorted(education_with_code, key=lambda x: x[1])
    top_education = sorted_educations[0][0] if sorted_educations else '无数据'

    # 最高薪资
    max_salary = max([eval(job.salary)[1] for job in job])

    # 优势城市
    city_counter = {}
    for j in job:
        addr = j.address.strip()
        if addr:
            city_counter[addr] = city_counter.get(addr, 0) + 1
    sorted_cities = sorted(city_counter.items(), key=lambda x: x[1], reverse=True)
    top_two = [item[0] for item in sorted_cities[:2]]  # 直接返回城市名称列表
    city = '、'.join(top_two)
    # print(job_num, user_num, top_education, max_salary, city)
    return job_num, user_num, top_education, max_salary, city


def getAllJobInfo():
    job = getAllJob()
    result = []
    for j in job:
        # print(j.id, j.title, j.address, j.jobType, j.educational, j.workExperience)
        result.append({
            'id': j.id,
            'title': j.title,
            'address': j.address,
            'jobType': j.jobType,
            'educational': j.educational,
            'workExperience': j.workExperience
        })
        break
    return result


def getAll(page=1, page_size=10):
    # 获取基础查询集
    job_query = getAllJob()

    # 创建分页器
    paginator = Paginator(job_query, page_size)

    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 构建结果集
    result = {
        'jobs': [],
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next()
        }
    }

    # 格式化每个职位数据
    for job in page_obj.object_list:
        job.workTag = [tag for tag in job.workTag.split('|') if tag]
        result['jobs'].append({
            'id': job.id,
            'title': job.title,
            'address': job.address,  # 分割城市和区域
            'jobType': job.jobType,
            'educational': job.educational,
            'workExperience': job.workExperience,
            'workTag': job.workTag,
            'salary': list(map(int, eval(job.salary))),  # 转换为数字列表
            'salaryMonth': job.salaryMonth,
            'practice': job.practice,
            'companyInfo': {  # 公司详细信息
                'title': job.companyTitle,
                'companyTag': job.companyTag,
                'nature': job.companyNature,
                'status': job.companyStatus,
                'people': eval(job.companyPeople),
                'url': job.companyUrl
            },
            'detailUrl': job.detailUrl
        })

    return result


def getDateData():
    jobs = getAllJob()
    # 统计每日数据量
    date_counter = {}
    for job in jobs:
        date_str = job.createTime.strftime('%Y-%m-%d')
        date_counter[date_str] = date_counter.get(date_str, 0) + 1

    # 按日期排序
    sorted_dates = sorted(date_counter.items(), key=lambda x: x[0])

    return {
        'dates': [item[0] for item in sorted_dates],
        'counts': [item[1] for item in sorted_dates]
    }

