from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache

# DB import
from .models import Prod_Plan, Cnc_Proc, Vision, Member

### 클래스 불러오기
from mainapp.pyfiles.cnc_proc.cnc_proc import Cnc_Proc_Model
from mainapp.pyfiles.cast_proc.cast_proc import Cast_Proc_Model
from mainapp.pyfiles.heat_proc.heat_proc import Heat_Proc_Model
from mainapp.pyfiles.vision.vision import Vision_Model

### 인스턴스 전역변수
my_instance = None
login_msg = """
            <script type='text/javascript'>
                alert('로그인 후 이용 가능합니다.');
                location.href = '/login';
            </script>
        """
permisson_msg = """
            <script type='text/javascript'>
                alert('접근 권한이 없습니다.');
                location.href = '/';
            </script>
        """
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

### 자동화검사 캡처 이미지
def cap_vision(request):
    try :
        latest_data = Vision.objects.latest('vision_date')
        img = latest_data.vision_img
        passfail = latest_data.vision_pred
    
    except :
        img = None
        passfail = None
        
    return render(request,
                "mainapp/vision/cap_vision.html",
                {"img":img,
                 "passfail":passfail})

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
#----------------------------------------------------------    
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
#----------------------------------------------------------
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

    part_number = request.GET.get("part_no","")
    part_plan = Prod_Plan.objects.filter(part_no=part_number)

    part_dict = {"part6":"헤드 볼트", "part15":"헤드 가스켓",
                    "part16":"크랭크 축", "part29":"클록 스프링",
                    "part94":"벨트 프리텐셔너"}
    part_name = part_dict[part_number]
    
    ### select box 받아온 변수
    part_date = request.POST.get("part_date","2021-09-13")
    part_date_plan = Prod_Plan.objects.filter(part_no=part_number, plan_date=part_date)[0]
    
    return render(request,
                "mainapp/planning/detail_planning.html",
                {"part_number":part_number,
                "part_plan":part_plan,
                "part_name":part_name,
                "part_date":part_date,
                "part_date_plan":part_date_plan})
#----------------------------------------------------------
### 기술 소개 페이지
def detail_intro(request):
    global my_instance

    if my_instance:
        my_instance.stopModel()
    return render(request,
                  "mainapp/introduce/detail_intro.html",
                  {})
#----------------------------------------------------------
### 로그아웃 처리하기
def logout(request):
    
    msg = """
            <script type='text/javascript'>
                alert('로그아웃 되었습니다.');
                location.href = '/';
            </script>
        """
        
    request.session.flush()
    
    return HttpResponse(msg)
#----------------------------------------------------------
### 회원가입 후 페이지
def joinafter(request):
    try :
        mem_id = request.POST.get("mem_id", "")
        mem_pass = request.POST.get("mem_pass", "")
        mem_com = request.POST.get("mem_com", "")
        mem_plan = request.POST.get("mem_plan", 0)
        mem_monitor = request.POST.get("mem_monitor", 0)
        mem_vision = request.POST.get("mem_vision", 0)

        
        Member.objects.create(mem_id=mem_id,
                            mem_pass=mem_pass,
                            mem_com=mem_com,
                            mem_plan=mem_plan,
                            mem_monitor=mem_monitor,
                            mem_vision=mem_vision)
         
    except:
        msg = """
            <script type='text/javascript'>
                alert('정보를 다시 확인해주세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
    
    msg = """
            <script type='text/javascript'>
                alert('가입이 완료되었습니다.');
                location.href = '/login';
            </script>
        """
        
    return HttpResponse(msg)
#----------------------------------------------------------
### 로그인 후 페이지
def loginafter(request):
    try :
        mem_login_id = request.POST.get("mem_login_id","")
        mem_login_pass = request.POST.get("mem_login_pass","")
        
        member = Member.objects.get(mem_id = mem_login_id)
  
        if (member.mem_id == mem_login_id) & (member.mem_pass == mem_login_pass):
            msg = """
                    <script type="text/javascript">
                        alert('정상적으로 로그인 되었습니다.');
                        location.href='/';
                    </script>
            """
            
            request.session["ses_mem_id"] = mem_login_id
            request.session["ses_mem_plan"] = member.mem_plan
            request.session["ses_mem_monitor"] = member.mem_monitor
            request.session["ses_mem_vision"] = member.mem_vision
            
        return HttpResponse(msg)
    
    except :
        msg = """
                <script type="text/javascript">
                    alert('아이디 또는 패스워드를 확인해주세요.');
                    history.go(-1);
                </script>
        """ 
        return HttpResponse(msg)

### 로그인 페이지
def login(request) :
    global my_instance

    if my_instance:
        my_instance.stopModel()
    return render(request,
                  "mainapp/member/login.html",
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