from django.contrib.auth.models import AbstractUser
from django.db import models
choices=(('mashhad','مشهد'),('tehran','تهران'),('shiraz','شیراز'),('isfahan','اصهان'),('rasht','رشت'),('sarry','ساری'),
             ('az','یزد'),('mashhad','کرمان'))
# Create your models here.
class normal_user(AbstractUser):
    activation_code=models.CharField(max_length=100,verbose_name='کد فعال سازی',null=True,blank=True)
    phone_number=models.CharField(max_length=20,verbose_name='شماره موبایل',null=True,blank=True)
    email = models.EmailField(max_length=20,verbose_name='ایمیل',null=True,blank=True)
    address=models.TextField(max_length=300,verbose_name='آدرس محل سکونت',null=True,blank=True)
    first_name = models.CharField(max_length=300, verbose_name='نام', null=True, blank=True)
    last_name =models.CharField(max_length=300, verbose_name='نام خانوادگی', null=True, blank=True)
    city=models.CharField(max_length=20,choices=choices, null=True, blank=True,verbose_name='شهر')
    postal_code=models.IntegerField(verbose_name='کد پستی', default=0)
    avatar=models.ImageField(upload_to='profiles',null=True,blank=True,verbose_name='تصویر پروفایل')
    reset_password_code=models.CharField(max_length=100,verbose_name='کد تغییر رمز عبور',default='')

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربرها'

class user_messages(models.Model):
    reciever_user=models.ForeignKey(normal_user,verbose_name='کاربر دریافت کننده پیام',on_delete=models.CASCADE,null=True,blank=True)
    message=models.CharField(verbose_name='متن پیام',max_length=300,blank=True,null=True)
    creation_date=models.DateTimeField(verbose_name='زمان ایجاد پیام',auto_now_add=True,null=True,blank=True)
    ssen_by_user=models.BooleanField(default=False,verbose_name='خوانده شده')
    def __str__(self):
        return self.reciever_user.username
    class Meta:
        verbose_name='پیام به کاربرها'
        verbose_name_plural='پیام ها به کاربرها'