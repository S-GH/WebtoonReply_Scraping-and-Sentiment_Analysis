from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
## 주의 : 예상 크롤링 시간 5~7시간 ##

#웹 페이지를 열고 소스코드 읽음
html = requests.get('http://comic.naver.com/webtoon/weekday.nhn')
soup = BeautifulSoup(html.text, 'html.parser')
html.close()
#요일별 웹툰 검색
data_list = soup.findAll('div',{'class':'col_inner'})
list = []
#각 웹툰별 링크 검색
for data in data_list:
    list.extend(data.findAll('li'))
list1 = []
for data in list :
    list1.extend(data.findAll('a',{'class':'title'}))
Tadress_list = []
for data in list1 :
    Tadress_list.append('https://comic.naver.com'+data.attrs['href'])
## Id 리스트선언
TtitleId_list = []

for address in Tadress_list :
    TtitleId_list.append(address[address.find('titleId')+8:address.find('&weekday')])

### 각종 list 선언
Tname_list = [] # 웹툰제목 ex) 신의 탑
Tlatestepi_list = [] # 웹툰최신화번호 ex) 483=
Trank_list = [] ## 웹툰 요일별 조회수순위 저장
rank_var = 1 # 요일별 순위 저장
temp_day = ['mon','mon']

############# step 1 : 웹툰별 웹툰제목, 주소, 최신화, 웹툰순위 csv파일 만들기 ##################
for req in Tadress_list :
    nhtml = requests.get(req)
    soup = BeautifulSoup(nhtml.text, 'html.parser')

    ### 1. 만화 제목 저장
    name = str(soup.findAll('title')[0].string)
    # ex) '신의 탑 :: 네이버 만화' 라고 저장되기때문에 필요없는 뒤의부분 :: 네이버만화를 지워준다.
    Tname_list.append(name[0:name.find(':')-1])

    #### 2. 최신화 number 저장
    a = soup.findAll('a')
    # 웹툰의 최신화 링크를 찾아서 링크안의 번호를 추출.
    comp = '/webtoon/detail.nhn?' + req[req.find('titleId'):-12] + '&no='
    for i in a :
        late_link = str(i.attrs['href'])
        if comp == late_link[0:len(comp)]:
            no = str(i.attrs['href'])
            # 주소의 구조가 /webtoon/detail.nhn?titleId=183559&no=458&weekday=mon
            # 이런식이여서 str의 'no='뒤의 번호를 구해야함. list를 'no=' , 'weekday' 기준으로 slice하여 최신화를 구한다.
            Tlatestepi_list.append(no[no.find('no=')+3:no.find('weekday')-1])
            break

    ### 3. 웹툰의 요일별 조회수 순위 저장.
    temp_day[0] = temp_day[1]
    temp_day[1] = req[req.find('weekday') + 8:]

    if temp_day[0] != temp_day[1] :
        rank_var = 1
        Trank_list.append(rank_var)
        rank_var = rank_var + 1
    else :
        Trank_list.append(rank_var)
        rank_var = rank_var + 1

    print('step 1 크롤링중...'+req)


DataFramelist = []
col = ['title','titleID','html','latest','rank']
for i in range(len(Tname_list)):
    DataFramelist.append([Tname_list[i]] + [TtitleId_list[i]] +[Tadress_list[i]]\
                         + [Tlatestepi_list[i]] + [Trank_list[i]])

## 첫번째 테이블 저장 열 : 웹툰이름, 웹툰Id, 웹툰주소, 최신화, 웹툰순위
table = pd.DataFrame(DataFramelist, columns=col)
table.to_csv("./weebtoon_info.csv", encoding="cp949", mode='w', index=True)
print('FINISHED')


############# step 2: step1의 주소를 활용해 각 화별 별점,별점 참여자수,댓글 크롤링 ##################
DataFramelist2 = []
cnt = 0

