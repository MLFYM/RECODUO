# 라이브러리 불러오기
from django.conf import settings
import numpy as np
import pandas as pd
import json
from gensim.models import Word2Vec
from scipy.sparse import csr_matrix
from scipy import sparse
from implicit.evaluation import  *
from implicit.als import AlternatingLeastSquares
import os; os.environ['KMP_DUPLICATE_LIB_OK']='True'
from collections import Counter
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import random
import phantomjs
import pickle

song_meta = pd.read_json(settings.MODEL_ROOT + '/newer_song_meta.json', encoding='utf-8')

# 2. trainset
playlist_df = pd.read_json(settings.MODEL_ROOT + '/train.json', typ = 'frame')

# Matrix-1 : 저장한 모델 불러오기
Model = Word2Vec.load(settings.MODEL_ROOT + '/tag2vec.model')

# Matrix-2 : R 행렬의 데이터 불러오기
R = sparse.load_npz(settings.MODEL_ROOT + "/R_data.npz")

# pickle을 이용해 훈련이 끝난 모델 불러오기
with open(settings.MODEL_ROOT + '/model_ALS.pkl', 'rb') as f:
    model_ALS=pickle.load(f)

# 유저-잠재요인 / 잠재요인-아이템 행렬에 대한 수치
user_factors = model_ALS.user_factors
item_factors = model_ALS.item_factors.T
print('**파일 및 모델 load 완료**')

# 코드 수정
# 유사한 태그 
def tags_for_rec(model, tag_name, top_n):

    pred_tags = model.wv.similar_by_word(word=tag_name, topn=top_n)
    tag_list = [tag for tag, _ in pred_tags]
    return tag_list
print('tags_for_rec 정의')

# 태그에서 플레이 리스트를 추천하는 메소드 만들기
def plst_id_for_rec(data, tags_list):
    plst_id_for_rec = []

    for index, value in enumerate(data[['id','tags']].values):
        # print(value[0])
        for tag in tags_list:
            # print(tag_list)
            if tags_list[1] in value[1]:
                plst_id_for_rec.append(value[0])
    # 후보 태그에 대한 추천될 플레이리스트 id 후보군이 형성된다.
    return plst_id_for_rec # 중복 언급 허용
print('plst_id_for_rec 정의')


# 플레이리스트 후보군에서 추천하는 노래 ID 후보군을 추출하는 메소드
def songs_for_rec(model, playlist_id, r, n):
    # plst_id_for_rec = list(set(plst_id_for_rec))
    songs_for_rec = []

    for idx in range(len(playlist_id)):
        # recommend items for a user
        recommendations = model.recommend(
                            userid = playlist_id[idx],
                            user_items = r,
                            N = n
                            )

        for song_id, rate in recommendations:
            # print(song_id)
            songs_for_rec.append(song_id)

    return songs_for_rec
print('songs_for_rec 정의')

# 만들어진 음악 후보군에서 최종으로 추천할 노래 생성(행렬1, 2 모두 적용)
def music_recommend(data, model, item_id, song_for_rec): # user_id => item_id

    answer = []
    str_item_id = str(item_id)
    count_songs = Counter(song_for_rec)

    # 후보군에서 반복언급된 TOP-3 노래 추출
    max_values = sorted(count_songs.values(), reverse=True)[1:4]

    ## 우선순위 1위 : 선호관계와 태그유사도에서 중복언급되는 곡id 확인
    # 1. 곡을 선호하는 유저 중 비슷한 유형의 TOP-3 유저id 추출
    recommended_id=data[data['songs'].astype('str').str.contains(str_item_id)].sort_values(by='like_cnt', ascending=False)[0:3]
    recommended_id = recommended_id['id'].to_list()

    # 2. 추출된 유저id의 플레이리스트 곡id 추출
    songs_id = []
    for pl_id in recommended_id:
        tmp = data[data['id']==pl_id]['songs'].tolist()
        songs_id += tmp[0]


    # 3. 이전에 태그유사도에서 추출한 song_for_rec과 교집합 추출
    songs_id = set(songs_id)
    intersect = list(songs_id.intersection(set(song_for_rec)))
    answer += intersect


    ## 우선순위 2위 : 디폴트로 6곡 추가
    # 1. 선호관계 유사도에서 추천곡 3개 디폴트
    songs_count = Counter(songs_id)
    tmpt = [song_id for song_id, _ in songs_count.most_common(3)]
    answer += tmpt

    # 2. 태그관계 유사도에서 추천곡 3개 디폴트
    for key in list(count_songs.keys()):
        if count_songs[key] == max_values :
            answer.append(key)
    # answer.sort()
    print('추천곡 후보군 :', answer)

    # input과 똑같은 id가 포함되어 있을 경우 삭제
    for s in answer:
        if s == item_id:
            answer.remove(s)
            print('기반 추천곡 제거 :', answer)
        else:
            pass

    # 우선순위 1, 2위 중 태그가 맞지 않을 경우
    while True:
        song_code = random.choice(answer)
        answer_df = song_meta[song_meta['id']==song_code]
        if answer_df.empty:
            answer.remove(song_code)

        if not answer_df.empty or len(answer)==0:
            break

    # 추천곡 이름 뽑아내기
    for value in answer_df['song_name'].values:
        song_title = value

    # 가수 이름 뽑아내기
    for value in answer_df['artist_name_basket'].values:
        artist_cell = value
        artist_name = artist_cell[0]

    return song_title, artist_name

    if len(answer)==0:
        while True:
            new_answer = list(count_songs.keys())
            song_code = random.choice(new_answer)
            new_answer_df = song_meta[song_meta['id']==song_code]
            if new_answer_df.empty:
                new_answer.remove(song_code)

            if not answer_df.empty or len(answer)==0:
                break

        # 추천곡 이름 뽑아내기
        for value in answer_df['song_name'].values:
            song_title = value

        # 가수 이름 뽑아내기
        for value in answer_df['artist_name_basket'].values:
            artist_cell = value
            artist_name = artist_cell[0]

        return song_title, artist_name


# 태그,곡 id만 입력하면 위의 메소드들이 다 실행되는 프로세스
def recommendation_process(tag, song_id, tag_model=Model, r_model=model_ALS, train=playlist_df):

    global tags_for_rec, plst_id_for_rec, songs_for_rec, music_recommend

    # 1. 태그 유사도 찾기
    tags_for_rec_result = tags_for_rec(model=tag_model, tag_name=tag, top_n=3)
    print('유사한 태그 : ', tags_for_rec_result)

    # 2. 태그를 가진 플레이리스트 찾기
    plst_id_for_rec_result = plst_id_for_rec(data=train, tags_list=tags_for_rec_result)

    # 3. 플레이리스트 중 가장 적합한 모델 찾기
    songs_for_rec_result = songs_for_rec(model=r_model, # 오류 발생 : data 넣을 필요 없음
                                         playlist_id = plst_id_for_rec_result,
                                         r = R,
                                         n = 1)

    # 4. 생성된 후보군으로 최종 모델 찾기
    music_recommend_result = music_recommend(data=train, model=r_model, item_id=song_id, song_for_rec=songs_for_rec_result)
    print(music_recommend_result)
    return music_recommend_result

print('recommendation_process 정의')
print('모든 함수 정의 완료')
