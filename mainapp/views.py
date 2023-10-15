from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Database import
from .models import Prod_Plan, Cnc_Proc, Vision

### 클래스 불러오기
from mainapp.pyfiles.cnc_proc.cnc_proc import Cnc_Proc_Model
from mainapp.pyfiles.cast_proc.cast_proc import Cast_Proc_Model
from mainapp.pyfiles.heat_proc.heat_proc import Heat_Proc_Model
from mainapp.pyfiles.vision.vision import Vision_Model

def vision_pass(request) :
    visions = Vision.objects.filter(vision_pred=1).order_by('-vision_id')
    return render(request,
           'mainapp/vision/pass.html',
           {'visions': visions})

def vision_fail(request) :
    visions = Vision.objects.filter(vision_pred=0).order_by('-vision_id')
    return render(request,
           'mainapp/vision/fail.html',
           {'visions': visions})
#----------------------------------------------------------
### 자동화 검사 모델 페이지
def vision_model(request):
    Vision_Model()
    return render(request,
                  "mainapp/vision/vision_model.html",
                  {})

### 자동화 검사 페이지
def detail_vision(request):
    return render(request,
                  "mainapp/vision/detail_vision.html",
                  {})
#----------------------------------------------------------
### cnc 공정 모니터링 모델 페이지
def cnc_proc_model(request):
    Cnc_Proc_Model()
    return render(request,
                  "mainapp/monitoring/cnc_proc_model.html",
                  {})

### cnc 공정 모니터링 페이지
def cnc_proc_monitoring(request):
    return render(request,
                  "mainapp/monitoring/cnc_proc_monitoring.html",
                  {})
    
### 열처리 공정 모니터링 모델 페이지
def heat_proc_model(request):
    Heat_Proc_Model()
    return render(request,
                  "mainapp/monitoring/heat_proc_model.html",
                  {})

### 열처리 공정 모니터링 페이지
def heat_proc_monitoring(request):
    return render(request,
                  "mainapp/monitoring/heat_proc_monitoring.html",
                  {})

### 주조 공정 모니터링 모델 페이지
def cast_proc_model(request):
    Cast_Proc_Model()
    return render(request,
                  "mainapp/monitoring/cast_proc_model.html",
                  {})

### 주조 공정 모니터링 페이지
def cast_proc_monitoring(request):
    return render(request,
                  "mainapp/monitoring/cast_proc_monitoring.html",
                  {})
#----------------------------------------------------------
### 생산 계획 페이지
def detail_planning(request):
    ### 기본 변수
    part_number = request.GET.get("part_no","")
    number = part_number[4:]
    part_plan = Prod_Plan.objects.filter(part_no=part_number)

    ### select box 받아온 변수
    part_date = request.POST.get("part_date","2021-09-13")
    part_date_plan = Prod_Plan.objects.filter(part_no=part_number, plan_date=part_date)[0]
    
    return render(request,
                  "mainapp/planning/detail_planning.html",
                  {"part_number":part_number,
                   "number":number,
                   "part_plan":part_plan,
                   "part_date":part_date,
                   "part_date_plan":part_date_plan})
#----------------------------------------------------------
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
#----------------------------------------------------------
### 메인 페이지
def main(request):
    return render(request,
                  "mainapp/main.html",
                  {})