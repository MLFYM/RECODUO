from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from .forms import ImgeVessel, SimpleUploadForm
import re
import base64
import numpy as np
from django.core.files.base import ContentFile
from django.conf import settings
from .face_functions import deep_face
from .search_playlist import find_songlist, find_artist, find_songid, find_songtag, repeat_recommend, videoid_for_recommend
import random
import pandas as pd
from .music_recommend_system import recommendation_process, song_meta, playlist_df, Model, model_ALS
from .google_scraping import google_crawling, re_crawling


global song_title, song_artist

# 전체 플레이리스트 youtube id-플레이리스트 정보 엑셀파일
playlist_id = {'PLPKZ6FAxaaf_yPICacEriKUZNGCVnejsb': '00_neutral.xlsx', #00년대 무표정,
'PLPKZ6FAxaaf-fn_89jK5gKjTeEnrgcPNZ' : '10_neutral.xlsx', #10년대 무표정,
'PLPKZ6FAxaaf8SvwHeoLOrDyxEerJFwSu8' : '80_neutral.xlsx', #80년대 무표정
'PLPKZ6FAxaaf_PHNrkCrQY44IDrInhZMbu' : '90_neutral.xlsx', #90년대 무표정,
'PLPKZ6FAxaaf-HBMxB0udxPNS4fbgIGJ7U' : 'season_spring.xlsx', #계절 봄,
'PLPKZ6FAxaaf-FG89RDpcj93J5_kCy6VIk' : 'season_fall.xlsx', #계절 가을,
'PLPKZ6FAxaaf90RHGzpRbyZT27AIvAuUy3' : 'season_summer.xlsx', #계절 여름,
'PLPKZ6FAxaaf_pQhrkVk4ZF5W-PAHDF5XX' : 'season_winter.xlsx', #계절 겨울,
'PLPKZ6FAxaaf-QGIbdZkW8j-b7liNj-X34' : 'firstlove_elementrymiddle.xlsx', #첫사랑 초등학교 중학교,
'PLPKZ6FAxaaf9Rshcledolpp2btBCZPPTz' : 'firstlove_univ.xlsx', #첫사랑 대학생,
'PLPKZ6FAxaaf_BHrvuSeEdHAlz9iIqXex3' : 'firstlove_high.xlsx', #첫사랑 고등학생,
'PLPKZ6FAxaaf-rwhaSfuENK0jtxSLDY0gv' : 'firstlove_nomemory.xlsx', #첫사랑 기억 안 남, # 여기까지 neutral
'PLPKZ6FAxaaf-9VWC5yUVo3XKBXujNS9Fp' : '10_positive.xlsx', #10년대 기쁨,
'PLPKZ6FAxaaf8lr7Cs_ebaZ7BAZomtAAte' : 'fridaynight_pizza.xlsx', #야식 피자,
'PLPKZ6FAxaaf_mlK960KUVNp6GGW3TCfQe' : 'lunch_alone.xlsx', #혼밥 점심,
'PLPKZ6FAxaaf9mBJBR9GfQrn-vhYtU1hMf' : 'lunch_boss.xlsx', #상사 점심,
'PLPKZ6FAxaaf_7OD2RK8hUGSCCJd91uFQ6' : 'fridaynight_pork.xlsx', #야식 삼겹살,
'PLPKZ6FAxaaf_-0fbjwrvsGIXdHtkkRx7-' : 'lunch_lover.xlsx',#애인 점심,
'PLPKZ6FAxaaf-CypAyYlCEhwC021-L7RG6' : 'fridaynight_chicken.xlsx',#야식 치킨,
'PLPKZ6FAxaaf8Qy0qwF2l_z0hDY2eMkBDj' : '90_positive.xlsx',#90년대 기쁨,
'PLPKZ6FAxaaf-1DlgYO-jNoGrOWs5hxtnF' : '80_positive.xlsx',#80년대 기쁨,
'PLPKZ6FAxaaf9ol1GU68Z1F3BmXOMM2yYg' : 'lunch_friend.xlsx',#친구 점심,
'PLPKZ6FAxaaf84tyUkdnx3c5JxZ00-rGSu' : '00_positive.xlsx',#00년대 기쁨,
'PLPKZ6FAxaaf-PFri6jI4T6gc-eFoM6vuS' : 'fridaynight_bossam.xlsx',#야식 족발보쌈, # 여기까지 positive
'PLPKZ6FAxaaf-_lMPVx_8lqjrbzoQz1bs-' : '80_negative.xlsx',#80년대 찡그림,
'PLPKZ6FAxaaf9ve5PmOfLul2YmKqFy1BiW' : 'reducestress_trip.xlsx',#스트레스 여행가기,
'PLPKZ6FAxaaf8UAmP0b9jDquvTcbNUopwe' : 'reducestress_exercise.xlsx',#스트레스 운동하기,
'PLPKZ6FAxaaf_-QcMvllxn6VD4xY-hRkj3' : 'reducestress_sing.xlsx',#스트레스 노래부르기,
'PLPKZ6FAxaaf_M6QbHniDuOH72dWi0-yIm' : 'reducestress_sleep.xlsx',#스트레스 잠자기,
'PLPKZ6FAxaaf_xuAQPdNiL8vpNXmlbPpDt' : '00_negative.xlsx',#00년대 찡그림,
'PLPKZ6FAxaaf9Kx9UXB4kbQHjqaO5-3qEP' : 'sbsdrama.xlsx',#sbs 드라마 ost,
'PLPKZ6FAxaaf9HzZluME97m3YR8VW8eecu' : '90_negative.xlsx',#90년대 찡그림,
'PLPKZ6FAxaaf_d8w2hLcfu6ath9nh6T6MF' : 'tvndrama.xlsx',#tvn 드라마 ost,
'PLPKZ6FAxaaf9kH9m52BZ_iyy1n6ll-fwU' : 'jtbcdrama.xlsx',#jtbc 드라마 ost,
'PLPKZ6FAxaaf9OCNJ78XPZ2um0UBeVwszD' : 'mbcdrama.xlsx',#mbc 드라마 ost,
'PLPKZ6FAxaaf-3hB25RxNtE6AE7ZtaU5Qp' : 'kbsdrama.xlsx',#kbs 드라마 ost,
'PLPKZ6FAxaaf8ZgzLvW8WWpAHxS4unCEwv' : '10_negative.xlsx'#10년대 찡그림 # 여기까지 negative
}


