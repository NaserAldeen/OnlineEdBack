"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from api.views import (CreateLesson,FetchLessonsAndUsers, DeleteClass,SaveClassName, SaveClassDescription, CreateClass, FetchClasses,FetchHistory,FetchCustomerHistory, ChangeOrderStatus, FetchOrders, PlaceOrder, FetchBranches,UserCreateAPIView, UserLoginAPIView, FetchItems, AddItem, DeleteItem, SaveInventory, SaveName, FetchWorkers)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', UserLoginAPIView.as_view()),
    path('signup/', UserCreateAPIView.as_view()),
    # path('fetch_items/', FetchItems.as_view()),
    # path('add_item/', AddItem.as_view()),
    # path('delete_item/', DeleteItem.as_view()),
    # path('save_inventory/', SaveInventory.as_view()),
    # path('save_name/', SaveName.as_view()),
    # path('fetch_workers/', FetchWorkers.as_view()),
    # path('fetch_branches/', FetchBranches.as_view()),
    # path('place_order/', PlaceOrder.as_view()),
    # path('fetch_orders/', FetchOrders.as_view()),
    # path('change_order_status/', ChangeOrderStatus.as_view()),
    # path('fetch_history/', FetchHistory.as_view()),
    # path('fetch_customer_history/', FetchCustomerHistory.as_view()),

    path('fetch_classes/', FetchClasses.as_view()),
    path('create_class/', CreateClass.as_view()),
    path('save_name/', SaveClassName.as_view()),
    path('save_description/', SaveClassDescription.as_view()),
    path('delete_class/', DeleteClass.as_view()),
    path('fetch_lessons_and_students/', FetchLessonsAndUsers.as_view()),
    path('create_lesson/', CreateLesson.as_view()),


]
