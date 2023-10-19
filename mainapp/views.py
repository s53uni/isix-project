from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache

# DB import
from .models import Prod_Plan, Cnc_Proc, Vision

### 클래스 불러오기
from mainapp.pyfiles.cnc_proc.cnc_proc import Cnc_Proc_Model
from mainapp.pyfiles.cast_proc.cast_proc import Cast_Proc_Model
from mainapp.pyfiles.heat_proc.heat_proc import Heat_Proc_Model
from mainapp.pyfiles.vision.vision import Vision_Model

### 인스턴스 전역변수
my_instance = None

#----------------------------------------------------------
### 자동화 검사 fail 페이지
def detail_fail(request):
    # vision_id 받아오기
    vision_id = request.GET.get("vision_id","")
    
    if vision_id != "" :
        # 테이블에서 이미지 가져오기
        vision_tb = Vision.objects.filter(vision_id=vision_id)[0]
    else :
        vision_tb = None
    
    return render(request,
                  "mainapp/vision/detail_fail.html",
                  {"vision_id":vision_id,
                   "vision_tb":vision_tb})

### 자동화 검사 pass 페이지
def detail_pass(request):
    # vision_id 받아오기
    vision_id = request.GET.get("vision_id","")
    
    if vision_id != "" :
        # 테이블에서 이미지 가져오기
        vision_tb = Vision.objects.filter(vision_id=vision_id)[0]
    else :
        vision_tb = None
        
    return render(request,
                  "mainapp/vision/detail_pass.html",
                  {"vision_id":vision_id,
                   "vision_tb":vision_tb})

### 자동화 검사 모델 페이지
def vision_model(request):
    global my_instance

    if my_instance:
        my_instance.stopModel()
        
    # 클래스 인스턴스 생성
    my_instance = Vision_Model()
    my_instance.runModel()
    
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
    global my_instance

    if my_instance:
        my_instance.stopModel()
        
    # 클래스 인스턴스 생성
    my_instance = Cnc_Proc_Model()
    my_instance.runModel()

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
    global my_instance

    if my_instance:
        my_instance.stopModel()
        
    # 클래스 인스턴스 생성    
    my_instance = Heat_Proc_Model()
    my_instance.runModel()

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
    global my_instance

    if my_instance:
        my_instance.stopModel()
        
    # 클래스 인스턴스 생성    
    my_instance = Cast_Proc_Model()
    my_instance.runModel()
    
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
    global my_instance

    if my_instance:
        my_instance.stopModel()
    ### 기본 변수
    part_number = request.GET.get("part_no","")
    part_plan = Prod_Plan.objects.filter(part_no=part_number)

    ### select box 받아온 변수
    part_date = request.POST.get("part_date","2021-09-13")
    part_date_plan = Prod_Plan.objects.filter(part_no=part_number, plan_date=part_date)[0]
    
    return render(request,
                  "mainapp/planning/detail_planning.html",
                  {"part_number":part_number,
                   "part_plan":part_plan,
                   "part_date":part_date,
                   "part_date_plan":part_date_plan})
#----------------------------------------------------------
### 기술 소개 - 자동화 검사 페이지
def intro_vision(request):
    global my_instance

    if my_instance:
        my_instance.stopModel()
    return render(request,
                  "mainapp/introduce/intro_vision.html",
                  {})

### 기술 소개 - 공정 모니터링 페이지
def intro_monitoring(request):
    global my_instance

    if my_instance:
        my_instance.stopModel()
    return render(request,
                  "mainapp/introduce/intro_monitoring.html",
                  {})

### 기술 소개 - 생산 계획 페이지
def intro_plannning(request):
    global my_instance

    if my_instance:
        my_instance.stopModel()
    return render(request,
                  "mainapp/introduce/intro_planning.html",
                  {})
#----------------------------------------------------------
### 메인 페이지
def main(request):
    global my_instance

    if my_instance:
        my_instance.stopModel()
    return render(request,
                  "mainapp/main.html",
                  {})