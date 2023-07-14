#!/usr/bin/env python


import roslib
import random
import math
import time
import rospy
import rospkg
import smach
import smach_ros
from std_msgs.msg import Bool
from armor_api.armor_client import ArmorClient
from os.path import dirname, realpath
import datetime
import helper


#########
#get the same way in upload map 
path = dirname(realpath(__file__))
new_map = path + "/../maps/new_map.owl"

 
######### 

map_Uploaded_flag=0
battery_charged_flag=1
urgent_room_flag=0


# Variables for putting diffrent times for setting diffrent vistedAat property for each room   
min_time = 0.0
max_time = 1.75


def check_nearby_urgent_room():
    """
    Check for nearby urgent rooms, update the global `urgent_room_flag`, and return the urgent room if it exists.

    Returns:
        str: The urgent room nearby, according to the urgency of each robot. Returns '0' if no urgent room is found.
    """
    global urgent_room_flag
    urgent_room_flag = 0  # Initially, assume there's no urgent room
    least_room = None

    client = ArmorClient("example", "ontoRef")
    client.call('REASON', '', '', [''])

    # Query for urgent rooms
    urgent_rooms_query = client.call('QUERY', 'IND', 'CLASS', ['URGENT'])
    #print(helper.list_Locations(urgent_rooms_query.queried_objects))
    urgent_rooms_query = helper.list_Locations(urgent_rooms_query.queried_objects)
    client.call('REASON', '', '', [''])

    # Query current robot location
    current_location_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1'])
    current_location = helper.clean_list(current_location_query.queried_objects)

    if current_location == 'C1':
        room1_visit_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', 'R1'])
        room2_visit_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', 'R2'])
        room1_visit_time = float(helper.get_time(room1_visit_time_query.queried_objects))
        room2_visit_time = float(helper.get_time(room2_visit_time_query.queried_objects))
        least_room = helper.get_least_visit_time_room('R1', room1_visit_time, 'R2', room2_visit_time)
    elif current_location == 'C2':
        room3_visit_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', 'R3'])
        room4_visit_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', 'R4'])
        room3_visit_time = float(helper.get_time(room3_visit_time_query.queried_objects))
        room4_visit_time = float(helper.get_time(room4_visit_time_query.queried_objects))
        least_room = helper.get_least_visit_time_room('R3', room3_visit_time, 'R4', room4_visit_time)

    room = helper.same_elements_bt_lists([least_room], urgent_rooms_query)

    if room is not None:
        if "R1" in room:
            urgent_room_flag = 1
            return 'R1'
        elif "R2" in room:
            urgent_room_flag = 1
            return 'R2'
        elif "R3" in room:
            urgent_room_flag = 1
            return 'R3'
        elif "R4" in room:
            urgent_room_flag = 1
            return 'R4'

    return '0'  # No nearby urgent room found



def navigate_to(target_location):
    """
    Move the robot to the target location and check the best path to do that .

    Args:
        target_location (str): The location to which the robot should move.
    """
    client = ArmorClient("example", "ontoRef")
    client.call('REASON', '', '', [''])

    # Query initial robot location
    initial_location_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1'])
    current_location = helper.clean_list(initial_location_query.queried_objects)
    print('From', current_location, 'to:', target_location)

    if target_location == current_location:
        # If the target location is the same as the current location, directly move to the target location
        update_location_property(client, 'Robot1', target_location, current_location)
        update_now_property(client, 'Robot1')
        check_and_update_visitedat_property(client, target_location)
    else:
        reachable_locations_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['canReach', 'Robot1'])
        reachable_locations = helper.list_Locations(reachable_locations_query.queried_objects)
        
        if target_location in reachable_locations:
            update_location_property(client, 'Robot1', target_location, current_location)
            update_now_property(client, 'Robot1')
            check_and_update_visitedat_property(client, target_location)
        else:
            potential_path = generate_path_to_target(client, current_location, target_location, reachable_locations)
            intermediate_location = potential_path[0]
            current_location = potential_path[2]
            update_location_property(client, 'Robot1', intermediate_location, current_location)
            hena = client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1'])
            hena = helper.clean_list(hena.queried_objects)
            print('Robot here at:', hena)
            update_now_property(client, 'Robot1')
            check_and_update_visitedat_property(client, intermediate_location)
            current_location = intermediate_location

            reachable_locations_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['canReach', 'Robot1'])
            reachable_locations = helper.list_Locations(reachable_locations_query.queried_objects)

            if target_location in reachable_locations:
                update_location_property(client, 'Robot1', target_location, current_location)
                update_now_property(client, 'Robot1')
                check_and_update_visitedat_property(client, target_location)

    final_location_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1'])
    print('Robot finally isIn', helper.clean_list(final_location_query.queried_objects))


