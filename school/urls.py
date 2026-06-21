from django.urls import path
from . import views

urlpatterns = [
    path("resister/",views.school_info , name='school_info'),
    path("register/",views.school_info , name='register'),
    path("show/",views.send , name='show'),
    path("info/",views.show_info , name='link'),
    path("",views.sigin ,name='singin'),
    path('seat/',views.seat ,name='seat'),
    path('parent/',views.parent,name='parent'),
    path('parent_login/',views.parent_login,name='parent_login'),
    path('payment/',views.payment, name='payment')
]
