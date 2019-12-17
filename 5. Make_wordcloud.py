import pandas as pd
from konlpy.tag import Twitter
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

'''
별점 참여자수 평균
high : 17458.482
low  : 21073.924

high false(부정) : 2224개 
high true(긍정)  : 2776개
low  false(부정) : 3271개 
low  true(긍정)  : 1727개 
'''

## 워드클라우드 색상 함수들
def make_colors_Reds(word,font_size,position,orientation,random_state,**kwargs):
    color = 'rgb(255,0,0)'
    return color

def make_colors_Blues(word,font_size,position,orientation,random_state,**kwargs):
    color = 'rgb(0,0,255)'
    return color

# 워드클라우드 제작 함수
# 변수 : csv_path = 워드클라우드 만들 csv파일 , col_name = csv파일의 string이 저장된 열이름
#       cloud_name = 저장될 워드클라우드 파일이름, font_color = 'Reds or Blues'
#       size = 소수점 3자리 float ex) size = 0.653 > 해상도 '653*653'
def WC_Make(csv_path, col_name, cloud_name, font_color, size):
    df = pd.read_csv(csv_path)
    reply = df[col_name].tolist()
    reply = ''.join(reply)

    # norm == 정규화(normalization)
    # 한국어를 처리하는 예시입니닼ㅋㅋㅋ -> 한국어를 처리하는 예시입니다ㅋㅋ
    # stem == 어근화(stemming)
    # 한국어를 처리하는 예시입니다 ㅋㅋ -> 한국어Noun, 를Josa, 처리Noun, 하다Verb, 예시Noun, 이다Adjective, ㅋㅋKoreanParticle
    twitter = Twitter()
    raw_pos_tagged = twitter.pos(reply, norm=True, stem=True)

    # 정규화 및 어근화를 마치고 품사 태깅까지 마친 상태에서,
    # 조사, 어미, 구두점을 제외한 나머지 단어들을 모두 word_cleaned 리스트에 담습니다.
    # 이 때에는 여러번 나온 단어들도 복수 허용되어 여러번 리스트에 담기게 됩니다.
    # 유의미한 의미를 갖고 있지 않은 단어를 제외할 수 있습니다.
    del_list = ['하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다',
                '보다','나오다','가다','알다','들다','지다','오다','해주다','시키다','받다','만들다','그리고','많다',
                '싶다','치다','보이다','근데','자다','나다','넣다','밀다','같다','없다','ㅠㅠ','자기','인호','ㅋㅋ',
                '동태','덴마','지금','오수','은주','지은','지은이','그냥','그리다','주다','하나','계속','정도',
                '이제','이번','유미','그래서','인호','유정']

    word_cleaned = []
    for word in raw_pos_tagged:
        if not word[1] in ["Josa", "Eomi", "Punctuation", "Foreign"]:  # Foreign == ”, “ 와 같이 제외되어야할 항목들
            if (len(word[0]) != 1) & (word[0] not in del_list):  # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외
                word_cleaned.append(word[0])

    # 리스트에 담긴 단어들을 대상으로 갯수를 세어,
    # 단어를 'key'로 등장 횟수를 'value'로 하는 dict를 만듭니다.
    word_dic = {}
    for word in word_cleaned:
        if word not in word_dic:
            word_dic[word] = 1  # changed from "0" to "1"
        else:
            word_dic[word] += 1

    # lambda 함수를 활용하여, 앞서 만든 dict를 value(==x[1])를 기준으로 하여 내림차순(reverse=True) 정렬합니다.
    sorted_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

    print('')
    print(cloud_name)

    cnt = 1
    for word, count in sorted_word_dic[:50]:
        print("{0}({1})".format(word, count), end=" ")
        if cnt%10 == 0:
            print('')
        cnt += 1

    naver_mask = np.array(Image.open("mergeimg4.jpg"))

    word_cloud = WordCloud(font_path="AppleGothic",
                           mask=naver_mask,
                           background_color='white')

    word_cloud.generate_from_frequencies(word_dic)
    if font_color == 'Reds':
        word_cloud.recolor(color_func=make_colors_Reds)
    else :
        word_cloud.recolor(color_func=make_colors_Blues)
    plt.figure(figsize=(7*size, 7*size))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(cloud_name)

WC_Make('./high_comments_False.csv','high_comment_False','high_False_Frequency.png','Reds',round(0.2224*2,3))
WC_Make('./high_comments_True.csv','high_comment_True','high_True_Frequency.png','Blues',round(0.2776*2,3))
WC_Make('./low_comment_False.csv','low_comment_False','low_False_Frequency.png','Reds',round(0.3271*2,3))
WC_Make('./low_comment_True.csv','low_comment_True','low_True_Frequency.png','Blues',round(0.1727*2,3))

## 시각화 해야할것
## 평균 별점, 평균 별점 참여자수, 긍정/부정 갯수 차이, 평균 랭킹