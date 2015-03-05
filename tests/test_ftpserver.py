import pytest
import mock
import os   
import subprocess
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


@pytest.mark.integration
def test_download__basic():
    from ftpserver import download

    url = 'http://www.google.com'
    outfile = 'google.html'

    result = download(url, outfile)

    try:
        assert result[-len(outfile):] == outfile
        assert len(result) > len(outfile)
        assert result[0] == '/'
    finally:
        # Clean up
        subprocess.call(['rm', result])


@pytest.mark.integration
def test_download__provide_full_path_for_outfile():
    """
    NOTE: Your tmp folder must be writable
    """
    from ftpserver import download

    url = 'http://www.google.com'
    outfile = '/tmp/google.html'

    result = download(url, outfile)

    try:
        assert result == outfile
    finally:
        # Clean up
        subprocess.call(['rm', result])


@pytest.mark.integration
def test_download__file():
    """
    NOTE: Your tmp folder must be writable
    """
    from ftpserver import download

    url = 'http://www.analysis.im/uploads/seminar/pdf-sample.pdf'
    outfile = 'pdf-sample.pdf'

    result = download(url, outfile)

    try:
        assert result[-len(outfile):] == outfile
        assert len(result) > len(outfile)
        assert result[0] == '/'
    finally:
        # Clean up
        subprocess.call(['rm', result])


@pytest.mark.integration
def test_download__youtube_video():
    """
    NOTE: Your tmp folder must be writable
    """
    from ftpserver import download

    url = 'https://www.youtube.com/watch?v=vLfAtCbE_Jc'
    outfile = 'vid.mp4'

    result = download(url, outfile)

    try:
        assert result[-len(outfile):] == outfile
        assert len(result) > len(outfile)
        assert result[0] == '/'
    finally:
        # Clean up
        subprocess.call(['rm', result])


@pytest.mark.slow
@pytest.mark.integration
def test_download__normal_video():
    """
    NOTE: THIS TEST IS FRAGILE AND SLOW
    Try to find way of making it better by finding a nice video url to use
    """
    from ftpserver import download

    url = 'http://clips.vorwaerts-gmbh.de/VfE_html5.mp4?start=0'
    outfile = 'normal_vid.mp4'

    result = download(url, outfile)

    try:
        assert result[-len(outfile):] == outfile
        assert len(result) > len(outfile)
        assert result[0] == '/'
    finally:
        # Clean up
        subprocess.call(['rm', result])


@pytest.mark.unit
def test_outfile_has_supported_extension__basic():
    from ftpserver import outfile_has_supported_extension

    outfile = 'vid.mp4'

    result = outfile_has_supported_extension(outfile)

    assert result is True


@pytest.mark.unit
def test_outfile_has_supported_extension__false():
    from ftpserver import outfile_has_supported_extension

    outfile = 'vid.pod'

    result = outfile_has_supported_extension(outfile)

    assert result is False


@pytest.mark.unit
def test_is_youtube_video__basic():
    from ftpserver import is_youtube_video
    url = 'https://www.youtube.com/watch?v=kfchvCyHmsc'

    result = is_youtube_video(url)

    assert result is True


@pytest.mark.unit
def test_is_youtube_video__simple_false():
    from ftpserver import is_youtube_video
    url = 'https://www.google.com/'

    result = is_youtube_video(url)

    assert result is False


@pytest.mark.unit
def test_is_youtube_video__youtube_appended_false():
    from ftpserver import is_youtube_video
    url = 'https://www.google.com/https://www.youtube.com/watch?v=kfchvCyHmsc'

    result = is_youtube_video(url)

    assert result is False
