import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
목적 : 앞서 얻은 정보를 활용해 긍정적, 부정적 댓글들(각 500개씩)을 분류해서 정리한다.  
결과 : 높은 별점 부정/긍정, 낮은 별점 부정/긍정 으로 분류해서 csv파일로 저장 
별점 참여자수 평균 = high : 17458.482명 
                 low : 21073.924명
높은 별점 긍정/부정 = high : 2224개 false(부정)
                  high : 2776개 true(긍정)
낮은 별점 긍정/부정 = low : 3271개 false(부정)
                  low : 1727개 true(긍정)
'''

emotion_highstar_path = 'path/to/highstar_emotion.csv'
emotion_lowstar_path = 'path/to/lowstar_emotion.csv'
info_path = 'path/to/weebtoon_info.csv'

highstar_csv = pd.read_csv(emotion_highstar_path)
lowstar_csv = pd.read_csv(emotion_lowstar_path)
rank_serach_csv = pd.read_csv(info_path,encoding="cp949")


## 각 코멘트 리스트
False_comment_list = []
True_comment_list = []
False_comment_listl = []
True_comment_listl = []
## 각 조회수 순위 리스트
rank_high_false = []
rank_high_True = []
rank_low_false = []
rank_low_True = []
## 각 별점 참여자수 평균 리스트
starM_high_false = []
starM_high_True = []
starM_low_false = []
starM_low_True = []
## 각 별점 평균 리스트
starP_high_false = []
starP_high_True = []
starP_low_false = []
starP_low_True = []

for i in range(1,11) :
    dff = highstar_csv[highstar_csv[f'comment{i}e'].isin([False])][f'comment{i}']
    df = highstar_csv[highstar_csv[f'comment{i}e'].isin([True])][f'comment{i}']
    rank = highstar_csv[highstar_csv[f'comment{i}e'].isin([False])]['titleId']
    rank2 = highstar_csv[highstar_csv[f'comment{i}e'].isin([True])]['titleId']
    mean_f = highstar_csv[highstar_csv[f'comment{i}e'].isin([False])]['star_person']
    mean_t = highstar_csv[highstar_csv[f'comment{i}e'].isin([True])]['star_person']
    point_f = highstar_csv[highstar_csv[f'comment{i}e'].isin([False])]['star_point']
    point_t = highstar_csv[highstar_csv[f'comment{i}e'].isin([True])]['star_point']

    False_comment_list = False_comment_list + list(dff)
    True_comment_list = True_comment_list + list(df)
    rank_high_false = rank_high_false + list(rank)
    rank_high_True = rank_high_True + list(rank2)
    starM_high_false = starM_high_false + list(mean_f)
    starM_high_True = starM_high_True + list(mean_t)
    starP_high_false = starP_high_false + list(point_f)
    starP_high_True = starP_high_True + list(point_t)

col1 = ['high_comment_False']
table = pd.DataFrame(False_comment_list, columns=col1)
table.to_csv('./high_comments_False.csv', encoding="utf_8_sig", mode='w', index=True)

col2 = ['high_comment_True']
table = pd.DataFrame(True_comment_list, columns=col2)
table.to_csv('./high_comments_True.csv', encoding="utf_8_sig", mode='w', index=True)

error_list = []

for j in range(1,11) :
    if j == 1 :
        dffl = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['False'])][f'comment{j}']
        dfl = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['True'])][f'comment{j}']
        dfa = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['추출불가'])][f'comment{j}']
        rankl = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['False'])]['titleId']
        rank2l = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['True'])]['titleId']
        mean_lf = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['False'])]['star_person']
        mean_lt = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['True'])]['star_person']
        point_lf = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['False'])]['star_point']
        point_lt = lowstar_csv[lowstar_csv[f'comment{j}e'].isin(['False'])]['star_point']

    else :
        dffl = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([False])][f'comment{j}']
        dfl = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([True])][f'comment{j}']
        rankl = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([False])]['titleId']
        rank2l = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([True])]['titleId']
        mean_lf = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([False])]['star_person']
        mean_lt = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([True])]['star_person']
        point_lf = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([False])]['star_point']
        point_lt = lowstar_csv[lowstar_csv[f'comment{j}e'].isin([False])]['star_point']

    # print(len(list(dffl)+list(dfl)))

    False_comment_listl = False_comment_listl + list(dffl)
    True_comment_listl = True_comment_listl + list(dfl)
    rank_low_false = rank_low_false + list(rankl)
    rank_low_True = rank_low_True + list(rank2l)
    starM_low_false = starM_low_false + list(mean_lf)
    starM_low_True = starM_low_True + list(mean_lt)
    starP_low_false = starP_low_false + list(point_lf)
    starP_low_True = starP_low_True + list(point_lt)

col1 = ['low_comment_False']
table = pd.DataFrame(False_comment_listl, columns=col1)
table.to_csv('./low_comment_False.csv', encoding="utf_8_sig", mode='w', index=True)

col2 = ['low_comment_True']
table = pd.DataFrame(True_comment_listl, columns=col2)
table.to_csv('./low_comment_True.csv', encoding="utf_8_sig", mode='w', index=True)


rank_high_false = list(set(rank_high_false))
rank_high_True = list(set(rank_high_True))
rank_low_false = list(set(rank_low_false))
rank_low_True = list(set(rank_low_True))

high_false_rlist = list(rank_serach_csv[rank_serach_csv['titleID'].isin(rank_high_false)]['rank'])
avgee = sum(high_false_rlist)/len(high_false_rlist)
avgaa = sum(starM_high_false)/len(starM_high_false)
avgbb = sum(starP_high_false)/len(starP_high_false)
print('**별점 높고 부정적 댓글들**')
print('랭크 평균:'+str(avgee))
print('별점 참여자수 평균:'+str(avgaa))
print('별점 평균:'+str(avgbb))
print('갯수 :')
print(len(False_comment_list))

high_True_rlist = list(rank_serach_csv[rank_serach_csv['titleID'].isin(rank_high_True)]['rank'])
avgee = sum(high_True_rlist)/len(high_True_rlist)
avgaa = sum(starM_high_True)/len(starM_high_True)
avgbb = sum(starP_high_True)/len(starP_high_True)
print('**별점 높고 긍정적 댓글들**')
print('랭크 평균:'+str(avgee))
print('별점 참여자수 평균:'+str(avgaa))
print('별점 평균:'+str(avgbb))
print('갯수 :')
print(len(True_comment_list))

low_false_rlist = list(rank_serach_csv[rank_serach_csv['titleID'].isin(rank_low_false)]['rank'])
avgee = sum(low_false_rlist)/len(low_false_rlist)
avgaa = sum(starM_low_false)/len(starM_low_false)
avgbb = sum(starP_low_false)/len(starP_low_false)
print('**별점 낮고 부정적 댓글들**')
print('랭크 평균:'+str(avgee))
print('별점 참여자수 평균:'+str(avgaa))
print('별점 평균:'+str(avgbb))
print('갯수 :')
print(len(False_comment_listl))

low_True_rlist = list(rank_serach_csv[rank_serach_csv['titleID'].isin(rank_low_True)]['rank'])
avgee = sum(low_True_rlist)/len(low_True_rlist)
avgaa = sum(starM_low_True)/len(starM_low_True)
avgbb = sum(starP_low_True)/len(starP_low_True)
print('**별점 낮고 긍정적 댓글들**')
print('랭크 평균:'+str(avgee))
print('별점 참여자수 평균:'+str(avgaa))
print('별점 평균:'+str(avgbb))
print('갯수 :')
print(len(True_comment_listl))

## 랭크 / 별점 / 별점평균 / 갯수  시각화
y1_value = (18.93, 17.64)
x_name=('high', 'low')
n_groups = len(x_name)
index = np.arange(n_groups)
plt.bar(index, y1_value, tick_label=x_name, align='center')
plt.xlabel('star high or low')
plt.ylabel('average rank')
plt.xlim( -1, n_groups)
plt.ylim( 0, 30)
plt.savefig('rank_bar.png')
plt.show()

## 별점 평균
y1_value = (9.99, 6.99)
x_name=('high', 'low')
n_groups = len(x_name)
index = np.arange(n_groups)
plt.bar(index, y1_value, tick_label=x_name, align='center')
plt.xlabel('star high or low')
plt.ylabel('star point')
plt.xlim( -1, n_groups)
plt.ylim( 0, 10)
plt.savefig('starpoint_bar.png')
plt.show()

## 별점 참여자수
## (17209+17657)/2 = 17433
## (20813+21583)/2 = 21198
y1_value = (17433, 21198)
x_name=('high', 'low')
n_groups = len(x_name)
index = np.arange(n_groups)
plt.bar(index, y1_value, tick_label=x_name, align='center')
plt.xlabel('star high or low')
plt.ylabel('person cnt')
plt.xlim( -1, n_groups)
plt.ylim( 0, 25000)
plt.savefig('person_bar.png')
plt.show()

## 갯수
y1_value = (2224,2776,3271,1727)
x_name=('high negative', 'high positive', 'low negative', 'low positive')
n_groups = len(x_name)
index = np.arange(n_groups)
plt.bar(index, y1_value, tick_label=x_name, align='center')
plt.xlabel('star high or low')
plt.ylabel('weebtoon cnt')
plt.xlim( -1, n_groups)
plt.ylim( 0, 3500)
plt.savefig('PNcount.png')
plt.show()