# MLFYM | Music Lists for Your Mood

> 딥러닝을 활용한 얼굴 감정인식 기반 음악 추천서비스의 웹 및 기술구현 파트 정리에 대한 내용입니다.



## 📽 프로젝트 소개

> MLFYM 의 데이터 수집 부터 전처리, 모델링, 웹 구현에 대한 전반적인 소개 입니다. 

### (1) 프로젝트의 전체 구조

1. 얼굴 감정 인식 및 분류 구조

   ![감정 인식 기반 아키텍처](https://user-images.githubusercontent.com/58945760/85095244-cd8b0780-b22b-11ea-9257-9d11c64e1713.PNG)

2. 음악 추천 시스템 구현 구조

   ![음악 추천 알고리즘](https://user-images.githubusercontent.com/58945760/85095248-cf54cb00-b22b-11ea-8e15-d4bd3f423bd8.PNG)



### (2) 프로젝트 시연 영상

1. 얼굴 감정 분류

   ![ezgif com-resize](https://user-images.githubusercontent.com/58945760/85095083-63726280-b22b-11ea-9521-2627c2a4243f.gif)

2. default Playlist => 질문지 & 선택지 => 추천알고리즘

   ![ezgif com-resize (1)](https://user-images.githubusercontent.com/58945760/85095111-72591500-b22b-11ea-8b10-c4a40e9b627e.gif)

3. default Playlist => 추천 알고리즘

   ![ezgif com-resize (2)](https://user-images.githubusercontent.com/58945760/85095132-843ab800-b22b-11ea-8f18-5be25d28fefe.gif)



## 프로젝트 목표

#### 쉽고 편리한 사용경험

- 앱을 다운로드 받지 않고도 바로 사용해볼 수 있도록 반응형 웹을 구축했습니다.
- 서비스 구성을 쉽고 간편하게 하여 이용자들이 직관적으로 이용하도록 구축했습니다.

#### 색다른 고객경험 제시

- 기존 스트리밍 서비스의 추천 시스템에서 사용하지 않았던 방식을 사용하여 고객에게 새로운 경험을 제시합니다.



## Team Members

|        ID         |  Name  |             Github              |
| :---------------: | :----: | :-----------------------------: |
|  **@dannylee93**  | 이동규 |  https://github.com/dannylee93  |
| **@WinterBlue16** | 이경희 | https://github.com/WinterBlue16 |
|   **@kimjis92**   | 김지승 |   https://github.com/kimjis92   |



## Directory Structure

```shell
# MLFYM
├── 📂 multifinal
└── 📂 media
└── 📂 mlfu
    ├── 📂 data
    ├── 📂 migrations
    ├── 📂 MLFYM
    ├── 📂 phantomjs.2.1.1-windows
    ├── 📂 static
    ├── 📂 templates
    |   ├── 📄 admin.py
    |   ├── 📄 apps.py
    |   ├── 📄 face_functions.py
    |   ├── 📄 forms.py
    |   ├── 📄 google_scraping.py
    |   ├── 📄 haarcascade_frontface.xml
    |   ├── 📄 MobileNetV2(full).h5
    |   ├── 📄 Model_ALS.pkl
    |   ├── 📄 models.py
    |   ├── 📄 music_recommend_system.py
    |   ├── 📄 R_data.npz
    |   ├── 📄 tag2vec.model
    |   ├── 📄 views.py
    |   └── 📄 ...
    ├── 📂 multifinal
    |   ├── 📄 settings.py
    |   ├── 📄 urls.py
    |   └── 📄 wsgi.py
    ├── 📂 statuc
    |   ├── 📄 db.sqlite3
    |   ├── 📄 ghostdriver.log
    |   ├── 📄 manage.py
    |   └── 📄 requirements.txt
```



## ⚙ Tech Stack

![KakaoTalk_20200619_124911264](https://user-images.githubusercontent.com/58945760/85095315-f7dcc500-b22b-11ea-9b78-946b8fc8dd29.png)



## 🏛 Service Architecture

> MLFYM의 대표적인 기능인 음악 추천 기능에 대한 아키텍처 설명입니다. 
>
> '서비스 시작 페이지'부터 웹캠을 통하여 이미지 데이터를 받고 분류한 감정에 맞춘 음악을 재생합니다.

![웹 시나리오](https://user-images.githubusercontent.com/58945760/85095289-e5fb2200-b22b-11ea-9b75-79c595329478.PNG)



## 📝 Document

- [프로젝트 기간 동안의 회의록]([https://github.com/WinterBlue16/MultcampusAI_FinalProject/tree/master/Meeting%20log](https://github.com/WinterBlue16/MultcampusAI_FinalProject/tree/master/Meeting log))
- [프로젝트에 대한 전반적인 설명](https://github.com/dannylee93/Emotion-Recognition/blob/master/README.md)
- [기술공유 01. CNN의 아키텍처 스터디 자료](https://github.com/dannylee93/Emotion-Recognition/tree/master/Model)
- [기술공유 02. 음악추천 시스템](https://github.com/dannylee93/Emotion-Recognition/tree/master/Recommender-System)
