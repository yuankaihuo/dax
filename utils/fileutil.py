__author__ = 'damons'

import os
import gzip
import errno
import printutil
import glob
import fnmatch
import tempfile
import shutil

def gunzip_directory(directory, remove=False):
    """
    Method to call the gunzip_file function on a directory
    
    :param directory: directory to iterate over and gunzip all files that end with gz
    :param remove: remove the unzipped file
    :return: filepaths to the unzipped file
    
    """
    zipped_files = glob.glob(os.path.join(directory, '*.gz'))
    unzipped_files = list()
    for zipped_file in zipped_files:
        unzipped_file = gunzip_file(zipped_file, remove)
        unzipped_files.append(unzipped_file)

    return unzipped_files


def gzip_directory(directory, remove=False, fnmatch_filter=None):
    """
    Method to call the gzip_file function on a directory using an fnmatch filter

    :param directory: directory to iterate over and gunzip all files that end with gz
    :param remove: remove the unzipped file
    :param fnmatch_filter: a filter that can be used to filter out files
     the directory see https://docs.python.org/2/library/fnmatch.html
    :return: filepath to the unzipped file

    """
    unzipped_files = glob.glob(os.path.join(directory, '*'))
    zipped_files = list()
    if fnmatch_filter is None:
        filtered_unzipped_files = unzipped_files
    else:
        filtered_unzipped_files = [ f for f in unzipped_files if fnmatch.fnmatch(os.path.basename(f), fnmatch_filter) ]

    for filtered_unzipped_file in filtered_unzipped_files:
        zipped_file = gzip_file(filtered_unzipped_file, remove)
        zipped_files.append(zipped_file)

    return zipped_files


def gunzip_file(filepath, remove=False):
    """
    Method to gunzip a file using python's gzip library

    :param filepath: path to a file to gunzip
    :param remove: remove the unzipped file
    :return: filepath to the unzipped file
    """

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
    """
    Method to gzip a file using python's gzip library

    :param filepath: path to a file to gunzip
    :param remove: remove the unzipped file if true
    :return: file path to the gzipped file
    """

    if not os.path.isfile(filepath):
        raise IOError(errno.ENOENT, 'File %s not found' % filepath)

    with open(filepath, 'r') as unzipped_obj:
        unzipped_data = unzipped_obj.read()

    zipped_fname = filepath +'.gz'
    with gzip.open(zipped_fname, 'w') as gzipped_obj:
        gzipped_obj.write(unzipped_data)

    if remove:
        try:
            os.remove(filepath)
        except IOError as RMIOE:
            printutil.print_warning_message(RMIOE.message)

    return zipped_fname


def make_temp_dir():
    """
    Method to create a temprary directory that shouldn't collide
     with others.

    :return: string of the temporary directory
    """

    return tempfile.mkdtemp()


def remove_file_if_exists(filepath):
    """
    Method to remove a file if it exits

    :param filepath: full path to a file to delete
    """

    if not os.path.isfile(filepath):
        printutil.print_warning_message('File %s does not exist' % filepath)
        return

    if not os.path.isdir(filepath):
        printutil.print_warning_message('%s is a directory, not a file.' % filepath)
        return

    os.remove(filepath)


def remove_directory_if_exists(dirpath):
    """
    Method to remove a directory if it exits

    :param dirpath: full path to a directory to delete
    """

    if  os.path.isfile(dirpath):
        printutil.print_warning_message('%s is a file, not a directory' % dirpath)
        return

    if not os.path.isdir(dirpath):
        printutil.print_warning_message('Directory %s does not exist' % dirpath)
        return

    shutil.rmtree(dirpath)
