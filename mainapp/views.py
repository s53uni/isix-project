from django.shortcuts import render
from django.http import HttpResponse

### 기술 소개 - 자동화 검사 페이지
def intro_inspection(request):
    return render(request,
                  "mainapp/introduce/intro_inspection.html",
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