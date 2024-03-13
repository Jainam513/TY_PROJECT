from django.contrib import admin
from .models import Service,Category,Worker,Contact,Customer
from .models import *

# Register your models here


admin.site.register(Service)

admin.site.register(Category)

admin.site.register(Worker)

admin.site.register(Contact)

admin.site.register(Customer)

admin.site.register(Feedback)


admin.site.register(Cart)

admin.site.register(Booking)

admin.site.register(WPay)

admin.site.register(Worker_Feedback)