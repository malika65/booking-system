import datetime
import time

import schedule
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import subprocess


def make_backup():
    day_of_month = datetime.datetime.now().day
    if (1 < day_of_month < 15) or day_of_month > 21:
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        subprocess.run(["heroku", "pg:backups:download"])

        upload_file_list = ['latest.dump']
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'title': upload_file, 'parents': [{'id': '1R10r7X_zmdsokfbIwZk8MxG5ces46mR2'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()
        subprocess.run(["rm", "-rf", "latest.dump"])


schedule.every().saturday.do(make_backup)

# schedule.every(10).seconds.do(make_backup)

while True:
    schedule.run_pending()
    time.sleep(1)

# Restore command
# subprocess.run(["heroku", "pg:backups:restore", 'https://drive.google.com/uc?id=1UCwErrCtrOkBRmKEXTt6i7Qg40LxJ8z1&export=download', "DATABASE_URL", "--confirm", "silk-travel"])
