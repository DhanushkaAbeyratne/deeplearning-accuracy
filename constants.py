'''
Returns constants to the project
'''

import os

def get_dirs():
    '''
    Returns constant directories paths
    '''
    dir_dict = dict()
    dir_dict['parent'] = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    return dir_dict