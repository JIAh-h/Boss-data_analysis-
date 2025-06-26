import json
from .getPublicData import *


def getTableData():
    job = getAllJob()

    def map_fn(item):
        item.salary = json.loads(item.salary)
        item.companyPeople = json.loads(item.companyPeople)
        item.workTag = [tag for tag in item.workTag.split('|') if tag]
        if item.companyTag != '无':
            tags = json.loads(item.companyTag)
            item.companyTag = [tag for sublist in tags for tag in
                               (sublist.split('，') if isinstance(sublist, str) else [sublist])]
        if not item.practice:
            item.salary = list(map(lambda x: str(int(x / 1000)), item.salary))
        else:
            item.salary = list(map(lambda x: str(int(x)), item.salary))
        item.salary = '-'.join(item.salary)
        item.companyPeople = list(map(lambda x: str(int(x)), item.companyPeople))
        item.companyPeople = '-'.join(item.companyPeople)
        return item

    job = list(map(map_fn, job))
    return job

