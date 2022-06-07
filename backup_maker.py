import datetime
import os
import subprocess
import time

import schedule
from google_drive_downloader import GoogleDriveDownloader as gdd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def make_backup():
    day_of_month = datetime.datetime.now().day
    if (1 < day_of_month < 15) or day_of_month > 21:

        gdd.download_file_from_google_drive(file_id='1qX8fBNA9zSpDCkuvGoAbarnnEbkleRHW',
                                            dest_path='./credentials.json',
                                            unzip=True)

        gauth = GoogleAuth()

        gauth.LoadCredentialsFile("credentials.json")
        time.sleep(10)
        gauth.Refresh()

        drive = GoogleDrive(gauth)

        subprocess.run(["heroku", "pg:backups:download"])

        upload_file_list = ['latest.dump']
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'title': upload_file, 'parents': [{'id':  os.environ['FOLDER_ID']}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()
        subprocess.run(["rm", "-rf", "latest.dump"])
        subprocess.run(["rm", "-rf", "credentials.json"])


schedule.every().wednesday.do(make_backup)

# schedule.every(10).seconds.do(make_backup)

while True:
    schedule.run_pending()
    time.sleep(1)

# Restore command
# subprocess.run(["heroku", "pg:backups:restore", 'https://drive.google.com/uc?id=1UCwErrCtrOkBRmKEXTt6i7Qg40LxJ8z1&export=download', "DATABASE_URL", "--confirm", "silk-travel"])
