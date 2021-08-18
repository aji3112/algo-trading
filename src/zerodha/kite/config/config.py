import logging
import sys
import threading

import numpy


def intializeConfig():

    numpy.set_printoptions(threshold=sys.maxsize)
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(threadName)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')