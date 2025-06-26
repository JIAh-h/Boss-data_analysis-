from .getPublicData import *
import json
from myApp.models import JobInfo


def getPageData():
    return list(educationList.keys()), workExperience


def getBarData(defaultEducation, defaultWorkExperience):
    if defaultEducation == '不限' and defaultWorkExperience == '不限':
        jobs = JobInfo.objects.all()
    elif defaultWorkExperience == '不限':
        jobs = JobInfo.objects.filter(educational=defaultEducation)
    elif defaultEducation == '不限':
        jobs = JobInfo.objects.filter(workExperience=defaultWorkExperience)
    else:
        jobs = JobInfo.objects.filter(educational=defaultEducation, workExperience=defaultWorkExperience)
    jobsType = {}
    for j in jobs:
        if j.practice == 0:
            if jobsType.get(j.jobType, -1) == -1:
                jobsType[j.jobType] = [json.loads(j.salary)[1]]
            else:
                jobsType[j.jobType].append(json.loads(j.salary)[1])
    # print(jobsType)
    barData = {}
    for k, v in jobsType.items():
        if not barData.get(k, 0):
            barData[k] = [0 for x in range(5)]
        for i in v:
            s = i / 1000
            if s < 10:
                barData[k][0] += 1
            elif 10 <= s < 20:
                barData[k][1] += 1
            elif 20 <= s < 30:
                barData[k][2] += 1
            elif 30 <= s < 40:
                barData[k][3] += 1
            else:
                barData[k][4] += 1
    # print(barData)
    legends = list(barData.keys())
    if len(legends) == 0:
        legends = None
    return salaryList, barData, legends


def avg(list):
    total = 0
    for i in list:
        total += i
    return round(total / len(list), 1)


def pieData():
    jobs = getAllJob()
    jobsType = {}
    for j in jobs:
        if j.practice == 1:
            if jobsType.get(j.jobType, -1) == -1:
                jobsType[j.jobType] = [json.loads(j.salary)[1]]
            else:
                jobsType[j.jobType].append(json.loads(j.salary)[1])
    result = []
    for k, v in jobsType.items():
        result.append({
            'name': k,
            'value': avg(v)
        })
    return result


def getFunnelData():
    jobs = JobInfo.objects.filter(salaryMonth__gt=0)
    data = {}
    for j in jobs:
        x = str(j.salaryMonth) + '薪'
        if data.get(x, -1) == -1:
            data[x] = 1
        else:
            data[x] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    # print(result)
    return result
