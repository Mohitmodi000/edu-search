from django.urls import path
from . import views

urlpatterns = [
    path("resister/",views.school_info , name='school_info'),
    path("register/",views.school_info , name='register'),
    path("show/",views.send , name='show'),
    path("info/",views.show_info , name='link_fallback'),
    path("info/<int:school_id>/",views.show_info , name='link'),
    path("",views.sigin ,name='singin'),
    path('seat/',views.seat ,name='seat'),
    path('parent/',views.parent,name='parent'),
    path('parent/edit/',views.parent_edit,name='parent_edit'),
    path('parent/change-cover/',views.change_cover,name='change_cover'),
    path('parent/logout/',views.user_logout,name='parent_logout'),
    path('parent_login/',views.parent_login,name='parent_login'),
    path('payment/',views.payment, name='payment')
]
