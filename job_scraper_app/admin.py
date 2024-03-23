from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Job, User, AttemptedJobs

admin.site.register(Job)
admin.site.register(AttemptedJobs)

# class JobAdmin(admin.ModelAdmin):
#     list_display = ('job_title', 'job_company_name', 'job_location', 'job_id', 'job_level')


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_phone_code', 'user_phone_number', 'user_avatar', 'user_interest')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('user_phone_code', 'user_phone_number', 'user_avatar', 'user_interest'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
