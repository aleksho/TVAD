import os
import pandas as pd
import json
from tqdm import tqdm
import  shutil
from glob import glob
import time as tm

from constants import *
from src.utils import getConnection

LOGGING = True
LOG_FILE = './log/log_copy.log'
SAVE_DIR = '/home/oleg/temp'

def copyTest(configDict):
    """
    """
    imageDf = pd.DataFrame(columns = ['image_path', 'silence_id'])

    # Get image list from db
    brandDb = getConnection(
        host=configDict['masterHostname'],
        user=configDict['masterUser'],
        password=configDict['masterPassword'],
        database=configDict['masterDbname'],
        sshConnection=SSH_CONNECT, sshPort=SSH_PORT
    )
    brandDbCursor = brandDb.cursor()
    try:
        t0 = tm.time()
        print('Get silence list with SQL request.')
        query = f'''
        SELECT S.id, S.video_id, S.second, D.name, V.folder_name
        FROM vsilence AS S
        INNER JOIN vvideo as V
            ON S.video_id=V.id
        INNER JOIN dinfo as D
            ON V.device_id=D.id
        INNER JOIN adcatalog as A
            ON S.found_ad_id=A.ad_id
        INNER JOIN (
                SELECT id, file_time
                FROM (
                    SELECT id, SUBSTRING(filename, LOCATE('_202', filename), 7) as file_time FROM vvideo
                    ) AS Z
                    WHERE Z.file_time >= '_202202') as T
            ON S.video_id=T.id
        WHERE
            V.device_id = 5
            AND S.image_status = 2
        LIMIT 3000;'''
        brandDbCursor.execute(query)
        qryData = brandDbCursor.fetchall()
        print(f"Time taken: {tm.time() - t0}")
        silenceList = [{'id' : row[0], 'video_id' : row[1], 'second' : row[2], 'dev_name' : row[3], 'folder_name' : row[4]} for row in qryData]
        fileQnty = 0
        for silence in tqdm(silenceList, desc = 'Copy files'):
            for secondIdx in range(3):
                second = silence['second'] + secondIdx
                basePath = f"/var/www/sellavir.self/sofwebclient/frames/api/{silence['dev_name']}/{silence['folder_name']}/"

                # filename 104_21341_12.jpg consists of
                # 104   - second
                # 21341 - frame number
                # 12    - video_id
                imageName = f"{second}_*_{silence['video_id']}.jpg"
                filePattern = os.path.join(basePath, imageName)
                secondFiles = sorted(glob(filePattern))

                for imgFile in secondFiles:
                    filePath = imgFile
                    fileBasename = os.path.basename(filePath)
                    shutil.copy(filePath, os.path.join(SAVE_DIR, fileBasename))
                    fileQnty += 1

    except:
        print(f"__________ getSponsorImageList: some errors!")
    brandDbCursor.close()
    brandDb.close()
    print(f"{fileQnty} files are copied.")
    return


if __name__ == '__main__':
    currentDir = os.getcwd()
    configFile = os.path.join(currentDir, CONFIG_FILE)
    with open(configFile, 'r') as file:
        configDict = json.load(file)

    copyTest(configDict)



