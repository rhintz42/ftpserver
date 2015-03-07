#!/usr/bin/python
import argparse
import subprocess
import os
import shutil
from ftplib import FTP

supported_extensions = ('.mp4', '.flv', '.pdf', '.txt')


# TODO
#class FTPServer(object):


def download_youtube_video(url, outfile):
    print("\nDownloading Youtube Video: %s" % (outfile))
    subprocess.check_call(['youtube-dl', url, '-o', outfile])
    full_path = os.path.abspath(outfile)
    print("\nFinished Downloading Youtube Video Here: %s" % (full_path))

    return full_path


def is_youtube_video(url):
    youtube_prefix = 'https://www.youtube.com/'
    if url[0:len(youtube_prefix)] == youtube_prefix:
        return True
    return False


def outfile_has_supported_extension(outfile):
    for se in supported_extensions:
        if outfile[-len(se):] == se:
            return True
    return False


def is_relative_path(outfile):
    return len(outfile) >= 0 and outfile[0] != '/'


def download(url, outfile):
    if is_youtube_video(url):
        full_path = download_youtube_video(url, outfile)
    else:
        print("\nDownloading Normal Video: %s" % (outfile))
        subprocess.check_call(['curl', '-L', url, '-o', outfile])
        full_path = os.path.abspath(outfile)
        print("\nFinished Downloading Normal Video Here: %s" % (full_path))

    return full_path


def init_arg_parser():
    parser = argparse.ArgumentParser()

    # parser.add_argument('-d', '--download', nargs='+')
    parser.add_argument('url', nargs='?')
    parser.add_argument('filename', nargs='?')
    parser.add_argument('-d', '--download', action='store_true')
    parser.add_argument('-o', '--outfile')
    parser.add_argument('-f', '--file')
    parser.add_argument('-t', '--type')

    # Be able to provide file to parse
    # parser.add_argument('-f', '--file')

    # Add ways of saying directory on ftp server to goto

    return parser


def parse_arg_input(parser):
    args = parser.parse_args()

    return args


def parse_settings(file_path):
    pass


def ftp_init_connection(settings):
    pass


def ftp_upload_video(local_file_path, remote_file_name='', remote_file_dir=''):
    local_filename = local_file_path.split('/')[-1]

    print("Connecting to FTP")
    ftp = FTP(### PUT SERVER AND SUCH INFO HERE)
    local_file = open(local_file_path, 'rb')

    print("Uploading video up on ftp server")
    ftp.storbinary('STOR %s/%s' %(remote_file_dir, local_filename), local_file)

    print("Finished uploading video")
    local_file.close()
    ftp.close()
    print("Closing Connection to FTP server")

def execute_command(command):
    tokens = command.split()
    
    type_ = tokens[0]
    url = tokens[1]
    outfile = tokens[2]

    if is_relative_path(outfile):
        outfile = "/tmp/%s" % outfile

    download(url, outfile)

    executed_commands_file = open('executed_commands.txt', 'a')
    executed_commands_file.write(command)
    executed_commands_file.close()

    ftp_upload_video(outfile, remote_file_dir='/Media_Drive/shows_to_watch')


def execute_file_commands(filepath, num_to_execute=None):
    while True:
        with open(filepath, 'r+') as commands_to_execute_file:
            commands = commands_to_execute_file.readlines()
            if len(commands) == 0:
                return
            command = commands[0]
            commands_to_execute_file.seek(0)
            commands_to_execute_file.write(''.join(commands[1:]))
            commands_to_execute_file.truncate()
            if command.isspace():
                continue
        execute_command(command)


def main():
    # TODO: Check to make sure that the server is configured and currently
    #   running
    settings = {
        'ftp_dir': '/mnt/pub',
    }

    parser = init_arg_parser()
    args = parse_arg_input(parser)

    if args.__contains__('file') and args.file:
        execute_file_commands(args.file)
    
    """
    # Get Settings (like the outfile)
    outfile = None
    if args.__contains__('outfile'):
        outfile = args.outfile
    if outfile is None:
        outfile = args.filename

    # Do actions (Like download)
    files_to_download = []
    if args.__contains__('download'):
        # Should change the download option to url
        files_to_download.append(args.url)

        download(files_to_download[0], outfile)
    """

if __name__ == '__main__':
    main()
