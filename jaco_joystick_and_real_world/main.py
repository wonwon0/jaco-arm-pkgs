import argparse
import rospy
import roslaunch
import os
import threading
import time

def argumentParser(argument):
    """ Argument parser """
    parser = argparse.ArgumentParser(description='Either use joystick to move robot in gazebo or links a real robot to '
                                                 'the gazebo robot')
    parser.add_argument('control_type', metavar='control_type', type=str, default='gazebo',
                        help='control_type = Gazebo: Only in gazebo environement. Control_type = real_world: links real'
                             'robot to gazebo robot')
    args_ = parser.parse_args(argument)
    return args_

if __name__ == '__main__':

    args = argumentParser(None)
    if (args.control_type == 'gazebo') or (args.control_type == 'real_world'):
        try:
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
            roslaunch.configure_logging(uuid)
            launch1 = roslaunch.parent.ROSLaunchParent(uuid, ["/home/phil/catkin_ws/src/jaco-arm-pkgs/jaco_tutorial/jaco"
                                                             "_on_table/launch/jaco_on_table_gazebo_controlled.launch"])

            # package = 'jaco_on_table'
            # executable = 'jaco_on_table_gazebo_controlled'
            # node = roslaunch.Node(package, executable)
            #launch = roslaunch.scriptapi.ROSLaunch()


            if args.control_type == 'gazebo':
                launch1.start()
                #time.sleep(7)
                client_thread = threading.Thread(target=os.system("python /home/phil/catkin_ws/src/jaco-arm-pkgs/"
                                                                  "jaco_joystick_and_real_world/scripts/"
                                                                  "gazebo_realworld_linker.py gazebo"))
            else:
                launch2 = roslaunch.parent.ROSLaunchParent(uuid,
                                                           ["/home/phil/catkin_ws/src/kinova-ros/kinova_bringup/"
                                                            "launch/kinova_robot.launch"])
                launch2.start()
                #time.sleep(3)
                launch1.start()
                #time.sleep(7)
                client_thread = threading.Thread(target=os.system("python /home/phil/catkin_ws/src/jaco-arm-pkgs/"
                                                                  "jaco_joystick_and_real_world/scripts/"
                                                                  "gazebo_realworld_linker.py real_world"))
            client_thread.start()


        except rospy.ROSInterruptException:
            pass
    else:
        print('wrong inputs try "-h" to get help')