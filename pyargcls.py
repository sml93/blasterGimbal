# -*- coding: utf-8 -*-
'''
    pysimplebgc
    -----------

    The public API and command-line interface to PySimpleBGC package.

    :copyright: Copyright 2015 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import os
import rospy
import argparse
import time
import copy
from datetime import datetime

# Make sure the logger is configured early:
# from . import VERSION
# from .logger import active_logger
from device_blast import SimpleBGC32
from compat_blast import stdout



def setstdcmd(cmdtype, device):
    '''set standard command'''
    fields = device.setcmd(cmdtype)
    for i in range(len(fields)):
        if fields[i]['name'] != 'reserved':
            stdout.write(("%s : " + fields[i]['valuefmt'] + "\n")%(fields[i]['name'],fields[i]['value']))


def getboardinfo3_cmd(device):
    '''Getboardinfo3 command.'''
    setstdcmd('CMD_BOARD_INFO_3', device)


def getrealtimedata3_cmd(device):
    '''Getrealtimedata3 command.'''
    setstdcmd('CMD_REALTIME_DATA_3', device)


def collectdata3_cmd(args, device):
    '''Collectdata3 command.'''
    device.setcollectcmd('CMD_REALTIME_DATA_3', args.output, args.delim, args.stdoutdisplay, args.measuresnb, args.storingperiod, args.samplingperiod)
            

def main():
    url = 'serial:/dev/ttyUSB0:115200:8N1'
    device = SimpleBGC32.from_url(url, timeout=10)

    for i in range(5):
        getrealtimedata3_cmd(device)
        print("\n\n")

    # # Parse argv arguments
    # try:
    #     pass
    # except Exception as e:
    #     pass
        

if __name__ == '__main__':
    main()
