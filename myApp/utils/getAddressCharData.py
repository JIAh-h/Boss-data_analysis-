from .getPublicData import *
from myApp.models import JobInfo
import json


def getPageData():
    jobs = getAllJob()
    addressList = []
    for job in jobs:
        addressList.append(job.address)
    return list(set(addressList))


def getSalaryData(address):
    jobs = JobInfo.objects.filter(address=address)
    salaryData = []
    for job in jobs:
        if job.practice == 0:
            salaryData.append(json.loads(job.salary)[1])
    salaryColum = [0 for x in range(len(salaryList))]
    for i in salaryData:
        s = i / 1000
        if s < 10:
            salaryColum[0] += 1
        elif s < 20:
            salaryColum[1] += 1
        elif s < 30:
            salaryColum[2] += 1
        elif s < 40:
            salaryColum[3] += 1
        else:
            salaryColum[4] += 1
    return salaryList, salaryColum


def getCompanyPeopleData(address):
    jobs = JobInfo.objects.filter(address=address)
    companyPeopleData = []
    for job in jobs:
        companyPeopleData.append(json.loads(job.companyPeople)[1])
    companyPeopleColum = [0 for x in range(len(companyPeople))]
    for i in companyPeopleData:
        if i <= 20:
            companyPeopleColum[0] += 1
        elif i < 100:
            companyPeopleColum[1] += 1
        elif i < 500:
            companyPeopleColum[2] += 1
        elif i < 1000:
            companyPeopleColum[3] += 1
        elif i < 10000:
            companyPeopleColum[4] += 1
        else:
            companyPeopleColum[5] += 1
    result = []
    for index, item in enumerate(companyPeopleColum):
        result.append({
            'name': companyPeople[index],
            'value': item
        })
    return result


def getEducationalData(address):
    jobs = JobInfo.objects.filter(address=address)
    educationsData = {}
    for job in jobs:
        if educationsData.get(job.educational, -1) == -1:
            educationsData[job.educational] = 1
        else:
            educationsData[job.educational] += 1
    result = []
    for key, value in educationsData.items():
        result.append({
            'name': key,
            'value': value
        })
    return result


def getDist(address):
    jobs = JobInfo.objects.filter(address=address)
    distData = {}
    for job in jobs:
        if job.dist != '':
            if distData.get(job.dist, -1) == -1:
                distData[job.dist] = 1
            else:
                distData[job.dist] += 1
    result = []
    for key, value in distData.items():
        result.append({
            'name': key,
            'value': value
        })
    return result
