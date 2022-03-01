#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 11:42:15 2021

@author: ol
"""

import numpy as np
import mysql.connector
import os
import glob
import pandas as pd
from tqdm import tqdm
import csv
import zipfile
import fnmatch
SSH_CONNECT = False
SSH_PORT = 33360

configDict = {
    "masterDbname": "sofautolist",
    "masterHostname": "localhost",
    "masterUser": "adsearch",
    "masterPassword": "adsearch"
}


def getConnection(host, user, password, database, sshConnection = False, sshPort = 0):
    """
    Connect to the mysql db - to local base or via SSH connection

    Parameters
    ----------
    host : str
    user : str
    password : str
    database : str
    sshConnection : bool
        If True - need connection via SSH port.
    sshPort : int
        Connection port

    Returns
    -------
    coonnector

    """
    if sshConnection:
        dbConnector = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database,
            port = sshPort,
            use_pure = True
            )
    else:
        dbConnector = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database,
            )
    
    return dbConnector



def get_one_label(query_format = None, conf = None, csv_file_path = None, mode = 'a', columns = None ):
    # print(label)
    # conf['label'] = label
    brandDb = getConnection(
        host=configDict['masterHostname'],
        user=configDict['masterUser'],
        password=configDict['masterPassword'],
        database=configDict['masterDbname'],
        sshConnection=SSH_CONNECT, sshPort=SSH_PORT
    )
    brandDbCursor = brandDb.cursor()
    if conf is not None:
        query = query_format.format(**conf)
        # print(f"data fetchall {conf['label']}")
    else:
        query = query_format
    # print(query)
    # print(csv_file_path)
    brandDbCursor.execute(query)
    qryData = brandDbCursor.fetchall()
    brandDbCursor.close()
    brandDb.close()

    with open(csv_file_path, mode, newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if mode == 'w':
            csvwriter.writerow(columns)
        for row in qryData:
            csvwriter.writerow(row)


def get_image_path(basePath, second, secondIdx = 1):
    new_sec = int(second) + secondIdx
    imageName = f"{new_sec}_*.jpg"
    filePattern = os.path.join(basePath, imageName)
    # print(filePattern)
    secondFiles = sorted(glob.glob(filePattern))
    return secondFiles

def get_image_path2(basePath, second, secondIdx = 1):
    # print(f'get_image_path2 {basePath} {second}')
    new_sec = int(second) + secondIdx
    imageName = f"{new_sec}_*.jpg"
    base_dir = os.listdir(basePath)
    # filePattern = os.path.join(basePath, imageName)
    # print(filePattern)
    # secondFiles = sorted(glob.glob(filePattern))
    secondFiles = fnmatch.filter(base_dir, imageName)

    return secondFiles


def to_zip(file_csv = None, file_label= None,  file_zip= None ):
    with zipfile.ZipFile(file=file_zip, mode="w", ) as out_zip:
        out_zip.write(file_label, os.path.basename(file_label))
        with open(file_csv, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            columns = next(reader, None)
            for row in tqdm(reader):
                file_path = row[11]
                file_name = row[12]
                out_zip.write(file_path, file_name)
