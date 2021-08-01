import ftplib
import json
import os
import re
from datetime import datetime



# some utility functions that we gonna need
from config import FTP_HOST, FTP_USER, FTP_PASS


def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024


def get_datetime_format(date_time):
    # convert to datetime object
    date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
    # convert to human readable date time string
    return date_time.strftime("%Y/%m/%d %H:%M:%S")

import sys
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def list_dir_ftp_json(directory):
    # initialize FTP session
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

    # force UTF-8 encoding
    ftp.encoding = "utf-8"

    # print the welcome message
    # print(ftp.getwelcome())

    # change the current working directory to 'pub' folder and 'maps' subfolder
    ftp.cwd(directory)

    current_dir = ftp.pwd()
    print("current_dir: ", current_dir)
    # print("directory: ", directory)
    # ftp.cwd("..")
    # print(ftp.pwd())
    # ftp.cwd(directory)
    # print(ftp.pwd())

    # LIST a directory
    # print("*"*50, "LIST", "*"*50)
    # ftp.dir()

    # filename =  '/Users/vincent/PycharmProjects/ReadDirToJSON/list_dir_ftp_json.txt'
    # filename =  '/Users/vincent/PycharmProjects/ReadDirToJSON' + current_dir + '.json'
    filename = '/Users/vincent/PycharmProjects/ReadDirToJSON/' + current_dir.replace("/", "_") + '.json'
    result = {}
    urlhomepath = 'http://www.eole-ns.com'

    # NLST command

    # print("*"*50, "NLST", "*"*50)
    # print("{:20} {}".format("File Name", "File Size"))
    for file_name in ftp.nlst():
        file_size = "N/A"
        # print(file_name)
        try:
            ftp.cwd(file_name)
        except Exception as e:
            # ftp.voidcmd("TYPE I")
            file_size = get_size_format(ftp.size(file_name))

        pattern = r'([\w\.\-\ \_\?\(\)]+\.(?:' + 'jpg|png|bmp|JPG|jpeg|JPEG' + '))'
        images = re.match(pattern, file_name)
        if images != None:
            # print(f"{file_name:20} {file_size}")
            dir_elm = splitall(current_dir)
            result[file_name] = {
                "file_name": file_name,
                "url": urlhomepath + current_dir + "/" + file_name,
                "name": "",
                "directory": current_dir,
                "category": dir_elm,
                "date": "",
                "description": "",
                "file_size": file_size
            }
        ftp.cwd(current_dir)
        # ftp.cwd(directory)

    '''
    # using the MLSD command
    print("*"*50, "MLSD", "*"*50)
    print("{:30} {:19} {:6} {:5} {:4} {:4} {:4} {}".format("File Name", "Last Modified", "Size", "Perm","Type", "GRP", "MODE", "OWNER"))
    
    for file_data in ftp.mlsd():
        # extract returning data
        file_name, meta = file_data
        # i.e directory, file or link, etc
        file_type = meta.get("type")
        if file_type == "file":
            # if it is a file, change type of transfer data to IMAGE/binary
            ftp.voidcmd("TYPE I")
            # get the file size in bytes
            file_size = ftp.size(file_name)
            # convert it to human readable format (i.e in 'KB', 'MB', etc)
            file_size = get_size_format(file_size)
        else:
            # not a file, may be a directory or other types
            file_size = "N/A"
        # date of last modification of the file
        last_modified = get_datetime_format(meta.get("modify"))
        # file permissions
        permission = meta.get("perm")
    
        # get the file unique id
        unique_id = meta.get("unique")
        # user group
        unix_group = meta.get("unix.group")
        # file mode, unix permissions
        unix_mode = meta.get("unix.mode")
        # owner of the file
        unix_owner = meta.get("unix.owner")
        # print all
        print(f"{file_name:30} {last_modified} {file_size:7} {permission:5} {file_type:4} {unix_group:4} {unix_mode:4} {unix_owner}")
    '''

    # quit and close the connection
    ftp.quit()

    json_res = json.dumps(result, indent=2)
    print(json_res)

    with open(filename, 'w') as fp:
        fp.write(json_res)


def list_dir(directory):
    # initialize FTP session
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

    # force UTF-8 encoding
    ftp.encoding = "utf-8"

    # print the welcome message
    # print(ftp.getwelcome())

    # change the current working directory to 'pub' folder and 'maps' subfolder
    ftp.cwd(directory)
    current_dir = ftp.pwd()
    print("current_dir: ", current_dir)
    # print("directory: ", directory)
    # LIST a directory
    print("*" * 50, "LIST", "*" * 50)
    ftp.dir()


create_json_file = 'y'
see_directory = "y"
while True:
    while True:
        see_directory = input("to see the list of files? (y/n): ")
        if see_directory == 'n': break
        elif see_directory == 'y':
            directory = input("which directory? : ")
            list_dir(directory=directory)
        else:
            continue

    create_json_file = input("to create a json file? (y/n): ")
    if create_json_file == 'n':
        print("Bye!")
        break
    elif create_json_file == 'y':
        directory_to_json = input("which directory to create a json file for the list of image files? : ")
        list_dir_ftp_json(directory_to_json)
    else:
        continue
