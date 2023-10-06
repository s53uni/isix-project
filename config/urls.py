from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 각 app들 include하기
    path('', include('mainapp.urls')),
    # 기존 path
    path('admin/', admin.site.urls),
]