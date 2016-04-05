__author__ = 'damons'

import uriutil
import printutil
import os

def download_scan_from_dict(xnat, scan_dict, resource_name, download_dir):
    '''
    Method to download a scan from a dict of scan info

    :param xnat: pyxnat Interface object to XNAT
    :param scan_dict: dictionary of information about a subject
    :param resource_name: name of the scan resource to download from
    :param download_dir: directory to download to
    :return: file path

    '''
    uri = uriutil.URI_SESSION_SCAN

    # Note that we will ignore resources in the scan_dict and user
    #  the user-passed resource
    formatted_uri = uriutil.format_uri(uri, scan_dict)

    obj = select_resource_by_uri(xnat, formatted_uri)
    if obj.exists():
        downloaded_files = download_scan(obj, resource_name, download_dir)
        return downloaded_files
    else:
        printutil.print_warning_message('Object defined by uri %s does not'
                                        ' exist' % formatted_uri)

def download_scan(obj, resource, download_dir):
    '''
    Generic method to download a scan

    :param obj: pyxnat EObject of the SCAN not the SCAN and RESOURCE
    :param resource: name of the resource to download from
    :param download_dir: directory to put the files in
    :return: list of file(s) downloaded

    '''

    return download(obj.resource(resource), download_dir)

def download(obj, download_dir):
    '''
    Generic download method that just calls get_copy for EVERY file in the resource
    :param obj: The object and resource to download from
    :param download_dir: directory to put the files in
    :return:
    '''

    files = obj.files()
    files_out = list()
    for f in files:
        new_location = os.path.join(download_dir, os.path.basename(f))
        files_out.append(new_location)
        obj.file(f).get_copy(new_location)

    return files_out


def select_resource_by_uri(xnat, uri):
    '''
    Method to select a resource from a fully qualified uri

    :param xnat: pyxnat Interface object to XNAT
    :param uri: some URI either from uriutil or otherwise specified
    :return: pyxnat E/Cobject

    '''

    return xnat.select(uri)


