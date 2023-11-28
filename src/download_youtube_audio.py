import pandas as pd
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
import os
import re

def download_youtube_audio(csv_file_path, download_directory='downloads'):
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path, delimiter=',')

    # 다운로드할 디렉토리 설정
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # yt-dlp 설정
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': download_directory + '/%(title)s.%(ext)s',
    }

    ## 각 행에 대해 유튜브 검색 및 다운로드
    for index, row in df.iterrows():
        song_title = row['Title']
        song_artist = row['Artist']
        search_query = f"{song_title} {song_artist}"
        video_search = VideosSearch(search_query, limit=1)

        try:
            video_info = video_search.result()['result'][0]
            video_url = video_info['link']
            video_title = video_info['title']

            # 검색된 영상 제목이 유효한지 확인
            if is_valid_video_title(song_title, song_artist, video_title):
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])

        except Exception as e:
            print(f"Error downloading {search_query}: {e}")


def is_valid_video_title(search_title, search_artist, video_title):
    '''
    소문자로 변환하여 비교하는 함수
    '''
    search_title = search_title.lower()
    search_artist = search_artist.lower()
    video_title = video_title.lower()

    # 제목과 아티스트가 유튜브 영상 제목에 모두 포함되어 있는지 확인
    return search_title in video_title and search_artist in video_title


def sanitize_filename(filename):
    '''
    파일명에서 부적절한 문자를 제거하고 공백 문자를 대체하는 함수
    '''
    return re.sub('[\\\\/:*?"<>|', '', filename).replace(' ','_')

# # 사용 예시
# search_title = "This Christmas"
# search_artist = "Taeyeon"
# video_title = "Taeyeon - This Christmas (Official Video)"

# if is_valid_video_title(search_title, search_artist, video_title):
#     print("Valid video title")
# else:
#     print("Invalid video title")

# 실행 소스 코드
# if __name__ == "__main__":
    
#     csv_file_path = '../성공.csv'
#     download_directory = '../downloads/'
#     #download_directory = download_directory or 'downloads'
#     download_youtube_audio(csv_file_path, download_directory)