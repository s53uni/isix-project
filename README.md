<a name="top"></a>
  
# SaaS 기반 AI 공정 최적화 시스템, ISIX
🏆 2023 BDIA Dev Contest 미래창업가상 수상 🏆
- 구분: 팀 프로젝트
- 기간: 2023년 9월 7일 ~ 2023년 11월 10일

<details>
  <summary>Table of Contents</summary>
  
  1. [프로젝트 팀원](#프로젝트-팀원)
  2. [프로젝트 개요](#프로젝트-개요)
  3. [사용 기술](#사용-기술)
  3. [주요 기능](#주요-기능)
  5. [미리보기](#미리보기)

</details>
<br>

![isix](https://github.com/s53uni/isix-project/assets/142832376/91cc31b7-f455-4dee-9551-f0efd87fe9ae)
<br><br>

## 프로젝트 팀원

<table>
    <tr align="center">
        <td style="width:300px;"><a href="https://github.com/xx-Sommer-xx"><b>김소연</b></a></td>
        <td style="width:300px;"><a href="https://github.com/pikachamps"><b>김현준</b></a></td>
        <td style="width:300px;"><a href="https://github.com/s53uni"><b>박시윤</b></a></td>
        <td style="width:300px;"><a href="https://github.com/rgon26"><b>양현준</b></a></td>
        <td style="width:300px;"><a href="https://github.com/gustn1051"><b>이경현</b></a></td>
        <td style="width:300px;"><a href="https://github.com/Erin-53"><b>최예진</b></a></td>
    </tr>
    <tr align="center">
        <td>안정 범위 모델<br>웹 배포</td>
        <td>자동화 검사 모델<br>BE 개발</td>
        <td>생산 계획 모델<br>FE/BE 개발</td>
        <td>품질 예측 모델<br>웹 배포</td>
        <td>품질 예측 모델<br>Grafana</td>
        <td>안정 범위 모델<br>웹 배포</td>
    </tr>
</table>

<p align="right"><a href="#top">⬆️TOP</a></p>

## 프로젝트 개요
스마트 제조 시장은 2027년까지 연간 13.95% 성장할 것으로 예상되며, 특히 프로세스 분야에서 높은 시장 점유율이 예상된다. 
그러나 국내 스마트 공장은 여전히 혁신의 중간 단계에 머물러 있으며, 중소기업들은 도입 비용과 전문 인력 부족으로 인해 스마트 제조 기술 도입에 어려움을 겪고 있다. 
<br><br>
이 프로젝트의 주된 목적은 AI 기반 데이터 분석을 통한 공정 최적화 SaaS 시스템을 개발하여 제조 공장의 효율성을 높이고, 
중소기업들이 스마트 제조 기술을 보다 쉽게 도입할 수 있도록 지원하는 것이다. 
이를 통해 생산 계획을 수립하고 제조 과정에서의 이상 징후를 조기에 탐지함으로써 기업들이 비용을 절감하고 생산성을 향상시킬 수 있다.
<br><br>

## 사용 기술
### Back-End
* Django
* Grafana
* MySQL

### Front-End
* HTML5
* CSS3
* Javascript

### Cloud-Service
* AWS
* EC2

### Web Architecture
![image](https://github.com/user-attachments/assets/a6b3afbc-d46a-4079-b101-53578630f699)
  
<p align="right"><a href="#top">⬆️TOP</a></p>

## 주요 기능
### 메인 화면
- 서비스에 대한 간략한 소개와 기대효과를 제공한다.
- 기술 소개, 생산 계획, 공정 모니터링, 자동화 검사로 이어지는 메뉴가 있다.
- 각 페이지는 실제 사용 시 고객이 보게 될 화면을 예시 데이터로 구현했다.
- 작업 데이터는 데이터베이스에 저장되며, Grafana를 통해 실시간 모니터링할 수 있다.

### 기술 소개
- 생산 계획, 공정 모니터링, 자동화 검사에 대한 소개가 담겨있다.
  
### 생산 계획
- 부품 5개에 대한 한 달의 생산 계획을 확인할 수 있다.
- LSTM 모델을 활용하여 이전 정보를 장기간 기억하고 긴 시퀀스 데이터를 처리할 수 있다.
- 딥러닝 기반의 모델을 통해 발주 수량을 예측하고 생산 계획을 수립할 수 있다.
  
### 공정 모니터링
- 주조, 열처리, CNC 공정에 대한 모니터링을 제공한다.
- XGBoost 모델을 사용하여 각 특성 값에 기반한 제품 품질을 예측한다.
- RFE 분석을 통해 주요 특성을 도출하고, XGBoost Tree를 기준으로 공정 안정 범위를 설정했다.

### 자동화 검사
- 공정 완료 제품의 실시간 영상을 확인할 수 있다.
- YOLOv5를 사용해 실시간 영상에서 제품을 감지하고 캡처한다.
- CNN을 통해 캡처된 이미지를 양품 또는 불량품으로 예측하고 분류한다.

<p align="right"><a href="#top">⬆️TOP</a></p>

## 미리보기
해당 서비스는 반응형 웹 사이트로, 데스크탑과 모바일에서 실시간 확인 가능
<table>
    <tr align="center">
        <td><b>데스크탑</b></td>
        <td><b>태블릿</b></td>
        <td><b>모바일</b></td>
    </tr>
    <tr align="center">
        <td><img src="https://github.com/s53uni/isix-project/assets/142832376/a2242374-55b1-494f-bd00-8376b5dea835.png"></td>
        <td><img src="https://github.com/s53uni/isix-project/assets/142832376/1055e703-5861-4bd8-b67e-6e9a8c5d92e5.png"></td>
        <td><img src="https://github.com/s53uni/isix-project/assets/142832376/6525fa09-02b8-4f8c-a116-b360bb14c6f4.png"></td>
    </tr>
</table>

<p align="right"><a href="#top">⬆️TOP</a></p>
