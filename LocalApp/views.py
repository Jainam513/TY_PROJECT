from collections import UserList
# from http import client
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from django.contrib.auth import authenticate, login, logout
from OnlineService.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from .models import *
from .models import  WPay
import uuid
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def drak(request):
    return render(request,"dark.html")


def nav(request):
    return render(request, 'navigation.html')


def about(request):
    return render(request, 'about.html')

def worker_about(request):
    return render(request,"worker_about.html")

def conc(request):
    if request.method=="POST":
        contact=Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        contact.name = name
        contact.email =email
        contact.subject=subject
        contact.save()
        messages.success(request,"Your Message sent successfully")
        # return HttpResponse('Thank You For Contact US')
    return render(request,"worker_conc.html")

def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)

def adminHome(request):
    return render(request, 'admin_base.html')

def admin_dashboard(request):
    user = Customer.objects.filter()
    category = Category.objects.filter()
    product = Service.objects.filter()
    new_order = Booking.objects.filter(status=1)
    # dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    done_order = Booking.objects.filter(status=5)
    # return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())



def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        msg = "Category added"
        messages.success(request,'Category Successfully Added')
        return redirect('view_category')
    return render(request, 'add_category.html', locals())

def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
        messages.success(request,'Category Update')
        return redirect('view_category')
    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category')


def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        stime = request.POST['stime']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Service.objects.create(name=name, price=price, category=catobj, desc=desc, image=image,stime=stime)
        messages.success(request, "Service added")
    return render(request, 'add_product.html', locals())

def view_product(request):
    product = Service.objects.all()
    return render(request, 'view_product.html', locals())

def edit_product(request, pid):
    product = Service.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        stime=request.POST['stime']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Service.objects.filter(id=pid).update(name=name, price=price,  category=catobj, desc=desc,stime=stime)
        messages.success(request, "Product Updated")
    return render(request, 'edit_product.html', locals())

def delete_product(request, pid):
    product = Service.objects.get(id=pid)
    product.delete()
    messages.success(request, "Service Deleted")
    return redirect('view_product')



def worker_Login(request):
    if request.method == "POST":
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(username=uname,password=pwd)
        if user:
            try:
                user1 = Worker.objects.get(user=user)
                if user1.status!="Pending":
                    login(request,user)
                    messages.success(request,"Login Successfully.")
                    return redirect(workerHome)
                else:
                    messages.success(request,"Your Login status is Pending, Please Try after some time.")
            except:
                messages.success(request,"Invalid Login.")
        else:
            messages.success(request,"Invalid Login.")

    return render(request,"worker_login.html")



def workerReg(request):
    error = ""
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        professional = request.POST['professional']
        image = request.FILES['image']
        imgs = request.FILES['imgs']
        email = request.POST['email']
        phoneNumber = request.POST['phoneNumber']
        address = request.POST['address']
        if User.objects.filter(email=email).exists():
            messages.warning(request,"This Email id Is already Register")
            return redirect(workerReg)
        else:
            try:
                user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=pwd,email=email)
                auth_token = str(uuid.uuid4())
                
                worker = Worker.objects.create(user=user,mobile=phoneNumber,image=image,imgs=imgs,professional=professional,address=address,status="Pending",type="worker",auth_token=auth_token)
                

                print(auth_token)
                worker.save()

                send_mail(
                    'You need to verify your account',
                    f'Paste the given link to continue  http://127.0.0.1:8000/verify/{auth_token}',
                    from_email = 'ty.test.3112@gmail.com',
                    recipient_list = [user.email,],
                    fail_silently=False,


                )
                return render(request,'token_send.html',locals())

            except:
                # messages.success(request,"error")
                pass
    return render(request,"worker_reg.html")

def w_success(request):
    return render(request,"email_success.html")

def token_send(request):
    return render(request,"token_send.html")

def verify(request,auth_token):
    try:
        worker = Worker.objects.filter(auth_token = auth_token).first()
        if worker:
            if worker.is_verified:
                messages.success(request," Your Account is already Verified..")
                return redirect('/worker_Login')
            worker.is_verified = True
            worker.save()
            messages.success(request," Congralutions!! Your Account is Verified..")
            return redirect('/worker_Login')
        else:
            return redirect('/error')
    except:
        pass

def error(request):
    return render(request,'error.html',locals())





def workerHome(request):
    if not request.user.is_authenticated:
        return redirect('worker_Login')
    return render(request, 'workerHome.html')

# admin_dashboard ma worker show karava
def manage_worker(request):
    worker = Worker.objects.all()
    pending = Worker.objects.filter(status="Pending")
    return render(request,'manage_worker.html',locals())


def pending_worker (request): 
    pending = Worker.objects.filter(status="Pending")
    d = {'pending': pending}
    return render(request, 'pending_worker.html',d)


def accept_worker(request):
    accept = Worker.objects.filter(status="Accept")
    d = {'accept': accept}
    return render(request, "worker_accept.html",d)



def all_worker(request):
    worker = Worker.objects.all()
    pending = Worker.objects.filter(status="Pending")
    return render(request, 'manage_worker.html', locals())


