from .getPublicData import *
from myApp.models import History
from django.db.models import F
import json


def addHistory(userInfo, jobId):
    hisData = History.objects.filter(user=userInfo, job_id=jobId)
    if len(hisData):
        hisData[0].count = F('count') + 1
        hisData[0].save()
    else:
        History.objects.create(user=userInfo, job_id=jobId, count=1)


def getHistoryData(userInfo):
    data = list(History.objects.filter(user=userInfo).order_by('-count'))

    def map_fn(item):
        item.job.salary = json.loads(item.job.salary)
        item.job.companyPeople = json.loads(item.job.companyPeople)
        item.job.workTag = [tag for tag in item.job.workTag.split('|') if tag]
        if item.job.companyTag != '无':
            tags = json.loads(item.job.companyTag)
            item.job.companyTag = [tag for sublist in tags for tag in
                                   (sublist.split('，') if isinstance(sublist, str) else [sublist])]
        if not item.job.practice:
            item.job.salary = list(map(lambda x: str(int(x / 1000)), item.job.salary))
        else:
            item.job.salary = list(map(lambda x: str(int(x)), item.job.salary))
        item.job.salary = '-'.join(item.job.salary)
        item.job.companyPeople = list(map(lambda x: str(int(x)), item.job.companyPeople))
        item.job.companyPeople = '-'.join(item.job.companyPeople)
        return item

    data = list(map(map_fn, data))
    return data


def removeHistory(hisId):
    his = History.objects.get(id=hisId)
    his.delete()
