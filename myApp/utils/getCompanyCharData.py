from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageData():
    jobs = getAllJob()
    typeData = []
    for i in jobs:
        typeData.append(i.jobType)
    return list(set(typeData))


def getCompanyBar(jobType):
    if jobType == 'all':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(jobType=jobType)
    natureData = {}
    for i in jobs:
        if natureData.get(i.companyNature, -1) == -1:
            natureData[i.companyNature] = 1
        else:
            natureData[i.companyNature] += 1
    natureData = sorted(natureData.items(), key=lambda x: x[1], reverse=True)
    rowData = []
    columData = []
    for k, v in natureData:
        rowData.append(k)
        columData.append(v)
    return rowData[:30], columData[:30]


def getCompanyPie(jobType):
    if jobType == 'all':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(jobType=jobType)
    addressData = {}
    for i in jobs:
        if addressData.get(i.address, -1) == -1:
            addressData[i.address] = 1
        else:
            addressData[i.address] += 1
    result = []
    for k, v in addressData.items():
        result.append({'name': k, 'value': v})
    return result


def getCompanyPeople(jobType):
    if jobType == 'all':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(jobType=jobType)

    def map_fn(item):
        item.companyPeople = json.loads(item.companyPeople)[1]
        return item

    jobs = list(map(map_fn, jobs))
    data = [0 for x in range(6)]
    for i in jobs:
        p = i.companyPeople
        if p <= 20:
            data[0] += 1
        elif p <= 100:
            data[1] += 1
        elif p <= 500:
            data[2] += 1
        elif p <= 1000:
            data[3] += 1
        elif p < 10000:
            data[4] += 1
        else:
            data[5] += 1
    return companyPeople, data