#change status of worker
def change_status(request,pid):
    # if not request.user.is_authenticated:
    #     return redirect('worker_Login')
    error=""
    data = Worker.objects.get(id=pid)
    if request.method=="POST":
        s = request.POST['status']
        data.status=s
        try:
            if s=="Accept":
                send_mail(
                    'status updated',
                    f'Now Your status Is update so you can login',
                    from_email='dhruvidabhi512@gmail.com',
                    recipient_list=[data.user.email,],
                    fail_silently=False,
                )
                data.save()
                error="No"
        except:
            error="Yes"
    d = {'data':data,'error':error}
    return render(request,"change_status.html",d)

def delete_worker(request,wid):
    worker = Worker.objects.get(id=wid)
    worker.delete()
    messages.success(request,"Worker Deleted Successfully")
    return redirect('manage_worker')

# cotacts us
def contact(request):
    if request.method=="POST":
        contact=Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        contact.name = name
        contact.email =email
        contact.subject=subject
        contact.save()
        messages.success(request,"Your Message sent successfully")
        # return HttpResponse('Thank You For Contact US')
    return render(request,'Contactus.html')

#singup







def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'login.html', locals())




#Profile User
def profile(request):
    # try:
        data = Customer.objects.get(user=request.user)
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            address = request.POST['address']
            mobile = request.POST['mobile']
            # image = request.FILES['image']

            try:
                # image = request.FILES['image']
                # data.image = image
                # data.save()
                pass
            except:
                pass
            user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
            Customer.objects.filter(id=data.id).update(mobile=mobile, address=address)
            messages.success(request, "Profile updated")
            return redirect('profile')
        return render(request, 'profile.html', locals())
    # except:
    #     pass
    
    
    # return render(request, 'profile.html', locals())



#worker profile

def worker_profile(request):
    # try:
        data = Worker.objects.get(user=request.user)
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            address = request.POST['address']
            mobile = request.POST['mobile']
            # image = request.FILES['image']

            try:
                image = request.FILES['image']
                data.image = image
                data.save()
                pass
            except:
                pass
            user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname,email=email)
            Worker.objects.filter(id=data.id).update(mobile=mobile, address=address)
            messages.success(request, "Profile updated")
            return redirect('worker_profile')
        return render(request, 'worker_profile.html', locals())
    # except:
    #     pass

#User LOGOUT
def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')

#USer  Change Password
def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')




#services

def user_product(request,pid):
    if pid == 0:
        product = Service.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Service.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "service.html", locals())

def worker_product(request,pid):
    if pid == 0:
        product = Service.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Service.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "worker_service.html", locals())




def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        # image = request.FILES['image']
        if User.objects.filter(email=email).exists():
            messages.warning(request,"This Email id Is already Register")
        else:
            user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
            Customer.objects.create(user=user, mobile=mobile, address=address)
            mydict = {'username': email}
            user.save()
            html_template = 'register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome to Service-Verse'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            messages.success(request, "Registeration Successful")

            return redirect("userlogin")
            # messages.success(request,"Now You Can Add the Service In Cart")
            # return redirect('userlogin')
            

    return render(request, 'registration.html', locals())

#for new page 
def product_detail(request, pid):
    try:
        product = Service.objects.get(id=pid)
        latest_product = Service.objects.filter().exclude(id=pid).order_by('-id')[:10]
        return render(request, "product_detail.html", locals())
    except:
        pass

def addToCart(request, pid):
    myli = {"objects":[]}
    if not request.user.is_authenticated:
        messages.success(request,"Please Login")
        return redirect('registration')
    try:
            cart = Cart.objects.get(user=request.user)
            myli = json.loads((str(cart.product)).replace("'", '"'))
            try:
                myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
            except:
                myli['objects'].append({str(pid):1})
            cart.product = myli
            cart.save()
    except:
            myli['objects'].append({str(pid): 1})
            cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')



 


def cart(request):
    try:
        try:
            cart = Cart.objects.get(user=request.user)
            product = (cart.product).replace("'", '"')
            myli = json.loads(str(product))
            product = myli['objects'][0]
        except:
            product = []
        lengthpro = len(product)
        return render(request, 'cart.html', locals())
    except:
        pass
    
    return render(request, 'cart.html', locals())



def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        services = Service.objects.filter(name__contains=searched)
        # name=searched
        d = {'searched':searched ,'services':services}
        return render(request,"search.html",d)
    else:
        return render(request,"search.html",locals())
    
    
    


def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')


def booking(request):
    error=""
    # RAZORPAY_API_KEY = 'rzp_test_cXsDgODG1MSNjr'
    # RAZORPAY_API_SECRET_KEY='MQi2EvnUWp4dVLpjH8eGrTR9'
    client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
    email = Customer.objects.get(user=request.user)
    user = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Service.objects.get(id=i)
        total = product.price 
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects':[]}
        print(total)
        razorpay_amount = int(total) * int(100)
        # print(order_amount)
        print(product.price)
        order_currency = 'INR'
        payment_order = client.order.create(dict(amount=razorpay_amount, currency=order_currency,payment_capture='1'))
        payment_order_id = payment_order['id']
        callback_url = '/success/'
        print(total)
        context = {
        'amount' :razorpay_amount, 'api_key':RAZORPAY_API_KEY, 'order_id':payment_order_id, 'callback_url':callback_url
        }
        cart.save()
        print(context)
        # messages.success(request, "Click Pay Button to Book Service")
        send_mail(
            'Payment Verification',
            'Your Payment For Order id is Done Successfully.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email,],
            fail_silently=False,
        )
        return render(request, 'payment.html',context)
    else:
        return render(request, "booking.html", locals())



