### 라이브러리
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### 정규화 패키지
from sklearn.preprocessing import StandardScaler

### 모델 관련 패키지
import tensorflow as tf
tf.random.set_seed(42)
from tensorflow.keras.models import load_model
from os import listdir
from sklearn.metrics import mean_absolute_error


### 생산 계획 모델
class Prod_Plan_Model :
    def __init__(self, part, num, date) :
        ### 데이터 가져오기
        data = self.getData(part, num)
        ### 모델 불러오기
        self.getModel(data, part, num, date)
        
    ### 데이터 가져오기
    def getData(self, part, num) :
        ### 데이터 불러오기
        data = pd.read_csv("mainapp/pyfiles/prod_plan/part_data/part{}_data.csv".format(part))
        
        return data
    
    ### 모델 가져오기
    def getModel(self, data, part, num, date) :
        ### 페이지에서 날짜 받아오기
        idx = data.index[(data['CRET_TIME'] == date)]
        idx = 0
        ### 주요 변수 선택 및 저장
        data = data.iloc[:, [1, num+1, num+2, num+3]].reset_index(drop=True)
        
        ### 독립/종속변수 만들기
        lookback = 3
        delay = num
        
        output_len = 1 # N=total_length-(3+3)+1
        n_feature = data.shape[-1] # =4
        
        X_part = np.zeros((1, lookback, n_feature)) # (N,3,4)
        y_part = np.zeros((1,)) # (N,)
        
        X_part[0] = data.iloc[idx:idx+lookback, :]
        y_part[0] = data.iloc[idx+lookback+delay-1, 0]

        ### 데이터 정규화
        Xscaler_part = StandardScaler()
        X_part = Xscaler_part.fit_transform(X_part.reshape(-1, X_part.shape[-1])).reshape(X_part.shape)

        yscaler_part = StandardScaler()
        y_part = yscaler_part.fit_transform(y_part.reshape(-1,1))

        ### 모델 불러오기
        best_model = load_model('mainapp/pyfiles/prod_plan/best_model/part{}_d{}_lstm.h5'.format(part, num))

        ### 예측하기
        y_pred_part = best_model.predict(X_part)
        
        ### 예측값을 기존 값 범위로 역변환
        y_pred_part_inv = yscaler_part.inverse_transform(y_pred_part)
        y_part_inv = yscaler_part.inverse_transform(y_part)
        
        self.y_pred_part_inv = y_pred_part_inv.reshape(1,)[0]
        
    def getY_Pred_Part_Inv(self) :
        
        return self.y_pred_part_inv