# :inbox_tray:데이터 수집

> 얼굴 감정 인식을 기반으로 하는 음악 추천 서비스, 들려듀오는 크게 **감정 분류 모델**과 **음악 추천 알고리즘** 두 부분으로 나눌 수 있다. 사용자의 감정을 제대로 판별하기 위해서는 모델의 정확도를 확보하는 것이 중요하며, 그를 결정하는 주요한 요소는 훈련 데이터의 질과 양이다. 
>
> 모델 훈련을 위해 수집 및 검증한 데이터는 총 3,247만 장으로, 수집 과정은 이하와 같다.



## 1. 검증 데이터 수집

### 1.1 Ai hub K-FACE Dataset

![다운로드](https://user-images.githubusercontent.com/58945760/87050140-d5413900-c238-11ea-8dd0-8bd24692f648.jpg)

![캡처](https://user-images.githubusercontent.com/58945760/87049625-30bef700-c238-11ea-97df-1ed8b98f66f7.PNG)

> 전체 데이터의 70% 이상을 차지한 Main Dataset

- [Ai hub 사이트](http://www.aihub.or.kr/aidata/73)에서 구체적인 데이터 정보를 확인할 수 있으며 [데이터 신청](http://kface.kist.re.kr/#/) 과정을 거쳐 저화질, 중화질, 고화질 데이터를 다운로드할 수 있다.  

- 데이터 신청을 위해서는 K-FACE 공식 홈페이지에 **필수적으로** 가입하여야 한다. 또한 **데이터 활용 계획서**와 **개인정보 동의서**를 별도 제출해야 하며 동의서 내 **소속 기관장의 서명**이 요구된다.  신청 후 승인이 날 때까지는 3~4일 정도가 소요된다. 

- 학술적인 목적에 한해 사용할 수 있으며, 상업적인 용도로는 이용할 수 없다.

- 표정으로 감정을 분류하는 모델을 만드는 만큼 섬세한 얼굴 변화까지 잡아낼 수 있도록 **고화질** 데이터를 신청하여 다운로드하였다. 

- 총 데이터 수는 **3,240만 장**이다. 

  

### 1.2 FFHQ Dataset

![보조데이터](https://user-images.githubusercontent.com/58945760/87051097-17b74580-c23a-11ea-8d07-0633189daced.PNG)

> 보다 정확한 모델 평가와 `overfitting`을 방지하기 위한 Sub Dataset

- [해당 Github](https://github.com/NVlabs/ffhq-dataset)에서 데이터 정보 및 라이센스 관련 사항을 확인할 수 있으며, 데이터는 [Google drive](https://drive.google.com/drive/folders/1tZUcXDBeOibC6jcMCtgRRz67pzrAHeHL?usp=drive_open)에서 다운로드할 수 있다. 

![캡처](https://user-images.githubusercontent.com/58945760/87054406-0708ce80-c23e-11ea-9cd5-1c89c28fc96a.PNG)

- 다운로드 가능한 파일은 위와 같으며, 특별한 신청 없이 누구나 이용 가능하다. 
- 감정 분류의 정확도를 높이기 위해 얼굴을 따로 crop한 1024x1024 이미지를 다운로드하였다. 
- 총 이미지는 **7만 장**이다. 



## 2. 이미지 선별  