from django.shortcuts import render
from django.http import HttpResponse

# Database import
from .models import Prod_Plan, Cnc_Proc

### 클래스 불러오기
from mainapp.pyfiles.prod_plan.prod_plan import Prod_Plan_Model
from mainapp.pyfiles.cnc_proc.cnc_proc import Cnc_Proc_Model

### 자동화 검사 페이지
def detail_vision(request):
    return render(request,
                  "mainapp/vision/detail_vision.html",
                  {})
    
    
### cnc 공정 모니터링 페이지
def cnc_proc_monitoring(request):
    
    return render(request,
                  "mainapp/monitoring/cnc_proc_monitoring.html",
                  {})
    
### 열처리 공정 모니터링 페이지
def heat_proc_monitoring(request):
    return render(request,
                  "mainapp/monitoring/heat_proc_monitoring.html",
                  {})

### 주조 공정 모니터링 페이지
def cast_proc_monitoring(request):
    return render(request,
                  "mainapp/monitoring/cast_proc_monitoring.html",
                  {})

### 생산 계획 페이지
def detail_planning(request):
    
    prod_plan = Prod_Plan_Model(6, 3, '2021-09-13 18:30:00')
    y_pred_part_inv = prod_plan.getY_Pred_Part_Inv()
    prods = Prod_Plan.objects.all()
    
    return render(request,
                  "mainapp/planning/detail_planning.html",
                  {"y_pred_part_inv":y_pred_part_inv,
                   "prods":prods})

### 기술 소개 - 자동화 검사 페이지
def intro_vision(request):
    return render(request,
                  "mainapp/introduce/intro_vision.html",
                  {})

### 기술 소개 - 공정 모니터링 페이지
def intro_monitoring(request):
    return render(request,
                  "mainapp/introduce/intro_monitoring.html",
                  {})

### 기술 소개 - 생산 계획 페이지
def intro_plannning(request):
    return render(request,
                  "mainapp/introduce/intro_planning.html",
                  {})

### 메인 페이지
def main(request):
    return render(request,
                  "mainapp/main.html",
                  {})