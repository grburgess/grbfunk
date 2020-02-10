import os

os.environ['GRBFUNK_DEBUG'] = 'True'

import lxml.etree
from grbfunk.handler import handler
from grbfunk.utils.package_data import get_path_of_data_file



def test_gbm_flt():
    ff = get_path_of_data_file('gbm_flt.xml')
    root = lxml.etree.parse(open(ff, "r"))
    handler(ff,root)
