from django.urls import path
from . import views

app_name = 'tramitec'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('doctype/create/', views.doctype_create_view, name='doctype_create'),
    path('doctype/update/<uuid:id>', views.doctype_update_view, name='doctype_update'),
    path('doctype/delete/<uuid:id>', views.doctype_delete_view, name='doctype_delete'),

    path('office/create/', views.office_create_view, name='office_create'),
    path('office/update/<uuid:id>', views.office_update_view, name='office_update'),
    path('office/delete/<uuid:id>', views.office_delete_view, name='office_delete'),

    path('expedient/create/', views.expedient_create_view, name='expedient_create'),
    path('expedient/update/<uuid:id>', views.expedient_update_view, name='expedient_update'),
    path('expedient/list/', views.expedient_list_view, name='expedient_list'),
    path('expedient/generate_expedient_pdf/<str:id>', views.generate_expedient_pdf, name='generate_expedient_pdf'),
    path('expedient/delete/<uuid:id>', views.expedient_delete_view, name='expedient_delete'),
    
    path('receive_expedient/create/', views.receive_expedient_create_view, name='receive_expedient_create'),
    path('receive_expedient/update/<uuid:id>', views.receive_expedient_update_view, name='receive_expedient_update'),
    path('receive_expedient/list/', views.receive_expedient_list_view, name='receive_expedient_list'),
    path('receive_expedient/delete/<uuid:id>', views.receive_expedient_delete_view, name='receive_expedient_delete'),
    path('receive_expedient/route/', views.receive_expedient_route_view, name='receive_expedient_route'),
    
]