def home(request):
    return render(request, 'mlfu/default.html', {})

def test(request):
    return render(request, 'mlfu/test.html', {})

def camera2(request):

    if request.method == 'POST':

        image_data = request.POST['imgsendinput']
        image_data2 = request.POST['imgsendinput']
        image_data = image_data.split(',')
        image_data = image_data[1]
        # image_data = image_data.encode()
        image_data = base64.b64decode(image_data)
        image_data = ContentFile(image_data, name='kk')
        # img = np.array(image_data)
        # print(image_data)
        print(type(image_data))
        print(type(image_data2))
        fs = FileSystemStorage()

        filename = fs.save('tt', image_data) # 경로명을 포함한 파일명 & 파일 객체
        uploaded_file_url = fs.url(filename) # 업로드된 이미지 파일의 URL을 얻어내 Template에게 전달

        imageURL = settings.MEDIA_URL + filename
        emotion_result = deep_face(settings.MEDIA_ROOT_URL + imageURL) # 이미지 얼굴 검출 및 모델 적용
        uploaded_file_url = uploaded_file_url +'2.jpeg'

        print(emotion_result) # 감정 판별 결과값 cmd에 출력

        # 각 감정에 따른 확률 계산
        neutral_p = emotion_result[1][0][0]*100
        positive_p = emotion_result[1][0][1]*100
        negative_p = emotion_result[1][0][2]*100

        neutral_p = round(neutral_p, 1)
        positive_p = round(positive_p, 1)
        negative_p = round(negative_p, 1)

        print(emotion_result[0])
        result = {"Neutral":"'무표정'으로 측정되었습니다", "Positive" : "'기쁨'으로 측정되었습니다", "Negative" : "'찡그림'으로 측정되었습니다", "Notfound":"얼굴이 발견되지 않았어요:(", "uploaded_file_url": uploaded_file_url,
        "neutral_p":neutral_p, "positive_p": positive_p, "negative_p": negative_p}

        if emotion_result[0] == 0: # 무표정 결과 페이지로 result와 넘김
            return render(request, 'mlfu/neutral_firstplaylist.html', {"result":result})
            # return render_to_response('mlfu/neutral_firstplaylist.html', {"result":result})

        elif emotion_result[0] == 1: # 기쁨 결과 페이지로 result와 넘김
            return render(request, 'mlfu/positive_firstplaylist.html', {"result":result})

        elif emotion_result[0] == 2: # 찡그림 결과 페이지로 result와 넘김
            return render(request, 'mlfu/negative_firstplaylist.html', {"result":result})

        else: # 이미지에서 얼굴이 검출되지 않을 경우 errorpage로 result와 넘김
            return render_to_response('mlfu/errorpage.html', {"result":result})


def giveQuestion_neutral(request): # 무표정 질문지 & 답변
    question_list_neutral = ["mlfu/neutral_randomquestion1.html", "mlfu/neutral_randomquestion2.html", "mlfu/neutral_randomquestion3.html"]
    playlist_url = random.choice(question_list_neutral) # 질문 세 개 중 랜덤으로 선택
    return render(request, playlist_url, {})

def giveQuestion_positive(request): # 기쁨 질문지 & 답변
    question_list_happy = ["mlfu/positive_randomquestion1.html", "mlfu/positive_randomquestion2.html", "mlfu/positive_randomquestion3.html"]
    playlist_url = random.choice(question_list_happy)
    return render(request, playlist_url, {})

def giveQuestion_negative(request): # 찡그림 질문지 & 답변
    question_list_frown = ["mlfu/negative_randomquestion1.html", "mlfu/negative_randomquestion2.html", "mlfu/negative_randomquestion3.html"]
    playlist_url = random.choice(question_list_frown)
    return render(request, playlist_url, {})

