#!/usr/bin/env python3 

print('loading libraries')
import roslib
import rospy
from math import *
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from std_msgs.msg import Float64



amplitude = 1.0
freq = 2
cloc_freq = 30
ang_vel = None
lin_acc = None
orientation = None
sensor_range = None

log_path = 'data_log.csv'


def log_imu(data):
  global ang_vel, lin_acc, orientation
  ang_vel = data.angular_velocity
  lin_acc = data.linear_acceleration
  orientation = data.orientation


def log_sensor(data):
  global sensor_range
  sensor_range = data.range


if __name__ == '__main__':
  print('loading publishers')
  rospy.Subscriber('/cane/imu', Imu, log_imu)
  rospy.Subscriber('/cane/sensor', Range, log_sensor)
  shoulder = rospy.Publisher('/cane/shoulder_position_controller/command', Float64, queue_size=10)

    
  print('initalizing node')
  rospy.init_node('brain', anonymous=True)
  rate = rospy.Rate(cloc_freq)
  

  print('logging data to ~/.ros/' + log_path)
  log = open(log_path, 'w')


  clock_counter = 0

  log.write('time(s) ang_vel_x ang_vel_y ang_vel_z lin_acc_x lin_acc_y lin_acc_z orientation_x orientation_y orientation_z sensor_range\n')

  try:
    while not rospy.is_shutdown():
      # print current stage
      # rospy.loginfo(stage_cmd)
      clock_counter += (1.0/cloc_freq)
      shoulder.publish(amplitude * sin(clock_counter * freq))

      if ang_vel is not None and lin_acc is not None and orientation is not None and sensor_range is not None:
        log.write('%f %f %f %f %f %f %f %f %f %f %f\n' 
          % (clock_counter, ang_vel.x, ang_vel.y, ang_vel.z, lin_acc.x, lin_acc.y, lin_acc.z, orientation.x, orientation.y, orientation.z, sensor_range))

      rate.sleep()
  except Exception as e:
    print(e)
  log.close()
    
  