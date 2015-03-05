import pytest
import mock
from argparse import Namespace


def test_init_arg_parser__basic_outfile_initialized():
    from ftpserver import init_arg_parser

    with mock.patch('ftpserver.argparse') as ap:
        ap.ArgumentParser.return_value = mock.Mock()
        parser = init_arg_parser()

    assert parser.add_argument.call_args[0] == ('-o', '--outfile')


def test_parse_arg_input__basic():
    from ftpserver import parse_arg_input

    args = Namespace(download='http://www.google.com')

    parser_mock = mock.Mock()
    parser_mock.parse_args.return_value = args

    result_args = parse_arg_input(parser_mock)

    assert result_args.download == args.download


def test_get_actions__basic():
    from ftpserver import get_actions
    from ftpserver import download as download_func

    args = Namespace(download='http://www.google.com', outfile='google.html')
    settings = {'ftp_dir': '/mnt/pub'}

    actions = get_actions(args, settings)

    assert actions[0] == (download_func, args.download, args.outfile, settings)


@pytest.mark.integration
def test_download__basic():
    from ftpserver import download

    url = 'http://www.google.com'
    outfile = 'google.html'
    settings = {'ftp_dir': '/mnt/pub'}

    result = download(url, outfile, settings)

    assert result[-len(outfile):] == outfile
    assert len(result) > len(outfile)
    assert result[0] == '/'


@pytest.mark.integration
def test_download__provide_full_path_for_outfile():
    """
    NOTE: Your tmp folder must be writable
    """
    from ftpserver import download

    url = 'http://www.google.com'
    outfile = '/tmp/google.html'
    settings = {'ftp_dir': '/mnt/pub'}

    result = download(url, outfile, settings)

    assert result == outfile
