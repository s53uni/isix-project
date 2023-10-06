from django.shortcuts import render
from django.http import HttpResponse


### main 메인 페이지
def main(request):
    return render(request,
                  "mainapp/main.html",
                  {})