def update_location_property(client, robot, new_location, old_location):
    """
    Update the location property of the robot.

    Args:
        client (ArmorClient): The ArmorClient object for making calls to the server.
        robot (str): The name of the robot.
        new_location (str): The new location to update.
        old_location (str): The old location to replace.
    """
    client.call('REPLACE', 'OBJECTPROP', 'IND', ['isIn', robot, new_location, old_location])
    client.call('REASON', '', '', [''])


def update_now_property(client, robot):
    """
    Update the current time property of the robot.

    Args:
        client (ArmorClient): The ArmorClient object for making calls to the server.
        robot (str): The name of the robot.
    """
    current_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['now', robot])
    current_time = helper.get_time(current_time_query.queried_objects)
    client.call('REPLACE', 'DATAPROP', 'IND',
                ['now', robot, 'Long', str(math.floor(time.time())), current_time])
    client.call('REASON', '', '', [''])


def check_and_update_visitedat_property(client, location):
    """
    Check and update the visitedAt property of the given location.

    Args:
        client (ArmorClient): The ArmorClient object for making calls to the server.
        location (str): The location to check and update.
    """
    location_class_query = client.call('QUERY', 'CLASS', 'IND', [location, 'true'])

    if location_class_query.queried_objects == ['URGENT'] or location_class_query.queried_objects == ['ROOM']:
        visited_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', location])
        visited_time = helper.get_time(visited_time_query.queried_objects)
        #print(visited_time)
        client.call('REPLACE', 'DATAPROP', 'IND',
                    ['visitedAt', location, 'Long', str(math.floor(time.time())), visited_time])
        visited_time_query = client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', location])
        visited_time = helper.get_time(visited_time_query.queried_objects)
        # print(visited_time)
        client.call('REASON', '', '', [''])


def generate_path_to_target(client, current_location, target_location, reachable_locations):
    """
    Generate a potential path from the current location to the target location.

    Args:
        client (ArmorClient): The ArmorClient object for making calls to the server.
        current_location (str): The current location of the robot.
        target_location (str): The target location to reach.
        reachable_locations (list): List of reachable locations from the current location.

    Returns:
        list: A potential path from the current location to the target location.
    """
    potential_path = []
    target_connectedTo_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['connectedTo', target_location])
    target_connectedTo = helper.list_Locations(target_connectedTo_query.queried_objects)
    common_location = helper.same_elements_bt_lists(target_connectedTo, reachable_locations)

    if common_location is None:
        update_location_property(client, 'Robot1', reachable_locations[0], current_location)
        current_location = reachable_locations[0]
        hena = client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1'])
        hena = helper.clean_list(hena.queried_objects)
        print('Robot here at:', hena)
        reachable_locations_query = client.call('QUERY', 'OBJECTPROP', 'IND', ['canReach', 'Robot1'])
        reachable_locations = helper.list_Locations(reachable_locations_query.queried_objects)
        common_location = helper.same_elements_bt_lists(target_connectedTo, reachable_locations)

    potential_path.append(common_location)
    potential_path.append(target_location)
    potential_path.append(current_location)

    return potential_path



def callback_map(data):
    """
    callback function for updating the published bool detects the status of 
    map_uploaded_flag (map uploaded or not).

    Args:
        data: the subscribed bool value.
        
    Returns:
        map_Uploaded_flag: The flag after changing it's status.
    """

    global map_Uploaded_flag
    if data.data == 1:
        map_Uploaded_flag= 1
    elif data.data ==0:
        map_Uploaded_flag = 0


def callback_bat(data):
    """
    callback function for updating the published bool detects the status of 
    battery_charged_flag (battery status).

    Args:
        data: the subscribed bool value.
        
    Returns:
        battery_charged_flag: The flag after changing its status.
    """
    global battery_charged_flag
    if data.data == 1:
        battery_charged_flag= 1
    elif data.data ==0:
        battery_charged_flag = 0