@csrf_exempt
def successs(request):
    return render(request,"successs.html")


def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())


def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 


def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())


#change order
def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

#mange user

def manage_customer(request):
    customer = Customer.objects.all()
    return render(request,'manage_user.html',locals())

def user_feedback(request):
    try:
        user = Customer.objects.get(user=request.user)
        if request.method == "POST":
            Feedback.objects.create(user=request.user, message=request.POST['feedback'])
            messages.success(request, "Feedback sent successfully")
        return render(request, "feedback-form.html", locals())
    except:
        pass
    return render(request, "feedback-form.html", locals())
    


def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())


def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage_feedback')

def read_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def worker_feedback(request):
    user = Worker.objects.get(user=request.user)
    if request.method == "POST":
        Worker_Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "worker_feedback.html", locals())

def manage_worker_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Worker_Feedback.objects.filter(status=int(action))
    return render(request, 'manage_worker_feedback.html', locals())

def read_wfeedback(request, pid):
    feedback = Worker_Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def delete_feedback(request, pid):
    feedback = Worker_Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return render(request, 'manage_worker_feedback.html', locals())


def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')



#worker get emil
def Workergetsms(request,):
    try:
        if request.method == 'POST':
            message = request.POST['message'] 
            email = request.POST['email']
            name = request.POST['name'] 
            #    phonenumber = request.POST['phonenumber']      
            #    emailname = request.POST['emailname']
            send_mail(
                'Contact Form',
                message,
                'settings.EMAIL_HOST_USER',
                    [email],
                fail_silently=False
            )
        return render(request,'Workergetsms.html')
    except:
        pass
    
    return render(request,'Workergetsms.html') 
    



#mange_order
def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 


def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))


def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals()) 









def review(request):
    return render(request, 'review.html')



# # worker Payment
# def workerpay(request):
#     try:
#         if request.method == "POST":
#             payemail = request.POST.get('payemail')
#             payname = request.POST.get("payname")
#             amount = int(request.POST.get("amount"))*100
#             client = razorpay.Client(auth=("rzp_test_cXsDgODG1MSNjr","MQi2EvnUWp4dVLpjH8eGrTR9"))
#             payment=client.order.create({'amount':amount, 'currency':"INR", 'payment_capture':'1'})
#             print(payment)
#             # wpay = WPay(payemail = payemail, payname=payname , amount=amount,payment_id = payment['id'])
#             return render(request,'workerpayment.html',{'payment' :payment})
#             print(wname,amount)
#     except:
#         pass
#     return render(request,'workerpayment.html')


# worker Payment
def workerpay(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        amount = int(request.POST.get("amount"))*100
        client = razorpay.Client(auth=("rzp_test_I9DANSLk2wH5Ib","F60ZYATM2RmiaMU4ptOOIpGx"))
        payment = client.order.create({'amount':amount, 'currency':"INR", 'payment_capture':'1'})
        print(payment)
        wpay = WPay(email = email ,name = name , amount = amount/100 , payment_id = payment['id'])
        # print(wpay)
        wpay.save()
        return render(request,'workerpayment.html',{'payment' :payment})     
    
    return render(request,'workerpayment.html')



@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id =""
        for key ,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
            print(order_id)
        user = WPay.objects.filter(payment_id=order_id).first()
        user.paide = True
        user.save()
        
        msg_plain =render_to_string('email.txt')
        msg_html = render_to_string('emailpay.html')
        
        send_mail("Your PAyment IS done", msg_plain , settings.EMAIL_HOST_USER,
                  [user.email] , html_message = msg_html)
        
    return render(request,'success.html')

def assign_task(request):
    worker = Worker.objects.all()
    # order = Booking.objects.get(id=pid)
    # customer = Customer.objects.filter(address=address) 
    if request.method == "POST":
        pro = request.POST['category']
        oid = request.POST['order']
        name = request.POST['name']
        add = request.POST['add']
        email = request.POST['email']
        
        # temp.objects.create(name=name,add=add)


        # d = {'oid':oid,'name':name,'add':add,'pro':pro}
        d = {'name':name,'add':add}

        send_mail(
            'Assign an Service',
            f'Your Service Details  Your Order ID is : {oid} Username is : {name} Address : {add}',
            from_email = 'ty.test.3112@gmail.com',
            recipient_list = [email,],
            fail_silently=False,
        )

        messages.success(request,'E-mail sent Successfully')

        # return render(request,"w_order.html",d)
        # return redirect('w_order',d)
    return render(request,"assign_task.html",{'worker':worker})
