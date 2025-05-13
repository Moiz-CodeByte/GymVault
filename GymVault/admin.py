from django.contrib import admin

from .models import User, Gym, GymAdmin, MembershipPlan, Member, Payment, Locker
# Register your models here.
admin.site.register(User)
admin.site.register(Gym)
admin.site.register(GymAdmin)
admin.site.register(MembershipPlan)
admin.site.register(Member)
admin.site.register(Payment)
admin.site.register(Locker)
