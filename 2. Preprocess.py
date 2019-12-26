import pandas as pd

info_path = 'path/to/weebtoon_star_info.csv'
reply_path = 'path/to/weebtoon_reply_info.csv'

csv = pd.read_csv(info_path)
csv2 = pd.read_csv(reply_path)
del csv2['Unnamed: 0']

## 2차원 배열 동적 선언
reply_list = []
for i in range(10):
    reply_list.append([])

csv_sort = csv.sort_values(by='star_point',axis=0)
## 웹툰 별점 하위 1000개 정보 가져오기
lowstar_csv = csv_sort[0:1000]

#두번 들어가있는 중복댓글 제거
lowstar_csv = lowstar_csv.drop_duplicates(["titleId","nom"],keep='first')
print(lowstar_csv)

titleId_lowlst = list(lowstar_csv['titleId'])
nom_lowlst = list(lowstar_csv['nom'])

for i in range(len(titleId_lowlst)):
    aa = csv2[csv2['titleId'].isin([f'{titleId_lowlst[i]}'])]
    bb = aa[aa['nom'].isin([f'{nom_lowlst[i]}'])]
    for j in range(1, 11):
        try:
            reply_list[j - 1].append(str(bb[f'comment{j}'].values[0]))
        except:
            # 없는 자료엔 공백('')을 추가.
            reply_list[j - 1].append('')
            # print('없는자료..')
            pass

# DataFrame자료형인 lowstar_csv에 comment1~10 열을 생성해 댓글을 넣어준다.
for i in range(10):
    lowstar_csv[f'comment{i+1}'] = reply_list[i]

# 해당 없는자료, weebtoon_star_info에 있는자료가 weebtoon_reply_info에는 없을 수 있다.
# 그러므로 없는자료에는 공백('')을 추가해둬 공백데이터는 이 단계에서 삭제해준다.
idx = lowstar_csv[lowstar_csv['comment1']==''].index
lowstar_csv = lowstar_csv.drop(idx)
print(lowstar_csv)
# 500개의 데이터만 뽑아 저장.
lowstar_csv = lowstar_csv[:500 - len(lowstar_csv)]
print(lowstar_csv)
lowstar_csv.to_csv("./lowstar_reply.csv", encoding="utf_8_sig", mode='w')


## 웹툰 별점 상위 500개 정보 가져오기
## 문제점 : 차례로 9.99별점의 댓글을 가져오면 한 웹툰에 치중된 정보를 모을수 있어서
## 별점이 9.9인것들중에서 랜덤으로 뽑아 데이터로 삼는다.
highstar_csv = csv[csv['star_point'].isin([9.99])]
highstar_csv = highstar_csv.sample(n=1000)
del highstar_csv['Unnamed: 0']

# 중복댓글 제거
highstar_csv = highstar_csv.drop_duplicates(["titleId","nom"],keep='first')

titleId_highlst = list(highstar_csv['titleId'])
nom_highlst = list(highstar_csv['nom'])

# 댓글이 들어갈 2차원 배열 선언
reply_list = []
for i in range(10):
    reply_list.append([])

for i in range(len(titleId_highlst)):
    aa = csv2[csv2['titleId'].isin([f'{titleId_highlst[i]}'])]
    bb = aa[aa['nom'].isin([f'{nom_highlst[i]}'])]

    for j in range(1, 11):
        try:
            reply_list[j - 1].append(str(bb[f'comment{j}'].values[0]))
        except:
            reply_list[j - 1].append('')
            # print('없는자료..')
            pass

for i in range(10):
    highstar_csv[f'comment{i+1}'] = reply_list[i]

idx = highstar_csv[highstar_csv['comment1']==''].index
highstar_csv = highstar_csv.drop(idx)
print(highstar_csv)
#500개의 데이터만 뽑는다.
highstar_csv = highstar_csv[:500 - len(highstar_csv)]
print(highstar_csv)
highstar_csv.to_csv("./highstar_reply.csv", encoding="utf_8_sig", mode='w')