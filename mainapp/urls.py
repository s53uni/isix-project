from django.urls import path

from . import views

urlpatterns = [
    ### 자동화 검사 페이지
    # - http://127.0.0.1:8000/vision/
    path('vision/', views.detail_vision),
    
    ### cnc - 공정 모니터링 페이지
    # - http://127.0.0.1:8000/monitoring/cnc_proc
    path('monitoring/cnc_proc', views.cnc_proc_monitoring),
    ### 열처리 - 공정 모니터링 페이지
    # - http://127.0.0.1:8000/monitoring/heat_proc
    path('monitoring/heat_proc', views.heat_proc_monitoring),
    ### 주조 - 공정 모니터링 페이지
    # - http://127.0.0.1:8000/monitoring/cast_proc
    path('monitoring/cast_proc', views.cast_proc_monitoring),
    
    ### 생산 계획 페이지
    # - http://127.0.0.1:8000/planning/
    path('planning/', views.detail_planning),
    
    ### 기술 소개 - 자동화 검사 페이지
    # - http://127.0.0.1:8000/introduce/vision
    path('introduce/vision', views.intro_vision),
    ### 기술 소개 - 공정 모니터링 페이지
    # - http://127.0.0.1:8000/introduce/monitoring
    path('introduce/monitoring', views.intro_monitoring),
    ### 기술 소개 - 생산 계획 페이지
    # - http://127.0.0.1:8000/introduce/planning
    path('introduce/planning', views.intro_plannning),
    
    ### 메인 페이지
    # - http://127.0.0.1:8000/index/
    path('index/', views.main),
    # - http://127.0.0.1:8000/
    path('', views.main),
]
