import printutil

# Mirror of the URIS here https://wiki.xnat.org/display/XNAT16/XNAT+REST+API+Directory

# User URIS
URI_USER_RESOURCE = '/data/user/cache/resources'
URI_USER_RESOURCES_BY_ID = '/data/user/cache/resources/{resource}'
URI_USER_FILE = '/data/user/cache/resources/{resource}/files'
URI_USER_FILE_BY_ID = '/data/user/cache/resources/{resource}/files/{file}'
URI_USER = '/data/users'
URI_USER_BY_ID = '/data/users/{user}'

# Project URIS
URI_PROJECT = '/data/archive/projects'
URI_PROJECT_BY_ID = '/data/archive/projects/{project}'
URI_PROJECT_ACCESSIBILITY = '/data/archive/projects/{project}/accessibility'
URI_PROJECT_ACCESSIBILITY_BY_TYPE = '/data/archive/projects/{project}/accessibility/{accessibility}'
URI_PROJECT_ARC_PATH = '/data/archive/projects/{project}/current_arc'
URI_PROJECT_ARC_PATH_BY_SUBDIR = '/data/archive/projects/{project}/current_arc/{folder}'
URI_PROJECT_FILES = '/data/archive/projects/{project}/files/{file}'
URI_PROJECT_PREARCHIVE_CODE = '/data/archive/projects/{project}/prearchive_code'
URI_PROJECT_PREARCHIVE_CODE_BY_ID = 'data/archive/projects/{project}/prearchive_code/{code}'
URI_PROJECT_QUARANTINE_CODE = '/data/archive/projects/{project}/quarantine_code'
URI_PROJECT_QUARANTINE_CODE_BY_ID = '/data/archive/projects/{project}/quarantine_code/{code}'
URI_PROJECT_RESOURCES = '/data/archive/projects/{project}/resources'
URI_PROJECT_RESOURCES_BY_ID = '/data/archive/projects/{project}/resources/{resource}'
URI_PROJECT_RESOURCES_BY_FILENAME = '/data/archive/projects/{project}/resources/{resource}/files/{file}'
URI_PROJECT_SEARCHES = '/data/archive/projects/{project}/searches/{search}'


def format_uri(uri, value_dict):
    '''
    Method to format any URI given a dict of key value pairs

    :param uri: String template of a URI
    :param value_dict: key value pairs where the keys are in the URI and the
     values are the value to insert
    :return: Formatted URI with text inserted

    '''

    uri_out = None
    try:
        uri_out = uri.format(**value_dict)
    except KeyError as KE:
        printutil.print_warning_message(KE.message)
    return uri_out


