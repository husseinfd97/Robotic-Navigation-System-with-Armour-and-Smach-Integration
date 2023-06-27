#!/usr/bin/env python

# Import the armor client class
import time
from armor_client import ArmorClient
import random
import time
import math
import rospy
import rospkg
from armor_api.armor_client import ArmorClient
from std_msgs.msg import Bool

from os.path import dirname, realpath
client = ArmorClient("example", "ontoRef") 


#def LoadMap():
path = dirname(realpath(__file__))
# Put the path of the file.owl
oldontology = path + "/../maps/topological_map.owl"
new_map = path + "/../maps/new_map.owl"




minwait = 0.0
maxwait = 1.75


import re

def extract_time(lst):
    """
    Function for finding the time with Unix format from the return of a queried property from armor.

    Args:
        lst (list): The time in the armor response format, e.g., ['"1669241751"^^xsd:long']

    Returns:
        str: The time extracted and changed to a string, e.g., "1665579740"
    """
    time_pattern = r'"(\d+)"'
    for item in lst:
        match = re.search(time_pattern, item)
        if match:
            return match.group(1)
    return ""








def LoadMap():
   
    client = ArmorClient("example", "ontoRef")
    client.call('LOAD','FILE','',[oldontology, 'http://bnc/exp-rob-lab/2022-23', 'true', 'PELLET', 'false'])
    pub = rospy.Publisher('mapsituation', Bool, queue_size=10)
    rospy.init_node('mapsituation_node', anonymous=True)
    pub.publish(0)


    print("Starting building the map")



    # ADD PROPERTIES TO OBJECTS
    # Distinction between rooms and corridors
    client.manipulation.add_objectprop_to_ind("hasDoor", "R1", "D1")
    client.manipulation.add_objectprop_to_ind("hasDoor", "R2", "D2")
    client.manipulation.add_objectprop_to_ind("hasDoor", "R3", "D3")
    client.manipulation.add_objectprop_to_ind("hasDoor", "R4", "D4")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C1", "D1")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C1", "D2")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C1", "D5")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C1", "D6")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C2", "D3")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C2", "D4")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C2", "D5")
    client.manipulation.add_objectprop_to_ind("hasDoor", "C2", "D7")
    client.manipulation.add_objectprop_to_ind("hasDoor", "E", "D6")
    client.manipulation.add_objectprop_to_ind("hasDoor", "E", "D7")
    print("All properties added!")
    
        
    print("All individuals are disjointed")

    
    # DISJOINT OF THE INDIVIDUALS OF THE CLASSES
    client.call('DISJOINT','IND','',['R1','R2','R3','R4','E','C1','C2','D1','D2','D3','D4','D5','D6','D7'])

    client.utils.apply_buffered_changes()
    client.utils.sync_buffered_reasoner()


    # ADD DATAPROPERTIES TO OBJECTS
    client.manipulation.add_dataprop_to_ind("visitedAt", "R1", "Long", str(int(time.time())))
    rospy.sleep(random.uniform(minwait, maxwait))
    client.manipulation.add_dataprop_to_ind("visitedAt", "R2", "Long", str(int(time.time())))
    rospy.sleep(random.uniform(minwait, maxwait))
    client.manipulation.add_dataprop_to_ind("visitedAt", "R3", "Long", str(int(time.time())))
    rospy.sleep(random.uniform(minwait, maxwait))
    client.manipulation.add_dataprop_to_ind("visitedAt", "R4", "Long", str(int(time.time())))
    rospy.sleep(random.uniform(minwait, maxwait))
   
    
    client.utils.apply_buffered_changes()
    client.utils.sync_buffered_reasoner()

    # Connections between locations

    print("All connections declared!")

    

    # INITIALIZE ROBOT POSITION
    client.manipulation.add_objectprop_to_ind("isIn", "Robot1", "E")
    print("Robot in its initial position!")

    # APPLY CHANGES AND QUERY
    client.utils.apply_buffered_changes()
    client.utils.sync_buffered_reasoner()


    print("map is built ")
    client.call('SAVE','','',[new_map])
    pub.publish(1)
   
rospy.sleep(3)
   
if __name__ == '__main__':
   try:
      LoadMap()
   except rospy.ROSInterruptException:
      pass 



