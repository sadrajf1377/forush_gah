from wsgiref.validate import validator

from django.core.exceptions import ValidationError
from django.db import models
from user_Module.models import normal_user,user_messages
from django.utils.text import slugify
class colors(models.Model):
    color=models.CharField(verbose_name='رنگ',max_length=30,blank=True,null=True)
    class Meta:
        verbose_name='رنگ'
        verbose_name_plural='رنگ ها'
    def __str__(self):
        return self.color

# Create your models here.
class images(models.Model):
    picture=models.ImageField(upload_to='product_images')
    product=models.ForeignKey('products',on_delete=models.CASCADE,verbose_name='محصول')

    def __str__(self):

        return self.product.title
    class Meta:
        verbose_name='تصویر محصول'
        verbose_name_plural='تصاویر محصولات'
    def delete(self, using=None, keep_parents=False):
        self.picture.delete()
        super().delete()



class brands(models.Model):
    title=models.CharField(max_length=30,verbose_name='برند کالا')
    def __str__(self):return self.title
    class Meta:
        verbose_name='برند محصول'
        verbose_name_plural='برندهای محصولات'

def product_count_validator(value):
    if value<0:
        raise ValidationError('تعداد محصول نمی تواند منقی باشد!',params={'value':value})
class products(models.Model):
    title=models.CharField(max_length=30,verbose_name='عنوان کالا',null=True,blank=True)
    price=models.IntegerField(verbose_name='قیمت کالا',default=0)
    is_active=models.BooleanField(verbose_name='فعال',default=True)
    add_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت محصول')
    short_description=models.CharField(max_length=100,verbose_name='خلاصه توضیحات',null=True,blank=True)
    main_description=models.TextField(max_length=300,verbose_name='توضیحات اصلی',null=True,blank=True)
    url=models.SlugField(max_length=300,verbose_name='slug_field',null=True,blank=True)
    color=models.ManyToManyField(colors,blank=True,null=True)
    category=models.ForeignKey('product_category',on_delete=models.CASCADE,verbose_name='دسته بندی کالا',null=True)
    brand=models.ForeignKey('brands',on_delete=models.CASCADE,verbose_name='بند محصول',null=True)
    amount_left=models.IntegerField(default=0,verbose_name='تعداد باقی مانده',validators=[product_count_validator])
    rating=models.IntegerField(verbose_name='امتیاز کالا',default=0)


    def chekc_if_ordered(self):
        return self.order_detail_set.filter(parent_order__is_paid=False).exists()
    def load_cooments(self):
        my_list=list(self.comment_set.all())
        return my_list
    def available_colors(self):
        return self.color.all()
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        new_url=self.title.replace('','-')

        self.url=new_url
        amount_changed=False
        old_amount=0
        new_amount=0
        try:
            old_amount=products.objects.get(id=self.id).amount_left
            new_amount=self.amount_left
            amount_changed=True
        except:
            pass
        if amount_changed and self.product_wish_list_set.exists():
            for user in self.product_wish_list_set.first().users.all():
                user_messages.objects.create(reciever_user_id=user.id,message=f'کالای {self.title} موجود شد !').save()



        super().save()
    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'
    def __str__(self):
        return self.title
    def product_images(self):
        return self.images_set.all()
    def thumbnail_photo(self):
        thumbnail_photo=self.images_set.all().first().picture
        return thumbnail_photo


class product_category(models.Model):
    title=models.CharField(verbose_name='دسته بندی',max_length=60,unique=True)
    def __str__(self): return self.title
    class Meta:
        verbose_name='دسته بندی محصول'
        verbose_name_plural='دسته بندی محصولات'

class product_wish_list(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE,null=True,blank=True,editable=False,verbose_name='کالا')
    users=models.ManyToManyField(normal_user,verbose_name='کاربران علاقه مند به این کالا',null=True,blank=True)
    def __str__(self):
        return self.product.title
    class Meta:
        verbose_name='علاقه مندی کالا'
        verbose_name_plural='علاقه مندی های کالا ها'