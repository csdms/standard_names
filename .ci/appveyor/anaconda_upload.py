from __future__ import print_function

import os
import sys
import subprocess
import traceback
import glob


def this_is_a_release():
    repo_tag = os.environ.get('APPVEYOR_REPO_TAG', 'false')
    tag_name = os.environ.get('APPVEYOR_REPO_TAG_NAME', '')

    return repo_tag == 'true' and tag_name.startswith('v')


def conda_package_filename(recipe):
    conda_build = ' '.join(['conda', 'build', '--output', recipe])
    try:
        resp = subprocess.check_output(conda_build, shell=True)
    except subprocess.CalledProcessError:
        traceback.print_exc()
    else:
        file_to_upload = resp.strip().split()[-1]

    # (dirname, filename) = os.path.split(file_to_upload)
    # try:
    #     file_to_upload = glob.glob(dirname + b'\\' + b'standard_names*.tar.bz2')[0]
    # except IndexError:
    #     raise RuntimeError('{name}: not a file'.format(name=dirname))

    if not os.path.isfile(file_to_upload):
        raise RuntimeError('{name}: not a file'.format(name=file_to_upload))

    return file_to_upload


def upload_to_anaconda_cloud(fname, channel='main'):
    token = os.environ.get('ANACONDA_TOKEN', 'NOT_A_TOKEN')
    anaconda_upload = ' '.join(['anaconda', '-t', token, 'upload', '--force',
                                '--user', 'csdms', '--channel', channel,
                                fname.decode('utf-8')])

    print('Uploading {name} to {channel} channel'.format(
        name=fname, channel=channel))

    try:
        subprocess.check_call(anaconda_upload, shell=True)
    except subprocess.CalledProcessError:
        traceback.print_exc()


def main():
    print('Using python: {prefix}'.format(prefix=sys.prefix))

    if this_is_a_release():
        os.environ['BUILD_STR'] = ''
    else:
        os.environ['BUILD_STR'] = 'dev'

    file_to_upload = conda_package_filename('conda-recipe')

    if this_is_a_release():
        upload_to_anaconda_cloud(file_to_upload, channel='main')
    else:
        upload_to_anaconda_cloud(file_to_upload, channel='dev')


if __name__ == '__main__':
    main()
