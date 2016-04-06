__author__ = 'damons'

import pyxnat.core.errors
import printutil
import tempfile
import os
from pyxnat import Interface
import shutil

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

def refresh_interface(xnat):
    '''

    :param xnat:
    :return:
    '''

    xnat.disconnect()
    return get_interface()

def get_interface(host=None, user=None, pwd=None):
    """
    Opens a connection to XNAT using XNAT_USER, XNAT_PASS, and XNAT_HOST from
     env if host/user/pwd are None.

    :param host: URL to connect to XNAT
    :param user: XNAT username
    :param pwd: XNAT password
    :return: InterfaceTemp object which extends functionaly of pyxnat.Interface

    """
    if user is None:
        user = os.environ['XNAT_USER']
    if pwd is None:
        pwd = os.environ['XNAT_PASS']
    if host is None:
        host = os.environ['XNAT_HOST']
    # Don't sys.exit, let callers catch KeyErrors
    return InterfaceTemp(host, user, pwd)

class InterfaceTemp(Interface):
    """
    Extends the pyxnat.Interface class to make a temporary directory, write the
     cache to it and then blow it away on the Interface.disconnect call()
     NOTE: This is deprecated in pyxnat 1.0.0.0
    """
    def __init__(self, xnat_host, xnat_user, xnat_pass, temp_dir=None):
        """
        Entry point for the InterfaceTemp class

        :param xnat_host: XNAT Host url
        :param xnat_user: XNAT User ID
        :param xnat_pass: XNAT Password
        :param temp_dir: Directory to write the Cache to
        :return: None

        """
        if not temp_dir:
            temp_dir = tempfile.mkdtemp()
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        self.temp_dir = temp_dir
        super(InterfaceTemp, self).__init__(server=xnat_host, user=xnat_user, password=xnat_pass, cachedir=temp_dir)

    def disconnect(self):
        """
        Disconnect the JSESSION and blow away the cache

        :return: None
        """
        self._exec('/data/JSESSION', method='DELETE')
        try:
            shutil.rmtree(self.temp_dir)
        except OSError as OSE:
            printutil.print_warning_message('Interface already disconnected!')