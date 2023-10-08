from django.urls import path

from . import views

urlpatterns = [
    ### 기술 소개 페이지
    # - 자동화 검사 페이지
    # - http://127.0.0.1:8000/intro/inspection/
    path('intro/inspection/', views.intro_inspection),
    # - 공정 모니터링 페이지
    # - http://127.0.0.1:8000/intro/monitoring/
    path('intro/monitoring/', views.intro_monitoring),
    # - 생산 계획 페이지
    # - http://127.0.0.1:8000/intro/planning/
    path('intro/planning/', views.intro_plannning),
    
    ### 메인 페이지
    # - http://127.0.0.1:8000/index/
    path('index/', views.main),
    # - http://127.0.0.1:8000/
    path('', views.main),
]
