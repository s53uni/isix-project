from django.shortcuts import render
from django.http import HttpResponse



### intro 기술 소개 페이지
def intro(request):
    return render(request,
                  "mainapp/detail/intro.html",
                  {})

### main 메인 페이지
def main(request):
    return render(request,
                  "mainapp/main.html",
                  {})