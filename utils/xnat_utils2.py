__author__ = 'damons'

import pyxnat.core.errors
import printutil

def wrapped_select(xnat, uri):
    '''
    Method to catch errors frequently encountered during pyxnat's select method

    :param xnat: pyxnat Interface object
    :param uri: URI to select
    :return: selected object or None if error is caught

    '''

    obj = None
    try:
        obj = xnat.select(uri)
    except pyxnat.core.errors.InterfaceError as interr:
        printutil.print_warning_message('Caught PyXNAT InterfaceError while '
                                        'selecting with message %s' %
                                        interr.message)
    except pyxnat.core.errors.DatabaseError as dberr:
        printutil.print_warning_message('Caught PyXNAT DatabaseError while '
                                        'selecting with message %s' %
                                        dberr.message)
    return obj

def wrapped_delete(obj):
    '''
    The pyxnat method delete method often seems to throw a DatabaseError.
     This is a simple wrapper to catch these common errors

    :param obj: pyxnat EObject to delete

    :return: None
    '''

    try:
        obj.delete()
    except pyxnat.core.errors.InterfaceError as interr:
        printutil.print_warning_message('Caught PyXNAT InterfaceError while '
                                        'deleting with message %s' %
                                        interr.message)
    except pyxnat.core.errors.DatabaseError as dberr:
        printutil.print_warning_message('Caught PyXNAT DatabaseError while '
                                        'deleting with message %s' %
                                        dberr.message)

def refresh_connection(xnat):
    '''

    :param xnat:
    :return:
    '''

    xnat.disconnect()
    return get_connection()