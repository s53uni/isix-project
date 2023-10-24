from django.conf import settings
import django
import os
import tensorflow as tf
from mainapp.pyfiles.vision.yolo_models.models.yolo import Model

import torch
from tensorflow import keras
import cv2
from mainapp.pyfiles.vision.utils.general import non_max_suppression
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
import time


### 자동화 검사 모델
class Vision_Model :
    def __init__(self) :
        # 실행 플래그 초기화
        self.is_running = False
        
    def stopModel(self):
        # 실행 플래그를 False로 설정하여 코드 중지
        self.is_running = False

    def runModel(self) :
        # 실행 플래그를 True로 설정
        self.is_running = True
        
        # MySQL 연결 정보 설정
        db_config = {
            'user': 'root',        # MySQL 사용자 이름
            'password': '0000',    # MySQL 비밀번호
            'host': '127.0.0.1',   # MySQL 호스트 주소
            'database': 'isix',    # MySQL 데이터베이스 이름
            'port': 3306          # MySQL 포트 번호
        }
        # # SQLAlchemy 엔진 생성
        engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

        # MySQL 서버에 연결
        conn = mysql.connector.connect(**db_config)

        # 커서 생성
        cursor = conn.cursor()
        
        # 테이블 존재 여부 확인 쿼리 실행
        find_query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'vision';"
        cursor.execute(find_query)

        # 생성/삭제 쿼리 지정
        create_query = """CREATE TABLE vision (
                            vision_id VARCHAR(30) PRIMARY KEY,
                            vision_date DATETIME,
                            vision_acc FLOAT,
                            vision_img VARCHAR(100),
                            vision_pred INT
                        );"""
        delete_query = "DELETE FROM vision;"

        img_to_draw_temp = ""
        
        if cursor.fetchone():
                # 테이블 이미 존재할 경우 데이터 삭제
                print("테이블 이미 존재함")
                cursor.execute(delete_query)
                conn.commit()
        else:
                # 테이블 없을 경우 테이블 생성
                print("테이블 존재하지 않음")
                cursor.execute(create_query)
                print("테이블 생성 완료")

        # 실행시 기존 이미지 삭제하기
        dir_list = ['mainapp/static/mainapp/pass', 'mainapp/static/mainapp/fail']
        
        try:
            for dir in dir_list :
                for filename in os.listdir(dir):
                    if filename.endswith(".jpg"):
                        file_path = os.path.join(dir, filename)
                        os.remove(file_path)
        except Exception as error:
            print(f"파일 삭제 중 오류 발생: {error}")

        ### 실행 시 동일한 결과를 얻기위한 random seed 설정
        # - 완전히 동일하지는 않음
        tf.keras.utils.set_random_seed(42)

        # - 텐서플로 연산을 고정적으로 만들기
        tf.config.experimental.enable_op_determinism()

        # YOLOv5 모델 초기화
        model = Model('mainapp/pyfiles/vision/yolo_models/models/yolov5s.yaml')  # 'yolov5s.yaml'는 모델 구성 파일의 경로로 바꿔주세요

        # 가중치 파일의 경로
        weights_path = 'mainapp/pyfiles/vision/yolo_models/models/best.pt'  # 불러올 가중치 파일의 경로로 바꿔주세요

        # 가중치 파일 로드
        checkpoint = torch.load(weights_path, map_location='cpu')  # 'cuda' 대신 'cpu'로 변경하여 CPU에서 실행할 수 있도록 합니다.
        
        # 모델에 가중치 로드
        model.load_state_dict(checkpoint['model'].state_dict())
        model.eval()  # 추론 모드로 모델 설정

        # TFLite 모델을 로드합니다.
        interpreter = tf.lite.Interpreter(model_path='mainapp/pyfiles/vision/yolo_models/models/best_cnn_model.tflite')

        # Interpreter를 초기화합니다.
        interpreter.allocate_tensors()
        
        # model_cnn = keras.models.load_model('mainapp/pyfiles/vision/yolo_models/models/best_cnn_model2.h5')
        # model_cnn.summary()

        ## 동영상 1초당 2프레임으로 저장
        cap = cv2.VideoCapture('mainapp/static/mainapp/videos/sample_video.mp4')

        # 코덱 정의
        fourcc = cv2.VideoWriter_fourcc(*'DIVX') # window의 경우 DIVX

        # 프레임 크기, FPS
        width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 파일명, 코덱, 1초당 프레임수, 너비와 넓이 - 동영상 저장
        number = 1
        count_ok = 1 # 프레임 번호 할당
        count_def = 1
        cnt = 1
        prev_box = (0, 0, 0, 0)
        img_to_draw_temp = ""
        
                
        while cap.isOpened():
            ### 외부에서 강제 종료 시키기
            if self.is_running == False:
                break
            
            ret, frame = cap.read()

            if not ret:
                break

            # 일반적으로 1초당 30프레임이 찍혀져 있음. 따라서 %30==0으로 하여 1초에 1프레임 저장
            if(int(cap.get(1)) % 20==0):  # 1초당 1프레임을 jpg로 저장

                # 이미지를 모델의 입력 크기로 조정
                img = cv2.resize(frame, (640, 640))

                # 이미지를 PyTorch 텐서로 변환
                img = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0) / 255.0

                # 모델로부터 예측 수행
                with torch.no_grad():
                    detections = model(img)

                # 후처리: confidence threshold와 iou threshold 적용
                results = non_max_suppression(detections, conf_thres=0.5, iou_thres=0.5)
                if len(results) > 0 and results[0] is not None:
                    results = results[0]
                for det in results:
                    label = int(det[-1])
                    confidence = det[4]
                    box = det[:4]

                    x1, y1, x2, y2 = map(int, box)

                    # 이미지를 시각화하기 전에 다시 원래 형식으로 변환
                    img_to_draw = img[0].permute(1, 2, 0).cpu().numpy()

                    x_ = ((x2 - x1) / 2) + x1
                    y_ = ((y2 - y1) / 2) + y1
                    min_ = 270
                    max_ = 370
                    current_box = x1, y1, x2, y2

                    if np.allclose(current_box, prev_box, atol=1):
                        current_box = prev_box

                    if (cnt >= 2) & (prev_box != current_box):                
                        img_cnn = cv2.resize(img_to_draw_temp, (300, 300))

                        # 데이터 유형을 FLOAT32로 변환
                        img_cnn = np.array(img_cnn, dtype=np.float32)
                    
                        # 배치 차원 추가
                        image_array = np.expand_dims(img_cnn, axis=0)
                        
                        # 모델 입력 텐서의 인덱스를 가져옵니다.
                        input_index = interpreter.get_input_details()[0]["index"]

                        # 모델 출력 텐서의 인덱스를 가져옵니다.
                        output_index = interpreter.get_output_details()[0]["index"]

                        # 입력 데이터를 모델에 전달하고 예측을 수행합니다.
                        interpreter.set_tensor(input_index, image_array)
                        interpreter.invoke()

                        pred_data = interpreter.get_tensor(output_index)
                        
                        # pred_data = model_cnn.predict(image_array)
                        # print(pred_data)

                        if pred_data[0][0] > 0.8:
                            print(f"count_ok[{count_ok}] / 예측값[1] / 예측범주명칭[양품]")
                            vision_id = datetime.now().strftime("%Y%m%d") + "-" + "{:03d}".format(number)
                            
                            cv2.imwrite(f'mainapp/static/mainapp/pass/{vision_id}.jpg', img_to_draw_temp * 255)
                            
                            vision_img = f"{vision_id}.jpg"
                            pred_data
                            
                            vision_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            df_temp = pd.DataFrame({'vision_id': vision_id,
                                'vision_date': vision_date,
                                'vision_pred': 1,
                                'vision_acc': pred_data[0],
                                'vision_img': vision_img})
                            
                            df_temp.to_sql(name="vision", con=engine, if_exists='append', index=False)
                            count_ok += 1
                            number += 1
                            
                            time.sleep(2.5)
                            
                        else :
                            print(f"count_def[{count_def}] / 예측값[0] / 예측범주명칭[불량]")
                            vision_id = datetime.now().strftime("%Y%m%d") + "-" + "{:03d}".format(number)
                            
                            cv2.imwrite(f'mainapp/static/mainapp/fail/{vision_id}.jpg', img_to_draw_temp * 255)
                            
                            # vision_img = f"{os.getcwd()}/fail/{vision_id}.jpg"
                            vision_img = f"{vision_id}.jpg"
                            pred_data
                            
                            vision_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            df_temp = pd.DataFrame({'vision_id': vision_id,
                                'vision_date': vision_date,
                                'vision_pred': 0,
                                'vision_acc': pred_data[0],
                                'vision_img': vision_img})
                            df_temp["vision_date"] = pd.to_datetime(df_temp["vision_date"])
                            
                            df_temp.to_sql(name="vision", con=engine, if_exists='append', index=False)
                            
                            count_def += 1
                            number += 1
                            
                            time.sleep(2.5)


                    if prev_box != current_box :
                        prev_box = current_box
                        cnt = 1

                        break
                    else :
                        img_to_draw_temp = img_to_draw
                        cnt += 1
                        
            if cv2.waitKey(1)& 0xFF == ord('q'): # 0xFF는 win64 환경
                break

        cap.release()
        cv2.destroyAllWindows()
        
        return cap
    
