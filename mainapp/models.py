from django.db import models

from django.db.models.fields import CharField, TextField, DateTimeField, BigIntegerField, FloatField
from django.db.models.fields import IntegerField
from django.db.models import FileField


# <클래스가 만들어진 후 매핑 작업 수행하기>
# python manage.py makemigrations mainapp
# python manage.py migrate


# 회원정보 테이블 매핑
class Member(models.Model) :
    
    mem_id =  CharField(primary_key=True,
                        max_length=20, null=False)
    mem_pass = CharField(max_length=15, null=False)
    mem_com = CharField(max_length=20, null=False)
    mem_plan = IntegerField(null=False)
    mem_monitor = IntegerField(null=False)
    mem_vision = IntegerField(null=False)

    # 내부 클래스 정의 : 메타클래스
    class Meta :
        managed = False
        db_table = "member"


### 생산계획 테이블
class Prod_Plan(models.Model):
    
    part_no =  CharField(primary_key=True, max_length=15)
    plan_date = CharField(max_length=15)
    plan_0day = IntegerField()
    plan_1day = IntegerField()
    plan_2day = IntegerField()
    plan_3day = IntegerField()
    plan_4day = IntegerField()
    plan_5day = IntegerField()
    plan_6day = IntegerField()
    plan_7day = IntegerField()

    class Meta:
        managed = False
        db_table = 'prod_plan'

### CNC 공정 테이블    
class Cnc_Proc(models.Model):
    
    cnc_id =  CharField(primary_key=True, max_length=15)
    cnc_date = DateTimeField()
    SpindleSpeed_max = IntegerField()
    Servocurrent_mean = IntegerField()
    SpindleLoad_max = IntegerField()
    SpindleSpeed_mse = IntegerField()
    SpindleSpeed_mse = IntegerField()
    Servocurrent_mse = IntegerField()
    cnc_pred = IntegerField()

    class Meta:
        managed = False
        db_table = 'cnc_proc'

### Vision 테이블  
class Vision(models.Model):
    
    vision_id = TextField(primary_key=True)
    vision_date = TextField()
    vision_pred = BigIntegerField()
    vision_acc = FloatField()
    vision_img = FileField(upload_to='images/')
    
    def __str__(self):
        return self.vision_id
    
    class Meta:
        managed = False
        db_table = 'vision'