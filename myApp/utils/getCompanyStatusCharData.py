from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageData():
    job = []
    jobs = getAllJob()
    for i in jobs:
        job.append(i.jobType)
    return list(set(job))


def getTechnologyData(type):
    if type == '不限':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(jobType=type)
    workTagData = {}
    for job in jobs:
        workTags = [tag.strip() for tag in job.workTag.split('|') if tag.strip()]
        for w in workTags:
            if not w:
                continue
            if w in workTagData:
                workTagData[w] += 1
            else:
                workTagData[w] = 1
    result = sorted(workTagData.items(), key=lambda x: x[1], reverse=True)[:20]
    technologyRow = []
    technologyColum = []
    for k, v in result:
        technologyRow.append(k)
        technologyColum.append(v)
    return technologyRow, technologyColum


def getCompanyStatusData():
    jobs = getAllJob()
    statusData = {}
    for job in jobs:
        if statusData.get(job.companyStatus, -1) == -1:
            statusData[job.companyStatus] = 1
        else:
            statusData[job.companyStatus] += 1
    result = []
    for k, v in statusData.items():
        result.append({
            'name': k,
            'value': v
        })
    return result
