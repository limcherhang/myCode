import os
import sys
rootPath = os.getcwd()
sys.path.append(rootPath)
import configparser
import pandas as pd
import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io

from connection.mysql_connection import MySQLConn
from utils.util import get_logger

def authenticate(service_file, scopes):
    creds = service_account.Credentials.from_service_account_file(service_file, scopes=scopes)
    return creds

def create_or_get_folder(service, parent_id, folder_path):
    folder_query = f"name='{folder_path}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents"
    folders = service.files().list(q=folder_query, fields='files(id)').execute().get('files', [])

    if not folders:
        # 文件夹不存在，创建它
        folder_metadata = {
            'name': folder_path,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        return folder['id']
    else:
        # 文件夹存在，返回其 ID
        return folders[0]['id']

def upload_file(filename, service_file, scopes, parent_folder_id, filePath='/'):
    creds = authenticate(service_file, scopes)
    service = build('drive', 'v3', credentials=creds)

    # 创建或获取目标文件夹的 ID
    folder_id = create_or_get_folder(service, parent_folder_id, filePath)

    # 打开文件并上传
    try:
        with open(filename, 'rb') as file_content:
            media = MediaIoBaseUpload(file_content, mimetype='application/octet-stream')

            file_metadata = {
                "name": filename,
                "parents": [folder_id]
            }

            file = service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()

        logger.info(f"File '{filename}' uploaded to folder '{filePath}' with ID: {file['id']}")
    except Exception as ex:
        logger.error(f"Upload failed, message: {ex}")
    # print(f'File "{filename}" uploaded to folder "{filePath}" with ID: {file["id"]}')



if __name__ == '__main__':
    
    file = __file__
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    logPath = os.getcwd()+ '/log'

    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    conn = MySQLConn(config['mysql_azureV2'])

    logger = get_logger(logPath, f"{filename}.log")

    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'Credentials.json'
    PARENT_FOLDER_ID = "1eMhegtGSMT1eeh9xyOyzP-QlJ_e8tUGr"

    upload_file('result_14200000.csv', SERVICE_ACCOUNT_FILE, SCOPES, PARENT_FOLDER_ID, 'test')

