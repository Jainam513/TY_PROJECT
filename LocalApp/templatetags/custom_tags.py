import json
from django import template
from LocalApp.models import *
register = template.Library()



@register.filter()
def applydiscount(pid):
    data = Service.objects.get(id=pid)
    price = int(data.price) * int(100 - int(data.discount or 0))/100
    return price

@register.filter()
def productimage(pid):
    data = Service.objects.get(id=pid)
    return data.image.url

@register.filter()
def productname(pid):
    data = Service.objects.get(id=pid)
    return data.name

@register.filter()
def productprice(pid):
    data = Service.objects.get(id=pid)
    return data.price

@register.simple_tag()
def producttotalprice(pid, qty):
    data = Service.objects.get(id=pid)
    return int(data.price or 0)

# @register.filter()
# def productstime(pid):
#     data = Service.objects.get(id=pid)
#     return data.product


@register.filter()
def get_product(productli):
    try:
        productli = productli.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        print(myli)
        pro_li = []
        for i, j in myli.items():
            pro_li.append(int(i))
        product = Service.objects.filter(id__in=pro_li)
        print(product)
        return product
    except:
        return None

@register.simple_tag
def get_qty(pro, bookid):
    try:
        book = Booking.objects.get(id=bookid)
        productli = book.product.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        return myli[str(pro)]
    except:
        return 0
    
@register.filter()
def productstime(pid):
    data = Service.objects.get(id=pid)
    return data.stime


@register.filter()
def productdes(pid):
    data = Service.objects.get(id=pid)
    return data.desc


#feedaback

@register.filter()
def reviewname(pid):
    data = Service.objects.get(id=pid)
    return data.name


@register.filter()
def review(pid):
    data = Service.objects.get(id=pid)
    return data.message