# -*- coding: utf-8 -*-

import requests
import re
import os
import sys
import zipfile
import tarfile
from common.logsave import logger

url_binary="http://scdvstransfer.nvidia.com/dvsshare/vol1/gputelecom_rel_cuda10.1_r418_Release_Ubuntu16_04_AMD64_cuda.ran.release/"
url_src="http://scdvstransfer.nvidia.com/dvsshare/vol1/gputelecom_rel_cuda10.1_r418_Release_Ubuntu16_04_AMD64_cuphy.source.release/"
prefix_url="http://scdvstransfer.nvidia.com/"

headers = {
    #"Accept": "*/*",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding" : "gzip, deflate",
    "Accept-Language" : "en-US,en;q=0.9",
    "Cache-Control" : "max-age=0",
    "Connection" : "keep-alive",
    "Host" : "scdvstransfer.nvidia.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

def getdownloadlink(down_url):
    r = requests.get(url=down_url)

    pattern = re.compile(r'A HREF="\S+\.zip"', re.DOTALL)
    downlnk = ''
    pkgType = ''
    match = pattern.findall(r.content)
    for i in match[::-1]:
        templnk = i.split('=')[-1][1:-1]
        if templnk.endswith('.release.zip'):
            downlnk = ''.join([prefix_url, templnk])
            pkgType = templnk.split('.')[-3]
            targetFileName = templnk.split('/')[-1]
            return pkgType, downlnk, targetFileName

def downloadFile(url):
    pkgType, downlnk, targetFileName = getdownloadlink(url)

    targetFileNameAbsPath = os.path.join(os.getcwd(), targetFileName)

    if os.path.exists(targetFileNameAbsPath):
        logger.info('file %s exist, download ignore ...\n' % targetFileName)
    else:
        logger.info('start download cuda ran sdk pkgType={} ...\n'.format(pkgType))
        os.system('wget %s' % downlnk)
        logger.info('download cuda ran sdk done!\n')

    return pkgType, targetFileName

def getfilelist(path, filelist, endword):
    #print(path)
    if os.path.isfile(path) and path.endswith(endword):
        filelist.append(path)
    else:
        for i in os.listdir(path):
            if i.endswith(endword):
                filelist.append(i)

def pickcuRanPkg(filelist):
    file = ''
    ctime = 0.0
    for f in filelist:
        stat = os.stat(f)
        if stat.st_ctime > ctime:
            file = f
    return file

def extractZipFile(file_zip, path):
    with zipfile.ZipFile(file_zip) as zf:
        logger.info('start decompress cuda ran sdk ...\n')
        zf.extractall(path)
        return zf.namelist()[0]

def extractTarfile(file_tar, path):
    with tarfile.open(file_tar, 'r:gz') as tf:
        for tarinfo in tf:
            tf.extract(tarinfo.name, path)
    logger.info('decompress cuda ran sdk done\n')

def compilecuPHY_binary(cuda_ran_sdk):
    logger.info('start compile cuda ran sdk ...\n')
    currpath = os.getcwd()

    os.system("rm -rf %s/cuPHY/build" % cuda_ran_sdk)
    os.system("mkdir %s/cuPHY/build" % cuda_ran_sdk)
    libPath = os.path.join(currpath, '%s/cuPHY/lib:$LD_LIBRARY_PATH' % cuda_ran_sdk)
    newPath = os.path.join(currpath, '%s/cuPHY/build' % cuda_ran_sdk)

    #os.system('export PATH=/usr/local/cuda/bin:$PATH')
    #os.system('export LD_LIBRARY_PATH=%s:$LD_LIBRARY_PATH' % libPath)
    #sys.path.append('/usr/local/cuda/bin')

    os.chdir(newPath)
    os.system('cmake ..')
    os.system('make -j 44')
    os.chdir(currpath)

    logger.info('compile cuda ran sdk done\n')

def compilecuPHY_Src(cuda_ran_sdk):
    logger.info('start compile cuphy src ...\n')
    currpath = os.getcwd()

    os.system("rm -rf %s/build" % cuda_ran_sdk)
    os.system("mkdir %s/build" % cuda_ran_sdk)

    newPath = os.path.join(currpath, '%s/build' % cuda_ran_sdk)

    os.chdir(newPath)
    os.system('cmake ..')
    os.system('make -j 44')
    os.chdir(currpath)

    logger.info('\ncompile cuda ran sdk done\n')

def  doPrepare(existsdkfolder, args, pkgFolder):
    oldPath = os.getcwd()
    newPath = os.path.join(oldPath, pkgFolder)

    if (existsdkfolder != ''):
        return os.path.join(newPath, existsdkfolder)
    else:
        os.chdir(newPath)
        url = url_binary if args.pkg == 'binary' or args.pkg == 'stress' else url_src
        pkgType, targetZipfile = downloadFile(url)
        tempTGZFile = extractZipFile(targetZipfile, newPath)
        extractTarfile(tempTGZFile, newPath)
        newsdkFolder = tempTGZFile[0:-4]
        if args.pkg == 'binary' or args.pkg == 'stress':
            compilecuPHY_binary(newsdkFolder)
        else:
            compilecuPHY_Src(newsdkFolder)

        os.chdir(oldPath)
        return os.path.join(newPath, newsdkFolder)

def doPrepare_curanbinary(folder):
    currpath = os.getcwd()
    if (folder != ''):
        return os.path.join(currpath, folder)
    else:
        downloadFile(url=url_binary)
        filelist = []
        getfilelist(currpath, filelist, '.zip')
        filename = extractZipFile(filelist[0], currpath)
        extractTarfile(filename, currpath)
        #print('cuda_ran_sdk={}'.format(filename[0][0:-4]))
        compilecuPHY_binary(filename[0:-4])
        return os.path.join(currpath, filename[0:-4])

def doPrepare_curanSrc(folder):
    currpath = os.getcwd()
    if (folder != ''):
        return os.path.join(currpath, folder)
    else:
        downloadFile(url=url_src)
        filelist = []
        getfilelist(currpath, filelist, '.zip')
        filename = extractZipFile(filelist[0], currpath)
       
        extractTarfile(filename, currpath)
        #print('cuda_ran_sdk={}'.format(filename[0][0:-4]))
        compilecuPHY_Src(filename[0:-4])
        return os.path.join(currpath, filename[0:-4])


if __name__ == '__main__':
    r = requests.get(url=url_binary)

    pattern = re.compile(r'A HREF="\S+\.zip"', re.DOTALL)
    downlnk = ''
    pkgType = ''
    match = pattern.findall(r.content)
    for i in match[::-1]:
        templnk = i.split('=')[-1][1:-1]
        if templnk.endswith('.release.zip'):
            downlnk = ''.join([prefix_url, templnk])
            pkgType = templnk.split('.')[-3]
            targetFileName = templnk.split('/')[-1]
            print (targetFileName)
            targetFileNameAbsPath = os.path.join(os.getcwd(), targetFileName)
            print(os.path.exists(targetFileNameAbsPath))
