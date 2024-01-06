from django import template
from user_Module.models import normal_user
from product_module.models import products

register=template.Library()
current_user:normal_user=None
@register.filter
def three_digits_currensy(value):

    return '{:,}'.format(value)


@register.filter
def get_user_order(val,user:normal_user):
    result=0
    if val==0:
      try:
          result= user.order_set.filter(is_paid=False).first().order_detail_set.all().count()
      except:
          pass
    elif val==1:
        result =user.order_set.filter(is_paid=False).first().order_detail_set.all()
    elif val==2:

        result=user.order_set.filter(is_paid=False).first().get_total_price()
    elif val==3:
        result=user.order_set.all()
    elif val==4:
        result=user.order_set.filter(is_paid=False).first()

    return result
@register.filter
def check_if_product_is_favoured(product:products,user_id):
    return product.product_wish_list_set.first().users.filter(id=user_id).exists()