def image_upload(request): # 로컬에서 이미지 업로드
    if request.method == 'POST':
        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            context = {'form':form, 'uploaded_file_url': uploaded_file_url}

            # 이하 모델 적용
            imageURL = settings.MEDIA_URL + filename
            emotion_result = deep_face(settings.MEDIA_ROOT_URL + imageURL) # val, pred_y => ex) [0, [[0.98, 0.72, 0.02]]]
            uploaded_file_url = uploaded_file_url +'2.jpeg'

            # 각 감정에 따른 확률 계산
            print(emotion_result)
            neutral_p = emotion_result[1][0][0]*100
            positive_p = emotion_result[1][0][1]*100
            negative_p = emotion_result[1][0][2]*100

            neutral_p = round(neutral_p, 1)
            positive_p = round(positive_p, 1)
            negative_p = round(negative_p, 1)

            print(emotion_result[0])
            result = {"Neutral":"'무표정'으로 측정되었습니다", "Positive" : "'기쁨'으로 측정되었습니다", "Negative" : "'찡그림'으로 측정되었습니다", "Notfound":"얼굴이 발견되지 않았어요:(", "uploaded_file_url": uploaded_file_url,
            "neutral_p":neutral_p, "positive_p": positive_p, "negative_p": negative_p}

            if emotion_result[0] == 0:
                # return HttpResponse("'무표정'으로 측정되었습니다")
                return render_to_response('mlfu/neutral_firstplaylist.html', {"result":result})
            elif emotion_result[0] == 1:
                # return HttpResponse("'기쁨'으로 측정되었습니다")
                return render_to_response('mlfu/positive_firstplaylist.html', {"result":result})
            elif emotion_result[0] == 2:
                # return HttpResponse("'찡그림'으로 측정되었습니다")
                return render_to_response('mlfu/negative_firstplaylist.html', {"result":result})
            else:
                return render_to_response('mlfu/errorpage.html', {"result":result})

    else:
        form = SimpleUploadForm()
        context = {'form': form}
        return render(request, 'mlfu/image_upload.html', context)

def song_list(request):
    global song_title, song_artist
    if request.method == 'POST':
        plstid = request.POST['playlistid']
        vid = request.POST['videoid']
        print(vid)
        playlist_file = playlist_id[plstid]

        songinfo = videoid_for_recommend(playlist_file, vid)
        # song_title = find_songlist(playlist_file)
        # song_artist = find_artist(playlist_file)

        # song_info = {'song_title' : song_title, 'song_artist': song_artist, 'plstid' : plstid}

        song_recommend = recommendation_process(tag=songinfo[0], song_id=songinfo[1])

        # # 수정 필요
        answer = google_crawling(song_recommend) # (video id, 곡 이름, 가수)
        print('크롤링 결과 :', answer)

        if len(answer) == 2:
            recomm_song = song_recommend
            result = {'recomm_song' : recomm_song }
            return render(request, 'mlfu/not_found.html', {'result' : result})

        else: # (video id, 곡 이름, 가수)
            result = {'song_recommend' : song_recommend, 'answer' : answer }
            return render(request, 'mlfu/recommend_song.html', {'result': result})

        # return render(request, 'mlfu/check_playlist.html', {"song_info":song_info})

def recommend_function(request):
    if request.method == 'POST':
        plstid = request.POST['sendid']
        title = request.POST['title']
        print(title)
        file = playlist_id[plstid]
        songid = find_songid(file, title)
        songtag = find_songtag(file, title)
        song_recommend = recommendation_process(tag=songtag, song_id=songid)

        # # 수정 필요
        answer = google_crawling(song_recommend) # (video id, 곡 이름, 가수)
        # if recomm_song == result:
        #     not_found = {'result' : result}
        #     return render(request, 'mlfu/not_found.html', {'not_found' : result})
        print('크롤링 결과 :', answer)

        if len(answer) == 2:
            recomm_song = song_recommend
            result = {'recomm_song' : recomm_song }
            return render(request, 'mlfu/not_found.html', {'result' : result})

        else: # (video id, 곡 이름, 가수)
            result = {'song_recommend' : song_recommend, 'songid' : songid, 'songtag' : songtag, 'answer' : answer }
            return render(request, 'mlfu/recommend_song.html', {'result': result})


def recommend_repeat(request):
    if request.method == 'POST':
        s_name = request.POST['songname']
        s_artist = request.POST['songartist']

        recommend_result = repeat_recommend(s_name, s_artist)
        print(recommend_result)

        # 곡 id는 song_meta에서, 태그는 song_meta에서 앨범명을 찾은 후 playlist_df에서 검색해야 한다!
        recommend_video = recommendation_process(tag=recommend_result[0], song_id=recommend_result[1])
        recomm_song = google_crawling(recommend_video)
        print('크롤링 결과:', recomm_song)

        if len(recomm_song) == 2:
            result = {'recomm_song' : recomm_song}
            return render(request, 'mlfu/not_found.html', {'result' : result})


        else:# (video id, 곡 이름, 가수)
            song_result = {'recommend_video' : recommend_video, 'recomm_song' : recomm_song}
            return render(request, 'mlfu/recommend_repeat.html', {'song_result' : song_result })
