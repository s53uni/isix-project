from django.urls import path

from . import views

urlpatterns = [
    ### 자동화 검사 페이지
    # - http://127.0.0.1:8000/inspection/
    path('inspection/', views.detail_inspection),
    
    ### 공정 모니터링 페이지
    # - http://127.0.0.1:8000/monitoring/
    path('monitoring/', views.detail_monitoring),
    
    ### 생산 계획 페이지
    # - http://127.0.0.1:8000/planning/
    path('planning/', views.detail_planning),
    
    ### 기술 소개 - 자동화 검사 페이지
    # - http://127.0.0.1:8000/introduce/inspection/
    path('introduce/inspection/', views.intro_inspection),
    ### 기술 소개 - 공정 모니터링 페이지
    # - http://127.0.0.1:8000/introduce/monitoring/
    path('introduce/monitoring/', views.intro_monitoring),
    ### 기술 소개 - 생산 계획 페이지
    # - http://127.0.0.1:8000/introduce/planning/
    path('introduce/planning/', views.intro_plannning),
    
    ### 메인 페이지
    # - http://127.0.0.1:8000/index/
    path('index/', views.main),
    # - http://127.0.0.1:8000/
    path('', views.main),
]
