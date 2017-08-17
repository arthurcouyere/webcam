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

configFile="dropbox_download.ini"

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

    os.chdir(currentDir)

    # create local folder if missing
    if not os.path.exists(syncFolder):
        log.info("creating folder : %s" % syncFolder)
        os.makedirs(syncFolder)

    try:
        # read remote folder content
        log.debug("liste remote folder : %s" % remotePath)
        res = dbx.files_list_folder(os.path.join("/", remotePath))

        # sync files
        for entry in res.entries:
            remoteFilePath = os.path.relpath(entry.path_display, "/")
            log.debug("remote file found : %s" % remoteFilePath)

            # sync file if not locally present
            if os.path.isfile(remoteFilePath):
                log.debug("skipping file     : %s" % remoteFilePath)
            else:
                log.info("downloading file  : %s" % remoteFilePath)
                res = dbx.files_download_to_file(remoteFilePath, entry.path_display)

    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', remotePath, '-- assumed empty:', err)
        sys.exit(1)

