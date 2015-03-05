#!/usr/bin/python
import argparse
import subprocess
import os

supported_extensions = ('.mp4', '.flv', '.pdf', '.txt')


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
    parser.add_argument('url')
    parser.add_argument('filename', nargs='?')
    parser.add_argument('-d', '--download', action='store_true')
    parser.add_argument('-o', '--outfile')

    # Be able to provide file to parse
    # parser.add_argument('-f', '--file')

    # Add ways of saying directory on ftp server to goto

    return parser


def parse_arg_input(parser):
    args = parser.parse_args()

    return args


def main():
    # TODO: Check to make sure that the server is configured and currently
    #   running
    settings = {
        'ftp_dir': '/mnt/pub',
    }

    parser = init_arg_parser()
    args = parse_arg_input(parser)
    
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

if __name__ == '__main__':
    main()
