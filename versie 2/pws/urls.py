from django.contrib import admin
from django.urls import path, re_path
from .views import *
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/save-nfc/(?P<uid>[\w:\-]+)/$', save_nfc_tag, name='save_nfc'),
    path('', home, name='home'),
    path('api/toggle/<str:uid>/', toggle_aanwezig, name='toggle_aanwezig'),
    path('adjust-balance/', adjust_balance, name='adjust_balance'),

]