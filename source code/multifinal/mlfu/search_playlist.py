from django.conf import settings
from .music_recommend_system import song_meta, playlist_df
from collections import Counter
import itertools
import random
import pandas as pd

def find_songlist(file):
    path = settings.MODEL_ROOT + '/data/' + file
    df = pd.read_excel(path, index_col=0)
    title = df['노래명'].tolist()
    return title

def find_artist(file):
    path = settings.MODEL_ROOT + '/data/' + file
    df = pd.read_excel(path, index_col=0)
    artist = df['아티스트'].tolist()
    return artist

def find_songid(file, name):
    path = settings.MODEL_ROOT + '/data/' + file
    df = pd.read_excel(path, index_col=0)
    title = df['노래명'].tolist()
    idx = title.index(name)
    songid = df['id'].tolist()
    print(songid[idx])
    return songid[idx]

def find_songtag(file, name):
    path = settings.MODEL_ROOT + '/data/' + file
    df = pd.read_excel(path, index_col=0)
    title = df['노래명'].tolist()
    idx = title.index(name)
    songtag = df['곡 태그'].tolist()
    print(songtag[idx])
    return songtag[idx]

def videoid_for_recommend(file, id):
    path = settings.MODEL_ROOT + '/data/' + file
    df = pd.read_excel(path, index_col=0)
    title = df['videoid'].tolist()
    title_2 = []
    for t in title:
        video_code = t.replace("'", '').replace('"', '')
        title_2.append(video_code)

    idx = title_2.index(id)
    songtag = df['곡 태그'].tolist()
    songid = df['id'].tolist()
    print(songtag[idx], songid[idx])
    return songtag[idx], songid[idx]


def repeat_recommend(song_title, song_artist):
    title = song_title
    artist = song_artist

    df = song_meta[song_meta['song_name'] == song_title]
    artist_name = df['artist_name_basket'].tolist()
    id_li = df['id'].tolist()
    # artist_name = list(itertools.chain(*artist_name))

    idx_li = []

    for i, artist_li in enumerate(df['artist_name_basket']):
        for a in artist_li:
            if a == song_artist:
                print(artist_li)
                idx = artist_name.index(artist_li)
                print(i)
                songid = id_li[i]
                idx_li.append(songid)


    choice_songid = random.choice(idx_li)
    print('선택된 곡 id :', choice_songid)

    # 1. id로 관련 playlist tag 정보 뽑아내기
    songlist_li = playlist_df['songs'].tolist()
    tag_li = playlist_df['tags'].tolist()
    plsttag = []

    for songlist in playlist_df['songs']:
        for song in songlist:
            if song == choice_songid:
                print(songlist)
                li_idx = songlist_li.index(songlist)
                print(li_idx)
                tag = tag_li[li_idx]
                plsttag.append(tag)


    print('태그 목록 :', plsttag)
    plsttag = list(itertools.chain(*plsttag))
    count_item = Counter(plsttag)
    best_tag = count_item.most_common(n=1)
    print(best_tag[0][0])

    if best_tag[0][1] > 1:
        return best_tag[0][0], choice_songid

    else:
        random_tag = random.choice(plsttag)
        print('선택된 태그 : ', random_tag)
        return random_tag, choice_songid
