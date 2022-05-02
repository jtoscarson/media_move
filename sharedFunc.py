from vars import LOG_LOCATION
import logging
from datetime import datetime
from os.path import join
from os import makedirs
from subprocess import Popen, PIPE, STDOUT

LOG_LOCATION = LOG_LOCATION()
logging.basicConfig(filename=LOG_LOCATION, level=logging.INFO)

def create_directory(PARENT_DIR, media_dir):
    des_path = join(PARENT_DIR, media_dir)
    if ".mkv" in des_path:
        logging.error(str(datetime.now()) + " - Error making parsing the file name: " + des_path)
    logging.info(str(datetime.now()) + " - Making Directory: " + des_path)
    try:
        makedirs(des_path)
    except:
        logging.warn(str(datetime.now()) + " - Directory Already Exists: " + des_path)
    return des_path

def rsync_file(source_path, des_path):
    logging.info(str(datetime.now()) + " - Copying file. Source: " + source_path + " Destination: " + des_path)
    process = Popen(['rsync', '-avzh', '--min-size=1', '--partial', source_path, des_path ], stdout=PIPE, stderr=STDOUT)
    with process.stdout:
        log_subprocess_output(process.stdout)
    logging.info(str(datetime.now()) + " - File Copied Successfully")
    return True

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info(str(datetime.now()) + ' - Rsync Logging: %r', line)