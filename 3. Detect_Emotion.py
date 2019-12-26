## 감정분석
## 결과물 : titleid, nom, comment, emotion
## 긍정:true  부정:false
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import pandas as pd
import os

# 자신의 구글 클라우드 인증, 환경변수 설정
json_path = 'path/to/own.json'
high_csv_path = 'path/to/highstar_reply.csv'
low_csv_path = 'path/to/lowstar_reply.csv'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path
highstar_csv = pd.read_csv(high_csv_path)
lowstar_csv = pd.read_csv(low_csv_path)
client = language.LanguageServiceClient()

def emotion_detect(csvlist, filename):
    ## 2차원 배열 동적 선언
    emotion_lst = []
    for i in range(10):
        emotion_lst.append([])
    for i in range(1,11):
        txt_lst = list(csvlist[f'comment{i}'])

        for txt in txt_lst :
            document = types.Document(
                content=str(txt),
                type=enums.Document.Type.PLAIN_TEXT)
            try :
                # Detects the sentiment of the text
                sentiment = client.analyze_sentiment(document=document).document_sentiment
                score = sentiment.score
                if score >= 0.10 :
                    print('Text: {}'.format(txt))
                    print('Sentiment: {}'.format(score))
                    emotion_lst[i-1].append(True)
                else :
                    print('Text: {}'.format(txt))
                    print('Sentiment: {}'.format(score))
                    emotion_lst[i-1].append(False)
            except:
                print('오류! : 구글 클라우드에서 지원하지 않는 문자열입니다.')
                print('Text: {}'.format(txt))
                emotion_lst[i-1].append('추출불가')

    for i in range(1,11) :
        csvlist[f'comment{i}e'] = emotion_lst[i-1]
    print(csvlist)
    csvlist.to_csv(f"./{filename}", encoding="utf_8_sig", mode='w', index=True)

emotion_detect(lowstar_csv,'lowstar_emotion.csv')
emotion_detect(highstar_csv,'highstar_emotion.csv')