class loading_map(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['NOT_YET_UPLODED', 'UPLOADED'])

    def execute(self, userdata):
        global map_Uploaded_flag
        client = ArmorClient("example", "ontoRef")
        #print(client)
        rospy.sleep(2)
        if map_Uploaded_flag==0:
            return 'NOT_YET_UPLODED'
        elif map_Uploaded_flag==1:
            client.call('LOAD','FILE','',[new_map, 'http://bnc/exp-rob-lab/2022-23', 'true', 'PELLET', 'false'])

            print("MAP IS LOADED SUCCESSFULLY")
            return 'UPLOADED'   



class moving_in_corridoor_planning_for_urgent(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['still_moving_in_cooridoor','urgent_room_exist','battery_low'])
        self.counter = 0

    def execute(self, userdata):
        global battery_charged_flag
        global urgent_room_flag 
        client = ArmorClient("example", "ontoRef")
        check_nearby_urgent_room()
        if battery_charged_flag==0:
            print("BATTERY LOW")
            return 'battery_low'

        elif battery_charged_flag==1 and urgent_room_flag==1:
            if urgent_room_flag==1:
                print("urgent room detected")
                return 'urgent_room_exist'
            elif urgent_room_flag ==0:
                if random.randint(0, 1)==0:
                    navigate_to('C1')
                    print("im moving to c1")
                    rospy.sleep(0.5)
                else:
                    navigate_to('C2')
                    print("moving to c2")
                    rospy.sleep(0.5)
            return 'still_moving_in_cooridoor'
             
        else:
            if random.randint(0, 1)==0:
                navigate_to('C1')
                print("im moving to c1")
                rospy.sleep(0.5)
            else:
                navigate_to('C2')
                print("moving to c2")
                rospy.sleep(0.5)
            return 'still_moving_in_cooridoor'
        

class move_to_urgent_room(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['keep_moving_to_urgent_rooms','cannot_plan','battery_low'])

    def execute(self, userdata):
        global battery_charged_flag
        global urgent_room_flag
        client = ArmorClient("example", "ontoRef")
        check_nearby_urgent_room()
        if battery_charged_flag==0:
            return 'battery_low'
        elif  battery_charged_flag==1:
            if urgent_room_flag==0:
                return 'cannot_plan'
            else:
                final_urgent_room=check_nearby_urgent_room()
                navigate_to(final_urgent_room)
                return 'keep_moving_to_urgent_rooms'

        

class Recharging(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['still_charging_battery','battery_charged'])


    def execute(self, userdata):
        
        global battery_charged_flag
        client = ArmorClient("example", "ontoRef")
        if battery_charged_flag==0:
            navigate_to('E')
            return 'still_charging_battery'
        elif battery_charged_flag==1: 
            return 'battery_charged'




def main():
    rospy.init_node('finite_state_machine')

    # Create a SMACH state machine
    R_FMS = smach.StateMachine(outcomes=[''])

    # Open the container
    with R_FMS:
        # Add states to the container
        smach.StateMachine.add('loading_map', loading_map(), 
                                transitions={'NOT_YET_UPLODED':'loading_map', 'UPLOADED':'moving_in_corridoor_planning_for_urgent'})
        smach.StateMachine.add('moving_in_corridoor_planning_for_urgent', moving_in_corridoor_planning_for_urgent(), 
                                transitions={'still_moving_in_cooridoor':'moving_in_corridoor_planning_for_urgent','urgent_room_exist':'move_to_urgent_room','battery_low':'Recharging'})
        smach.StateMachine.add('move_to_urgent_room', move_to_urgent_room(), 
                        transitions={'keep_moving_to_urgent_rooms':'move_to_urgent_room','cannot_plan':'moving_in_corridoor_planning_for_urgent','battery_low':'Recharging'})
        smach.StateMachine.add('Recharging', Recharging(), 
                        transitions={'still_charging_battery':'Recharging','battery_charged':'moving_in_corridoor_planning_for_urgent' })


    # Subcribers for detecting the battery and map uploading status
    rospy.Subscriber("load_map", Bool, callback_map)
    rospy.Subscriber("battery_state", Bool, callback_bat)

    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', R_FMS, '/SM_ROOT')
    sis.start()
    # Execute the state machine
    outcome = R_FMS.execute()
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
    
