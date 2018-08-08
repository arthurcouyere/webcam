#!/usr/bin/env python

import sys
import logging
import argparse
import dropbox
import os

# logging.basicConfig(format='%(asctime)-15s %(message)s')
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

# Get your app key and secret from the Dropbox developer website
ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'
FOLDER       = 'capture'

############################
# main
############################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='sync folder with dropbox')
    parser.add_argument('-v', action='store_true', help="verbose mode")
    args = parser.parse_args()
    if args.v:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    dbx  = dropbox.Dropbox(ACCESS_TOKEN)
    user = dbx.users_get_current_account()
    log.debug("user account = %s" % user.name.display_name)

    log.debug("syncing folder %s" % FOLDER)

    remoteFileList = []
    remotePath = FOLDER

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

    os.chdir(os.path.dirname(sys.argv[0]))
    localPath = FOLDER

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

