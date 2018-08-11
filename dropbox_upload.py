#!/usr/bin/env python

import sys
import logging
import configparser
import argparse
import dropbox
import os

############################
# configuration
############################

configFile="dropbox_upload.ini"

# logging.basicConfig(format='%(asctime)-15s %(message)s')
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

############################
# main
############################
if __name__ == '__main__':

    # get current dir
    currentDir = os.path.dirname(sys.argv[0])

    # parse args
    parser = argparse.ArgumentParser(description='sync folder with dropbox')
    parser.add_argument('-v', action='store_true', help="verbose mode")
    args = parser.parse_args()
    if args.v:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try :
        # read config file
        log.debug("reading config file : %s" % configFile)
        config = configparser.ConfigParser()
        with open(os.path.join(currentDir, configFile)) as f:
            config.read_file(f)

        # read config
        accessToken  = config['general']['accessToken']
        syncFolder   = config['general']['syncFolder']

    except Exception as err:
        print("ERROR reading %s : %s" % (configFile, err))
        sys.exit(1)

    
    log.debug("access token = [%s]" % accessToken)
    dbx  = dropbox.Dropbox(accessToken)
    user = dbx.users_get_current_account()
    log.debug("user account = %s" % user.name.display_name)

    log.debug("syncing folder %s" % syncFolder)

    remoteFileList = []
    remotePath = syncFolder

    try:
        log.debug("liste remote folder : %s" % remotePath)
        res = dbx.files_list_folder(os.path.join("/", remotePath))

        for entry in res.entries:
            remoteFilePath = os.path.join(remotePath, entry.name)
            log.debug("remote file found : %s" % remoteFilePath)
            remoteFileList.append(remoteFilePath)

    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', remotePath, '-- assumed empty:', err)
        sys.exit(1)

    os.chdir(currentDir)
    localPath = syncFolder

    for localFileName in os.listdir(localPath):
        localFilePath = os.path.join(localPath, localFileName)
        if os.path.isfile(localFilePath):
            log.debug("local file found  : %s" % localFilePath)

            if localFilePath in remoteFileList:
                log.debug("file already copied on remote : %s" % localFilePath)
            else:
                log.info("copying file on remote : %s" % localFilePath)

                with open(localFilePath, 'rb') as f:
                    data = f.read()

                res = dbx.files_upload(data, os.path.join("/", localFilePath), mode=dropbox.files.WriteMode.overwrite)

