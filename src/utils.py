from PyQt5.QtWidgets import QApplication, QFileDialog
import pandas as pd
import sys

# response에 CSV 형식이 있는지 확인하고 있으면 저장하기
def save_to_csv(df):
    #app = QApplication(sys.argv)  # QApplication 인스턴스 생성

    file_path, _ = QFileDialog.getSaveFileName(
        None, 
        "Save File", 
        "", 
        "CSV Files (*.csv);;All Files (*)"
    )  # 파일 저장 대화상자 열기

    if file_path:
        df.to_csv(file_path, index=False, lineterminator='\n')
        return f'파일을 저장했습니다. 저장 경로는 다음과 같습니다.\n{file_path}\n'
    else:
        return '저장을 취소했습니다.'

# 주의: PyQt5 애플리케이션은 이 스크립트가 실행되는 환경에 따라 GUI를 띄울 수도 있고 띄울 수 없을 수도 있습니다.


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