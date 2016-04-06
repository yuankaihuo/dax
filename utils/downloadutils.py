__author__ = 'damons'

import uriutil
import printutil
import os
import errno

def download_scan_from_dict(xnat, scan_dict, resource_name, download_dir):
    '''
    Method to download a scan from a dict of scan info

    :param xnat: pyxnat Interface object to XNAT
    :param scan_dict: dictionary of information about a subject
    :param resource_name: name of the scan resource to download from
    :param download_dir: directory to download to
    :return: file path

    '''
    uri = uriutil.URI_SESSION_SCAN_BY_ID

    xnaturi = uriutil.XNATURI(xnat=xnat, uri=uri, value_dict=scan_dict)
    xnaturi.select()

    if xnaturi.exists():
        downloaded_files = download_scan(xnaturi.uri_obj, resource_name, download_dir)
        return downloaded_files
    else:
        printutil.print_warning_message('Object defined by uri %s does not'
                                        ' exist' % xnaturi.formatted_uri)

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
        new_location = os.path.join(download_dir, f.label())
        files_out.append(new_location)
        obj.file(f.label()).get_copy(new_location)

        # Check to make sure we got the file
        if not os.path.isfile(new_location):
            raise IOError(errno.ENOENT, 'File %s not found' % new_location)

    return files_out



