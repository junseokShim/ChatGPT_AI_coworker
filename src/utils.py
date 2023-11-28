from PyQt5.QtWidgets import QApplication, QFileDialog
import pandas as pd
import sys


def save_to_csv(df):
    
    file_path, _ = QFileDialog.getSaveFileName(
        None, 
        "Save File", 
        "", 
        "CSV Files (*.csv);;All Files (*)"
    )  # 파일 저장 대화상자 열기

    if file_path:
        print(df)
        df.to_csv(file_path, index=False, lineterminator='\n')
        return f'파일을 저장했습니다. 저장 경로는 다음과 같습니다.\n{file_path}\n 이 플레이리스트의 음원을 내려받으시겠습니까?', file_path

    else:
        return '저장을 취소했습니다.', None


def extract_csv_to_dataframe(response):

    if ";" in response:
        response_lines=response.strip().split("\n")
        csv_data=[]
        for line in response_lines:
            if ";" in line:
                csv_data.append(line.split(";"))
        if len(csv_data) > 0:
            df=pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return df
        else:
            return None
    else:   
        return None


def save_playlist_as_csv(playlist_csv):
    '''
    save playlists using function call
    '''
    if ";" in playlist_csv:
        lines = playlist_csv.strip().split("\n")
        csv_data = []

        for line in lines:
            if ";" in line:
                csv_data.append(line.split(";"))

        if len(csv_data)>0:
            df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return save_to_csv(df)

    return f"저장에 실패했습니다. \n저장에 실패한 내용은 다음과 같습니다. \n{playlist_csv}"