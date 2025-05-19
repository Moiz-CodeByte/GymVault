from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('gymadmin', 'Gym Admin'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username

class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class GymAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.gym.name}"

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_days = models.IntegerField()
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.gym.name})"

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True)
    # end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
    )

    PAYMENT_STATUS = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    def __str__(self):
        return f"{self.member.user.username} - {self.amount} ({self.status})"

class Locker(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    locker_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    assigned_member = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.locker_number} - {self.gym.name}"
