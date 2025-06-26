from myApp.models import User
import hashlib


def changePassword(userInfo, passwordInfo):
    oldPwd = passwordInfo['oldPassword']
    newPwd = passwordInfo['newPassword']
    checkPwd = passwordInfo['checkNewPassword']

    user = User.objects.get(username=userInfo.username)
    md5 = hashlib.md5()
    md5.update(oldPwd.encode())
    oldPwd = md5.hexdigest()
    if user.password != oldPwd:
        return "原密码错误"
    if newPwd != checkPwd:
        return "新密码两次输入不一致"

    md5 = hashlib.md5()
    md5.update(newPwd.encode())
    newPwd = md5.hexdigest()
    user.password = newPwd
    user.save()
