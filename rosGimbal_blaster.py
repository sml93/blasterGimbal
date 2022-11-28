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

from compat_blast import stdout
from device_blast import SimpleBGC32
from std_msgs.msg import Float32, Float32MultiArray


class rosGimbal:
    def __init__(self, url, device):
        self.url = url
        self.device = device
        self.rate = rospy.Rate(10)

    def convertUnit(self, a):
        return a * 0.021973


    def setstdcmd(self, cmdtype):
        '''set standard command'''
        fields = self.device.setcmd(cmdtype)
        for i in range(len(fields)):
            if (fields[i]['name'] == 'ANGLE_ROLL'):
                # stdout.write(("%s : " + fields[i]['valuefmt'] + "\n")%(fields[i]['name'],fields[i]['value']))
                self.angleRoll_str = fields[i]['name']
                self.angleRoll = fields[i]['value']
            elif (fields[i]['name'] == 'ANGLE_PITCH'):
                # stdout.write(("%s : " + fields[i]['valuefmt'] + "\n")%(fields[i]['name'],fields[i]['value']))
                self.anglePitch_str = fields[i]['name']
                self.anglePitch = fields[i]['value']
            else: pass
        print('%s: %.2f \n' %(self.angleRoll_str, self.convertUnit(self.angleRoll)))
        print('%s: %.2f \n' %(self.anglePitch_str, self.convertUnit(self.anglePitch)))
        # print("\n")


    def getboardinfo3_cmd(self):
        '''Getboardinfo3 command.'''
        self.setstdcmd('CMD_BOARD_INFO_3')


    def getrealtimedata3_cmd(self):
        '''Getrealtimedata3 command.'''
        self.setstdcmd('CMD_REALTIME_DATA_3')



    def collectdata3_cmd(self, args):
        '''Collectdata3 command.'''
        self.device.setcollectcmd('CMD_REALTIME_DATA_3', args.output, args.delim, args.stdoutdisplay, args.measuresnb, args.storingperiod, args.samplingperiod)


    def sender(self):
        self.getrealtimedata3_cmd()
        # pub = rospy.Publisher('encoder_rotations', Float32, queue_size=10)
        pub1 = rospy.Publisher('test', Float32MultiArray, queue_size=10)
        list_array = [self.convertUnit(self.angleRoll), self.convertUnit(self.anglePitch)]
        # roll_str = "%s : %f \n" % (self.angleRoll_str, self.convertUnit(self.angleRoll))
        # rospy.loginfo(roll_str)
        msg = Float32MultiArray()
        msg.data = [round(self.convertUnit(self.angleRoll), 2), round(self.convertUnit(self.anglePitch), 2)]
        # pub.publish(self.convertUnit(self.angleRoll))
        pub1.publish(msg)


def main():
    rospy.init_node('rosGimbal', anonymous=True)
    url = 'serial:/dev/ttyUSB0:115200:8N1'
    device = SimpleBGC32.from_url(url, timeout=10)
    run  = rosGimbal(url, device)
    while not rospy.is_shutdown():
        run.sender()
        run.rate.sleep()

        

if __name__ == '__main__':
    main()
