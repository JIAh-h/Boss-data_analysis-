from django.contrib import admin
from myApp.models import JobInfo, User, History


class JobManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'address', 'jobType', 'educational', 'workExperience', 'workTag', 'salary',
                    'salaryMonth', 'companyTag', 'hrName', 'hrWork', 'practice', 'companyTitle', 'companyAvatar',
                    'companyNature', 'companyStatus', 'companyPeople', 'detailUrl', 'companyUrl', 'dist']
    list_display_links = ['title']
    list_editable = ['address', 'jobType', 'educational', 'workExperience', 'workTag', 'salary',
                     'salaryMonth', 'companyTag', 'hrName', 'hrWork', 'practice', 'companyTitle', 'companyAvatar',
                     'companyNature', 'companyStatus', 'companyPeople', 'detailUrl', 'companyUrl', 'dist']
    list_filter = ['jobType']
    search_fields = ['title']
    readonly_fields = ['id']
    list_per_page = 20
    date_hierarchy = 'createTime'


class UserManager(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'educational', 'workExperience', 'address', 'work', 'avatar', 'createTime']
    list_display_links = ['username']
    list_editable = ['password', 'educational', 'workExperience', 'address', 'work', 'avatar']
    search_fields = ['username']
    readonly_fields = ['id']
    list_per_page = 20
    date_hierarchy = 'createTime'


class HistoryManager(admin.ModelAdmin):
    list_display = ['id', 'user', 'job', 'count']


admin.site.register(JobInfo, JobManager)
admin.site.register(User, UserManager)
admin.site.register(History, HistoryManager)
