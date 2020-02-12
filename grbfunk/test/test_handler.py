import os
import time
os.environ["GRBFUNK_DEBUG"] = "True"

import lxml.etree
from grbfunk.handler import handler
from grbfunk.utils.package_data import get_path_of_data_file


def test_gbm_flt():
    ff = get_path_of_data_file("gbm_flt.xml")
    root = lxml.etree.parse(open(ff, "r"))
    handler(ff, root)

    time.sleep(5)
    

def test_gbm_gnd():
    ff = get_path_of_data_file("gbm_gnd_pos.xml")
    root = lxml.etree.parse(open(ff, "r"))
    handler(ff, root)

    time.sleep(5)
    
def test_gbm_fin():
    ff = get_path_of_data_file("gbm_fin_pos.xml")
    root = lxml.etree.parse(open(ff, "r"))
    handler(ff, root)

    time.sleep(5)