for titleId in TtitleId_list :
    for no in range(1,int(Tlatestepi_list[cnt])+1) :
        reqq = f'https://comic.naver.com/webtoon/detail.nhn?titleId={titleId}&no={no}&weekday=mon'
        print(reqq)
        try :
            nnhtml = requests.get(reqq)
            soup = BeautifulSoup(nnhtml.text, 'html.parser')
            starPoint = soup.find_all('span',{'id':'topPointTotalNumber'})
            starPerson = soup.find_all('span', {'class': 'pointTotalPerson'})
            DataFramelist2.append([titleId] + [no] + [starPoint[0].string] + \
                                  [starPerson[0].find('em').string])
        except :
            pass
        print('step 2 크롤링중...' + str(titleId) + ' ' + str(no))
    cnt = cnt + 1

## 두번째 테이블 저장 열 : 웹툰Id, 웹툰화별 번호, 웹툰별점, 웹툰별점 참여자수
col2 = ['titleId','nom','star_point','star_person']
table2 = pd.DataFrame(DataFramelist2, columns=col2)
table2.to_csv("./weebtoon_star_info.csv", encoding="cp949", mode='w', index=True)
print('FINISHED')

########### step 3: step2로 크롤링한 데이터를 종합해 csv파일 만들기  ##############
## csv파일은 2개 : 별점+별점참여자수 테이블, 댓글 테이블
## 댓글찾기 3번째 테이블 댓글 10개씩 받아서 10행 + ID, no 2행으로 총 12행
## 별점 + 별점참여자수 2번째 테이블 ID,no,별점,참여자수 총 4행

DataFramelist3 = []

for i in range(len(TtitleId_list)):
    titleId = TtitleId_list[i]
    latest_nom = int(Tlatestepi_list[i])
    for j in range(latest_nom):
        print(f'step3 크롤링중... {titleId} ,{latest_nom - j}' + '화')
        # api 옵션
        obj = f'{titleId}' + '_' + f'{latest_nom - j}'
        # 셀레니움을 사용해도되지만 api가 더빠르기때문에 이것을 사용.
        # 네이버 웹툰 댓글 수집 api
        # pageSize=15&indexSize=10&groundId=&listType=OBJECT&sort=BEST *중요*
        u = 'http://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=comic&templateId=webtoon&pool=cbox3&_callback=jQuery1113012327623800394427_1489937311100&lang=ko&country=KR&objectId=' + obj + '&categoryId=&pageSize=15&indexSize=10&groundId=&listType=OBJECT&sort=BEST&_=1489937311112'
        comment_url = u + '&page=' + '1'
        header = {
            'Host': 'apis.naver.com',
            'Referer': 'https://comic.naver.com/comment/comment.nhn?titleId=' + '1' + '&no=1',
            'Content-Type': 'application/javascript'
        }

        res = requests.get(comment_url, headers=header)
        soup = BeautifulSoup(res.content, 'lxml')

        try:
            content_text = soup.select('p')[0].text
            one = content_text.find('(') + 1
            two = content_text.find(');')
            content = json.loads(content_text[one:two])
            comments = content['result']['commentList']
            comment_list = []
            DataFramelist3.append([titleId] + [latest_nom - j] + [comments[0]['contents']] + [comments[1]['contents']] + \
                                  [comments[2]['contents']] + [comments[3]['contents']] + [comments[4]['contents']] + \
                                  [comments[5]['contents']] + [comments[6]['contents']] + [comments[7]['contents']] + \
                                  [comments[8]['contents']] + [comments[9]['contents']])
        except :
            pass

## 세번째 테이블 열: 웹툰Id, 웹툰 화별 번호, 코맨트 위에서부터 1~10
col3 = ['titleId', 'nom', 'comment1', 'comment2', 'comment3', 'comment4', 'comment5', 'comment6', 'comment7' \
    , 'comment8', 'comment9', 'comment10']
table3 = pd.DataFrame(DataFramelist3, columns=col3)
table3.to_csv("./weebtoon_reply_info.csv", encoding="utf_8_sig", mode='w', index=True)
print('FINISHED')