# reply_crawling
## py files
- 1. Crawling.py : 웹툰 정보 크롤링 과정 코드
- 2. Preprocess.py : 웹툰을 별점 별로 나누는 전처리 과정 코드
- 3. Detect_Emotion.py : 구글 감정분석 모델을 이용해 댓글의 내용을 감정분석하고 저장하는 전처리 코드
- 4. Emotion_Classification.py : 댓글의 긍정/부정 별로 파일을 나누고, 각 웹툰의 정보를 시각화하는 코드
- 5. Make_wordcloud.py : 앞서 만든 긍정/부정 댓글을 종합해 워드클라우드를 만드는 코드

## csv files
- weebtoon_info.csv : 웹툰 정보가 담긴 파일. (이름, 주소, 고유번호, 화번호, 조회수순위)
- weebtoon_star_info.csv : 웹툰 정보 + 각 화별 별점 정보
- weebtoon_reply_info.csv : 웹툰 정보 + 각 화별 댓글 정보
- lowstar_reply.csv / highstar_reply.csv : 별점이 낮은 웹툰의 정보 , 별점이 높은 웹툰의 정보 (각 500화씩)
- lowstar_emotion.csv / highstar_reply.csv : 별점이 낮은 웹툰의 감정 정보, 별점이 높은 웹툰의 감정정보 (각 5000댓글)
- lowstar_comment_False(부정),Treu(긍정) / highstar_comments_False,True(긍정) : 높은 별점, 낮은 별점별로 긍정적, 부정적 반응의 댓글을 따로 모은 파일.

## png files
> 시각화파일들

-rank_bar.png : 낮은별점 / 높은 별점의 조회수 순위 평균 시각화
-PNcount.png : 낮은별점, 높은별점의 긍정,부정별 댓글 갯수 시각화
-person_bar.png : 낮은별점, 높은별점의 별점 참여자 평균 시각화
-starpoint_bar.png : 낮은별점, 높은별점의 평균 별점 시각화
