# Assignment Project

## Introduction
This assignment project focuses on implementing a robotic system using the Armour package and Smach package. The system aims to simulate a robot operating in a 2D environment consisting of four rooms and three corridors. The robot's behavior is designed to navigate through the environment, visiting different locations while following certain policies. The system incorporates the use of the Armour package for managing the robot's knowledge base and the Smach package for creating a finite state machine for controlling the robot's actions.

- Armour package: [Link to Armour Package](https://armour.github.io/)
- Smach package: [Link to Smach Package](http://wiki.ros.org/smach)

## Environment
The 2D environment is composed of four rooms and three corridors. The rooms are labeled as R1, R2, R3, and R4, while the corridors are labeled as C1, C2, and E. The robot moves within this environment, with various doors (D1...D6) connecting the rooms and corridors.

## Robot Behavior and Logic
The robot's behavior can be divided into two phases:

### Phase 1: Building the Topological Map
The robot starts in the E location and waits until it receives information to build the topological map. This information includes the relations between C1, C2, R1, R2, R3 locations, and the doors D1...D6.

### Phase 2: Navigating and Visiting Locations
After building the topological map, the robot moves to a new location and waits for some time before visiting another location. This behavior is repeated in an infinite loop. When the robot's battery is low, it returns to the E location and waits for some time before starting the behavior again.

The surveillance policy for the robot's movement is as follows:
- When the robot's battery is not low, it primarily stays on corridors.
- If a reachable room has not been visited for some time, the robot should visit it.

The implemented code ensures that the robot follows this behavior and policy by incorporating the necessary functions and logic.

## Software Architecture
The software architecture of the project consists of three nodes:

1. Load Map Node: Responsible for loading the topological map and publishing the load_map status.
2. State Machines Node: Implements the finite state machine (FSM) that controls the robot's behavior and actions. It subscribes to the load_map and battery_state topics, updates the urgent_room_flag and location_updated flags, and performs the necessary actions such as moving in the corridor, moving to urgent rooms, and recharging.
3. Battery Node: Publishes the battery_state status periodically, indicating the current battery level of the robot.

### Temporal Diagram
A temporal diagram illustrates the sequence of interactions between the nodes, showcasing how the load_map, urgent_room_flag, location_updated, and battery_state are published and utilized by the state machines node.

### State Diagrams
State diagrams provide a visual representation of the different states and transitions in the state machines node. They illustrate the flow and decision-making process of the finite state machine.

## Installation and Running Procedure
To install and run the project, follow these steps:
1. Navigate to your workspace's src directory.
2. Clone the project repository: `git clone https://github.com/husseinfd97/as_1.git`
3. Build the project: `catkin_make`
4. Launch the project: `roslaunch as_1 project.launch`

## System's Features
The implemented system offers the following key features:
- Ability to load the topological map and establish relations between locations and doors.
- Navigation logic based on the surveillance policy, prioritizing corridors and visiting rooms.
- Battery monitoring and recharging functionality.

## System's Limitations
While the implemented system covers the specified requirements, it also has some limitations:
- The surveillance policy is simple and does not consider dynamic changes or complex decision-making.
- The environment is limited to a predefined 2D layout with a fixed number of rooms and corridors.
- The system does not incorporate any external sensing or perception capabilities.

## Possible Technical Improvements
To enhance the system, the following improvements can be considered:
- Implementing more sophisticated surveillance policies that account for dynamic factors and optimize robot movement.
- Extending the environment to support a larger number of rooms, corridors, and door configurations.
- Integrating additional sensors and perception capabilities to enable more advanced navigation and mapping functionalities.

By addressing these improvements, the system can be further optimized for various real-world scenarios and requirements.

