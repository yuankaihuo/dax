__author__ = 'damons'

import os
import gzip
import errno
import printutil

def gunzip_file(filepath, remove=False):
    '''
    Method to gunzip a file using python's gzip library

    :param filepath: path to a file to gunzip
    :param remove: remove the unzipped file
    :return: filepath to the unzipped file
    '''

    if not os.path.isfile(filepath):
        raise IOError(errno.ENOENT, 'File %s not found' % filepath)

    try:
        gzip_file_object = gzip.GzipFile(filepath)
        gzip_file_data = gzip_file_object.read()
    except IOError as GzipIOE:
        printutil.print_warning_message(GzipIOE.message)
        return None

    unzipped_file_name = filepath[:-3]
    with open(unzipped_file_name, 'w') as unzipped_obj:
        unzipped_obj.write(gzip_file_data)

    if remove:
        try:
            os.remove(filepath)
        except IOError as RMIOE:
            printutil.print_warning_message(RMIOE.message)

    return unzipped_file_name

def gzip_file(filepath, remove=False):
    '''
    Method to gzip a file using python's gzip library

    :param filepath: path to a file to gunzip
    :param remove: remove the unzipped file if true
    :return: file path to the gzipped file
    '''

    if not os.path.isfile(filepath):
        raise IOError(errno.ENOENT, 'File %s not found' % filepath)

    with open(filepath, 'r') as unzipped_obj:
        unzipped_data = unzipped_obj.read()

    zipped_fname = filepath +'.gz'
    with gzip.open(zipped_fname) as gzipped_obj:
        gzipped_obj.write(unzipped_data)

    if remove:
        try:
            os.remove(filepath)
        except IOError as RMIOE:
            printutil.print_warning_message(RMIOE.message)

    return zipped_fname