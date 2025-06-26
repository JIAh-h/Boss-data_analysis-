from .getPublicData import *
import os


def getPageData():
    jobs = getAllJob()
    jobType = {}
    for job in jobs:
        if jobType.get(job.jobType, -1) == -1:
            jobType[job.jobType] = 1
        else:
            jobType[job.jobType] += 1
    return list(educationList.keys()), workExperience, list(jobType.keys())


def changeSelfInfo(newInfo, fileInfo):
    user = User.objects.get(username=newInfo.get('username'))
    old_avatar_path = user.avatar.path if user.avatar else None
    user.educational = newInfo.get('educational')
    user.workExperience = newInfo.get('workExperience')
    user.address = newInfo.get('address')
    user.work = newInfo.get('work')
    if fileInfo.get('avatar') is not None:
        # 新增：删除旧头像文件
        if old_avatar_path and os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)
        user.avatar = fileInfo.get('avatar')
    user.save()
