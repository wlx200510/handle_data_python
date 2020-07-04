#!/bin/env python3
# coding=utf-8
import os
import re
import shutil

PROJECT_PATH = 'projects'  # 根据实际情况灵活修改，尽量用绝对路径 如 /mnt/hdd4/project
BACK_UP_PATH = 'back_project'  # 要备份到到的磁盘目录 如 /mnt/hdd-backup/project-back
ALL_BACKUP_PATH = []  # 要输出的全部待备份的路径，会输出到 backupPath.txt 文件中


def getClass2DRoundFileName(round, childFilePath):  # childFilePath 是要遍历的文件夹
    # Class2D/job0**/和子文件夹：备份最后round轮run_it0**_classes.mrcs；
    allFilePath = [path for path in os.listdir(
        childFilePath) if os.path.isfile(childFilePath + os.sep + path) and (path.startswith('run_it') or path.startswith('run_ct')) and path.endswith('_classes.mrcs')]
    roundNumArr = []
    for fileName in allFilePath:
        roundNumArr.append(
            re.match(r'run_(.*?)it(\d+).*', fileName).groups(0)[1])
    roundNumArr = list(set(roundNumArr))
    roundNumArr.sort(key=lambda x: int(x), reverse=True)
    return [childFilePath + os.sep + fileName for fileName in allFilePath for num in roundNumArr[0:round] if fileName.find('_it' + num) != -1]


def getClass3DRoundFileName(childFilePath):
    # 备份最后5轮的star文件，和最后一轮的所有文件（star，mrc，blid);
    allFilePath = [path for path in os.listdir(
        childFilePath) if os.path.isfile(childFilePath + os.sep + path) and (path.startswith('run_it') or path.startswith('run_ct'))]
    roundNumArr = []
    for fileName in allFilePath:
        roundNumArr.append(
            re.match(r'run_(.*?)it(\d+).*', fileName).groups(0)[1])
    roundNumArr = list(set(roundNumArr))
    roundNumArr.sort(key=lambda x: int(x), reverse=True)
    # 获取最后一轮的备份文件
    latestBackupFiles = [childFilePath + os.sep +
                         latestPath for latestPath in allFilePath if latestPath.find('_it' + roundNumArr[0]) != -1]
    # 倒数2-5轮的备份文件
    otherBackupFiles = [childFilePath + os.sep +
                        starPath for starPath in allFilePath for order in roundNumArr[1:5] if starPath.endswith('.star') and starPath.find('_it' + order) != -1]

    return latestBackupFiles + otherBackupFiles


def getAllExtractFileName(childFilePath):
    allFilePath = [path for path in os.listdir(
        childFilePath) if os.path.isfile(childFilePath + os.sep + path) and not path.endswith('_extract.star')]
    return [childFilePath + os.sep + fileName for fileName in allFilePath]


def getJobPaths(currentChildPath):
    if os.path.exists(PROJECT_PATH + os.sep + currentChildPath):
        pathNameArr = os.listdir(PROJECT_PATH + os.sep + currentChildPath)
        curAbsPath = PROJECT_PATH + os.sep + currentChildPath + os.sep
        jobBackupArr = [
            jobPath for jobPath in pathNameArr if re.match(r'job\d+?$', jobPath) and os.path.isdir(curAbsPath + jobPath)]
        return [curAbsPath + backupPath for backupPath in jobBackupArr]
    else:
        return []


def setClass2dBackupFiles():
    class2DBackupArr = getJobPaths('Class2D')
    for backup in class2DBackupArr:
        ALL_BACKUP_PATH.extend(getClass2DRoundFileName(1, backup))


def setClass3dBackupFiles():
    class3DBackupArr = getJobPaths('Class3D')
    refine3DBackupArr = getJobPaths('Refine3D')
    for class3DFilePath in class3DBackupArr:
        ALL_BACKUP_PATH.extend(getClass3DRoundFileName(class3DFilePath))
    for refine3DFilePath in refine3DBackupArr:
        ALL_BACKUP_PATH.extend(getClass3DRoundFileName(refine3DFilePath))


def setExtractBackupFiles():
    extractBackupArr = getJobPaths('Extract')
    for extractFilePath in extractBackupArr:
        ALL_BACKUP_PATH.extend(getAllExtractFileName(extractFilePath))


def backupFiles(pathList):
   # 真正的复制备份操作！！
    for originPath in pathList:
        backupPath = originPath.replace(PROJECT_PATH, BACK_UP_PATH, 1)
        if not os.path.exists(os.path.dirname(backupPath)):
            os.makedirs(os.path.dirname(backupPath))
        shutil.copy(originPath, backupPath)


if __name__ == '__main__':
    if not os.path.exists(PROJECT_PATH):
        print('未找到放数据的文件夹:', PROJECT_PATH)
        exit(0)
    else:
        setClass2dBackupFiles()  # 跑Class2D文件夹
        setClass3dBackupFiles()  # 跑Class3D文件夹
        setExtractBackupFiles()  # 跑Extract文件夹

        with open('backupPath.txt', 'wt') as fout:
            fout.write('\n'.join(ALL_BACKUP_PATH))
        # backupFiles(ALL_BACKUP_PATH)
