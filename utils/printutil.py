__author__ = 'damons'

import datetime
import sys

def print_warning_message(message):
    '''
    Print a message with the timestamp in front of it

    :param message: The string to print
    :return: None

    '''

    now = datetime.datetime.now()
    sys.stdout.write('[%s] WARNING: %s\n' % (now, message))