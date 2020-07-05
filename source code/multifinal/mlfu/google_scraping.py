from django.conf import settings
from selenium import webdriver
import time
import re
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.parse import quote
import phantomjs
from .music_recommend_system import recommendation_process, song_meta, playlist_df, Model, model_ALS
from .search_playlist import repeat_recommend


# video link를 가져오기 위한 class는 AP7Wnd, rl7ilb, kCrYT 세 개이며
# AP7Wnd > rl7ilb > kCrYT 순으로 크롤링하며 video id를 찾는다

# 재크롤링을 위한 함수
def re_crawling(recommend_song):

    re_result = repeat_recommend(recommend_song[0], recommend_song[1])

    # 곡 id는 song_meta에서, 태그는 song_meta에서 앨범명을 찾은 후 playlist_df에서 검색해야 한다!
    re_video = recommendation_process(tag=re_result[0], song_id=re_result[1])

    song_name = re_video[0]
    artist_name = re_video[1]

    url = "https://www.google.com/search?q="+artist_name+"+"+song_name
    print(url)

    # beautifulsoup
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)

    # 접근 차단 방지를 위한 5초 대기
    # time.sleep(5)

    # Youtube video 링크를 포함한 모든 URL을 받아오기 위한 리스트
    url_li = [] # 첫 번째 크롤링 리스트
    a_li = []

    for text in soup.find_all('div', {'class' : 'AP7Wnd'}): # div 태그 안 'AP7Wnd' 클래스에 속하는 모든 것을 가져옴
        url = text.get_text() # 텍스트 추출
        if "https://www.youtube.com/watch?v=" in url:
            url_li.append(url) # 리스트에 추가

    print("재크롤링 AP url 리스트 :", url_li)

    if len(url_li) != 0:
        return url_li, re_video[0], re_video[1]

    else:
        col = 0
        atag =[]
        for taglist in soup.find_all('div', {'class':'rl7ilb'}):
            if taglist.find('a') != None:
                tag = taglist.find('a')['href']
                atag.append(tag)
                col += 1
        print('rl7ilb href 태그 리스트 :', atag)

        if len(atag) == 0:
            count = 0
            at=[]
            for tag_list in soup.find_all('div', {'class':'kCrYT'}):
                if tag_list.find('a') != None:
                    t = tag_list.find('a')['href']
                    at.append(t)
                    count +=1
            print('kCrYT href 리스트 :', at)

            if count != 0:
                youtube_url = []
                y_count = 0
                for a in at:
                    if "/url?q=https://www.youtube.com/watch%3Fv%3D" in a:
                        youtube_url.append(a)

                if len(youtube_url) != 0:
                    print('youtube 리스트 :', youtube_url)
                    return youtube_url, re_video[0], re_video[1]
                else:
                    print('url을 찾지 못했습니다. 크롤링을 계속합니다.')
                    return re_video[0], re_video[1]

            else:
                print('url을 찾지 못했습니다. 크롤링을 계속합니다.')
                return re_video[0], re_video[1]

        else:
            youtube_count = 0
            y_li = []
            for a in atag:
                if "/url?q=https://www.youtube.com/watch%3Fv%3D" in a:
                    y_li.append(a)
                    youtube_count += 1

            if youtube_count != 0:
                print("youtube url을 찾았습니다.")
                return y_li, re_video[0], re_video[1]

            else:
                yt_count = 0
                yt_li=[]
                for tag_list in soup.find_all('div', {'class':'kCrYT'}):
                    if tag_list.find('a') != None:
                        t = tag_list.find('a')['href']
                        yt_li.append(t)
                        yt_count +=1
                print('kCrYT href 리스트 :', yt_li)

                if yt_count != 0:
                    youtube_url = []
                    y_count = 0
                    for a in y_li:
                        if "/url?q=https://www.youtube.com/watch%3Fv%3D" in a:
                            youtube_url.append(a)

                    if len(youtube_url) != 0:
                        print('youtube 리스트 :', youtube_url)
                        return youtube_url, re_video[0], re_video[1]

                    else:
                        print('url을 찾지 못했습니다. 크롤링을 계속합니다.')
                        return re_video[0], re_video[1]

                else:
                    print('url을 찾지 못했습니다. 크롤링을 계속합니다.')
                    return re_video[0], re_video[1]




