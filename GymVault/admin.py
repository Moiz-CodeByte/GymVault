from django.contrib import admin

from .models import User, Gym, GymAdmin, MembershipPlan, Member, Payment, Locker
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('username', 'email')



class GymAdminModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym')
    list_filter = ('gym',)
    search_fields = ('user__username', 'gym__name')

class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_in_days', 'gym')
    list_filter = ('gym', 'price')
    search_fields = ('name', 'gym__name')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym', 'membership_plan', )
    list_filter = ('gym', 'membership_plan')
    search_fields = ('user__username', 'user__email', 'gym__name')   
   

class LockerAdmin(admin.ModelAdmin):
    list_display = ('locker_number', 'gym', 'is_available', 'assigned_member')
    list_filter = ('gym', 'is_available')
    search_fields = ('locker_number', 'gym__name')     


admin.site.register(User, UserAdmin)
admin.site.register(Gym)
admin.site.register(GymAdmin, GymAdminModelAdmin)
admin.site.register(MembershipPlan, MembershipPlanAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Payment)
admin.site.register(Locker, LockerAdmin)










