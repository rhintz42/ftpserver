#!/usr/bin/python
import argparse
import subprocess
import os


def download(url, outfile, settings):
    subprocess.check_call(['curl', url, '-o', outfile])
    full_path = os.path.abspath(outfile)
    return full_path


def init_arg_parser():
    parser = argparse.ArgumentParser()

    # parser.add_argument('-d', '--download', nargs='+')
    parser.add_argument('-d', '--download')
    parser.add_argument('-o', '--outfile')

    # Be able to provide file to parse
    # parser.add_argument('-f', '--file')

    # Add ways of saying directory on ftp server to goto

    return parser


def parse_arg_input(parser):
    args = parser.parse_args()

    return args


def get_actions(args, settings):
    actions = []
    if args.__contains__('download'):
        actions.append((download, args.download, args.outfile, settings))
        
    return actions


def main():
    # TODO: Check to make sure that the server is configured and currently
    #   running
    settings = {
        'ftp_dir': '/mnt/pub',
    }

    parser = init_arg_parser()
    args = parse_arg_input(parser)
    
    action = get_actions(args, settings)

if __name__ == '__main__':
    main()