# 크롤링 함수
def google_crawling(recommend_song):
    song_name = recommend_song[0] # 곡 이름
    artist_name = recommend_song[1] # 가수 이름

    url = "https://www.google.com/search?q="+artist_name+"+"+song_name
    print(url)

    # beautifulsoup
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)

    # 접근 차단 방지를 위한 5초 대기
    # time.sleep(5)

    # Youtube video 링크를 포함한 모든 URL을 받아오기 위한 리스트
    url_li = [] # 첫 번째 크롤링 리스트
    s_url_li = [] # 두 번째 크롤링 리스트
    t_url_li = []

    for text in soup.find_all('div', {'class' : 'AP7Wnd'}): # div 태그 안 'AP7Wnd' 클래스에 속하는 모든 것을 가져옴
        # print("***AP7Wnd 태그 불러오기 완료 ***")
        url = text.get_text() # 텍스트 추출
        if "https://www.youtube.com/watch?v=" in url:
            url_li.append(url) # 리스트에 추가

    print("***url 리스트 구성 완료***")
    print('AP7Wnd url 리스트 확인 :', url_li)
    print(len(url_li))

    if len(url_li) == 0:
        print('**AP7Wnd 클래스에서 파싱 실패**')
        # time.sleep(5) # 5초 대기

        a_tag_li = [] # a tag를 받을 리스트

        # class rl7ilb에 속하는 모든 것을 긁어온다
        col = 0
        for taglist in soup.find_all('div', {'class':'rl7ilb'}):
            if taglist.find('a') != None:
                x = taglist.find('a')
                a_tag_li.append(x)
                col += 1

        if col == 0:
            print('**rl7ilb 클래스에서 파싱 실패**')
            a_count = 0
            for tag_list in soup.find_all('div', {'class':'kCrYT'}):
                if tag_list.find('a') != None:
                    x = tag_list.find('a')
                    a_tag_li.append(x)
                    a_count += 1

            if a_count == 0:
                print('***재크롤링 시작***')
                # a 태그가 나올 때까지 아래의 함수 반복
                while True:
                    atag_li = re_crawling(recommend_song) # 재크롤링 함수 적용
                    if atag_li[0] != None or len(atag_li)==2: # 함수값이 존재하지 않을 경우
                        break # 루프 멈춤

                if len(atag_li) == 2:
                    print('크롤링에 실패했습니다.')
                    return atag_li

                # youtube 링크 주소가 list 안에 존재할 경우 1
                elif len(atag_li[0]) == 1 or any(t for t in atag_li[0] if "https://www.youtube.com/watch?v=" in t):
                    print('***재크롤링 종료***')
                    print("**youtube 링크 발견**")
                    h_li = [t for t in atag_li[0] if "https://www.youtube.com/watch?v=" in t]
                    x = h_li[0] # s_url_li의 첫 번째 아이템 꺼내기
                    song_id_1 = x[32:] # 전체 URL 중 video id부분만 슬라이싱
                    print('video id는 {}입니다.'.format(song_id_4))

                    return song_id_1, atag_li[1], atag_li[2]


                elif any(t for t in atag_li[0] if "/url?q=https://www.youtube.com/watch%3Fv%3D" in t):
                    print('***재크롤링 종료***')
                    print("**youtube 링크 발견**")
                    h_li = [t for t in atag_li[0] if "/url?q=https://www.youtube.com/watch%3Fv%3D" in t]
                    x = h_li[0] # s_url_li의 첫 번째 아이템 꺼내기
                    song_id_2 = x[43:54] # 전체 URL 중 video id부분만 슬라이싱
                    print('video id는 {}입니다.'.format(song_id_2))

                    return song_id_2, atag_li[1], atag_li[2]


            else:
                print('a 태그 리스트 :', a_tag_li)
                y_url_li = []
                y_count = 0
                for s in a_tag_li:
                    s_href = s['href']
                    if "/url?q=https://www.youtube.com/watch%3Fv%3D" in s_href:
                        y_url_li.append(s_href)
                        print("**youtube 링크 발견**")
                        y_count += 1

                print('y count : ', y_count)

                if y_count != 0:
                    y = y_url_li[0] # url_li의 첫 번째 아이템 꺼내기
                    song_id_3 = y[43:54] # 전체 URL 중 video id부분만 슬라이싱
                    print('video id는 {}입니다.'.format(song_id_3))

                    return song_id_3, recommend_song[0], recommend_song[1]

                else:
                    while True:
                        atag_li = re_crawling(recommend_song) # 재크롤링 함수 적용
                        if atag_li[0] != None or len(atag_li)==2: # 함수값이 존재할 경우
                            break # 루프 멈춤

                    if len(atag_li)==2:
                        print('크롤링에 실패했습니다.')
                        return atag_li

                    # youtube 링크 주소가 list 안에 존재할 경우 1
                    elif len(atag_li[0]) == 1 or any(t for t in atag_li[0] if "https://www.youtube.com/watch?v=" in t):
                        print('***재크롤링 종료***')
                        print("**youtube 링크 발견**")
                        h_li = [t for t in atag_li[0] if "https://www.youtube.com/watch?v=" in t]
                        x = h_li[0] # s_url_li의 첫 번째 아이템 꺼내기
                        song_id_4 = x[32:] # 전체 URL 중 video id부분만 슬라이싱
                        print('video id는 {}입니다.'.format(song_id_4))

                        return song_id_4, atag_li[1], atag_li[2]


                    elif any(t for t in atag_li[0] if "/url?q=https://www.youtube.com/watch%3Fv%3D" in t):
                        print('***재크롤링 종료***')
                        print("**youtube 링크 발견**")
                        h_li = [t for t in atag_li[0] if "/url?q=https://www.youtube.com/watch%3Fv%3D" in t]
                        x = h_li[0] # s_url_li의 첫 번째 아이템 꺼내기
                        song_id_5 = x[43:54] # 전체 URL 중 video id부분만 슬라이싱
                        print('video id는 {}입니다.'.format(song_id_5))

                        return song_id_5, atag_li[1], atag_li[2]


        else: # rl7ilb
            print('a 태그 리스트 :', a_tag_li)
            if any(s for s in a_tag_li if "/url?q=https://www.youtube.com/watch%3Fv%3D" in s):
                print("**youtube 링크 발견**")
                url_li = [s for s in a_li if "/url?q=https://www.youtube.com/watch%3Fv%3D" in s]
                y = url_li[0] # url_li의 첫 번째 아이템 꺼내기
                song_id_6 = y[43:54] # 전체 URL 중 video id부분만 슬라이싱
                print('video id는 {}입니다.'.format(song_id_3))

                return song_id_6, recommend_song[0], recommend_song[1]
                # 예외처리 고민


    else:
        s = url_li[0]
        song_id = s[32:43] # 전체 URL에서 video id만 슬라이싱
        print('video id는 {}입니다.'.format(song_id))

        return song_id, recommend_song[0], recommend_song[1]
