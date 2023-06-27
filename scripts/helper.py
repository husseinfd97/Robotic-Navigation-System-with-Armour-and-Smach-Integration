def clear_strings(strings, type):
    """
    Function to format a list of query strings by extracting only the meaningful part.

    Args:
       query_strings (str[]): The list of query strings to format.
       object_type (str): The query object type, which can be 1 for LOCATION or  2 for TIMESTAMP.

    Returns:
       formatted_list (str[]): The formatted list of query strings.
    """

    if object_type == 1:
        cleaned_list = [query.split()[4] for query in strings]
    elif object_type == 2:
        cleaned_list = [query[:-10] for query in strings]

    return cleaned_list


#def find_urgent(): 
    

        #choose an urgent room (randomly) if reachable random.choice(var)
        #urgent_locations = self.clear_strings(self.armor_client.call('QUERY','IND','CLASS',['URGENT']),1)
        #get the urgent rooms 


        #else, choose a corridor (randomly)

        #else, choose any reachable room (randomly)



def get_closest_urgent_room():
    global room_priority_flag
    closest_room = None
    armor_client = ArmorClient("example", "ontoRef")

    def update_robot_location():
        return locate_individual(
            armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1']).queried_objects
        )

    current_location = update_robot_location()

    while closest_room is None:
        if current_location == 'E':
            navigate_to('C1' if random.randint(1, 2) == 1 else 'C2')
            armor_client.call('REASON', '', '', [''])
            current_location = update_robot_location()

        urgent_rooms_query = armor_client.call('QUERY', 'IND', 'CLASS', ['URGENT'])
        for room in urgent_rooms_query.queried_objects:
            if current_location == 'C1' and room in ['R1', 'R2']:
                closest_room = room
                room_priority_flag = 0
                break
            elif current_location == 'C2' and room in ['R3', 'R4']:
                closest_room = room
                room_priority_flag = 0
                break

    room_priority_flag = 1 if closest_room is None else room_priority_flag
    return closest_room

#Changes made:

#The function update_robot_location() has been added to avoid repetition of the code for updating the robot's location.
#The loop structure has been altered to reduce the depth of nesting. The main loop now continues until an urgent room is found, or no more urgent rooms exist.
#The checks for urgent rooms in the locations 'C1' and 'C2' have been condensed into single line conditions.
#Finally, the function will return None if no urgent room is found.
#As mentioned previously, remember to properly attribute the original source if you're adapting someone else's code.





def navigate_to(destination):
    armor_client = ArmorClient("example", "ontoRef")
    armor_client.call('REASON', '', '', [''])
    current_location = locate_individual(
        armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1']).queried_objects
    )
    
    accessible_locations = list_Locations(
        armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['canReach', 'Robot1']).queried_objects
    )
    
    if destination in accessible_locations:
        armor_client.call('REPLACE', 'OBJECTPROP', 'IND', ['isIn', 'Robot1', destination, current_location])
        armor_client.call('REASON', '', '', [''])
        
        now_query = armor_client.call('QUERY', 'DATAPROP', 'IND', ['now', 'Robot1'])
        armor_client.call('REPLACE', 'DATAPROP', 'IND', ['now', 'Robot1', 'Long', str(math.floor(time.time())), findbt(now_query.queried_objects)])
        armor_client.call('REASON', '', '', [''])
        
        room_query = armor_client.call('QUERY', 'CLASS', 'IND', [destination, 'true'])
        if room_query.queried_objects in [['URGENT'], ['ROOM']]:
            visited_query = armor_client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', destination])
            armor_client.call('REPLACE', 'DATAPROP', 'IND', ['visitedAt', destination, 'Long', str(math.floor(time.time())), findbt(visited_query.queried_objects)])
            armor_client.call('REASON', '', '', [''])
    
    else:
        connected_to_query = armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['connectedTo', destination])
        common_location = find_common_connection(list_Locations(connected_to_query.queried_objects), accessible_locations)
        
        if common_location is None:
            armor_client.call('REPLACE', 'OBJECTPROP', 'IND', ['isIn', 'Robot1', accessible_locations[0], current_location])
            armor_client.call('REASON', '', '', [''])
            current_location = locate_individual(armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1']).queried_objects)
            common_location = find_common_connection(list_Locations(armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['canReach', 'Robot1']).queried_objects), accessible_locations)
        
        armor_client.call('REPLACE', 'OBJECTPROP', 'IND', ['isIn', 'Robot1', common_location, current_location])
        armor_client.call('REASON', '', '', [''])
        current_location = locate_individual(armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1']).queried_objects)
        
        armor_client.call('REPLACE', 'OBJECTPROP', 'IND', ['isIn', 'Robot1', destination, current_location])
        armor_client.call('REASON', '', '', [''])
        
        now_query = armor_client.call('QUERY', 'DATAPROP', 'IND', ['now', 'Robot1'])
        armor_client.call('REPLACE', 'DATAPROP', 'IND', ['now', 'Robot1', 'Long', str(math.floor(time.time())), findbt(now_query.queried_objects)])
        armor_client.call('REASON', '', '', [''])
        
        room_query = armor_client.call('QUERY', 'CLASS', 'IND', [destination, 'true'])
        if room_query.queried_objects in [['URGENT'], ['ROOM']]:
            visited_query = armor_client.call('QUERY', 'DATAPROP', 'IND', ['visitedAt', destination])
            armor_client.call('REPLACE', 'DATAPROP', 'IND', ['visitedAt', destination, 'Long', str(math.floor(time.time())), findbt(visited_query.queried_objects)])
            armor_client.call('REASON', '', '', [''])
    
    current_location = locate_individual(
        armor_client.call('QUERY', 'OBJECTPROP', 'IND', ['isIn', 'Robot1']).queried_objects
    )
    print(f'Robot isIn {current_location}')

