"""OnlineServices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from razorpay import Payment
from LocalApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('nav/',nav,name="navigation"),
    path('about/', about, name="about"),
    path('admin-login/', adminLogin,name="admin_login"),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),
    path('add-product/', add_product, name='add_product'),
    path('view-product/', view_product, name='view_product'),
    path('edit-product/<int:pid>/', edit_product, name="edit_product"),
    path('delete-product/<int:pid>/', delete_product, name="delete_product"),
    #path('main/', main, name="main"),
    
     # worker login nd reg, home page
    path('worker_Login/',worker_Login,name="worker_Login"),
    path('workerReg',workerReg,name="workerReg"),
    path('workerHome',workerHome,name="workerHome"),

    # show worker
    path('manage_worker',manage_worker,name="manage_worker"),
    path('pending_worker',pending_worker,name="pending_worker"),
    path('accept_worker',accept_worker,name="accept_worker"),
    path('all_worker',all_worker,name="all_worker"),
    #chnage status
    path('change_status/<int:pid>',change_status,name="change_status"),
    path('delete_worker/<int:wid>/', delete_worker, name="delete_worker"),


 #contact us
     path('contact/',contact,name="contact"),
     path('user-feedback/', user_feedback, name="user_feedback"),
     path('manage-feedback/', manage_feedback, name="manage_feedback"),
     path('delete-feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
     path('feedback-read/<int:pid>/', read_feedback, name="read_feedback"),
    #couster
    
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    # path('profile/', profile, name="profile"),
    path('profile/', profile, name="profile"),
    path('logout/', logoutuser, name="logout"),
    path('change-password/', change_password, name="change_password"),
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('my-order/', myOrder, name="myorder"),
    path('drak/',drak,name="dark"),
    path('search',search,name="search"),
    path('booking/', booking, name="booking"),
    path('successs/',successs,name="successs"),
    path('manage_customer/',manage_customer,name="manage_customer"),
    path('manage-order/', manage_order, name="manage_order"), 
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
    path('Workergetsms/',Workergetsms,name='Workergetsms'),
    
    #Eamil Reset
    #emailpasswordreset
    
     path('reset_password',auth_views.PasswordResetView.as_view(),name='reset_password'),
     path('reset_password_send',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),     
      path('reset_password_complate',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
        
    #admin manage order
     path('manage-order/', manage_order, name="manage_order"), 
     path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    
    
    # path('payment/', payment, name="payment"), 
    path('review/',review,name="review"),
    
    #worker Payment
    path('workerpay/',workerpay,name="workerpay"),
    path('success/',success,name="success"),

     path('W_success',w_success,name="w_success"),
    #token for email
    path('token_send',token_send,name="token_send"),

    path('verify/<auth_token>',verify,name="verify"),

    path('error',error,name="error"),

    path('worker_about/',worker_about,name="worker_about"),
    path('conc/',conc,name="conc"),
    path('worker_product/<int:pid>/',worker_product,name="worker_product"),
    path('worker_profile/',worker_profile,name="worker_profile"),
    path('worker_feedback/', worker_feedback, name="worker_feedback"),
    path('manage_worker_feedback/',manage_worker_feedback,name="manage_worker_feedback"),
    path('delete_feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    path('read_wfeedback/<int:pid>/', read_wfeedback, name="read_wfeedback"),

    path('assign_task/',assign_task,name="assign_task"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
