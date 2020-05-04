from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# visited dict
visited = {}
# path to back track
reverse_path = []
# opposite dict for reversing directions
opposite_dir = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# Add starting room to visited
visited[player.current_room.id] = player.current_room.get_exits()

# While number_of_rooms_visited < total_rooms
while len(visited) < len(room_graph):
    # current
    # print(f"Current Room: {player.current_room.id}\nAvailable exits: {player.current_room.get_exits()}")

    # if the room has not been visited
    if player.current_room.id not in visited:
        # add to visited    room_id : [list of exits]
        visited[player.current_room.id] = player.current_room.get_exits()
        # remove the direction you came from
        previous_dir = traversal_path[-1]
        visited[player.current_room.id].remove(opposite_dir[previous_dir])
         
    # if the room has no unexplored exits
    if len(visited[player.current_room.id]) == 0:
        # assign prev_direction from reverse path and remove it to avoid looping
        previous_dir = reverse_path[-1]
        # TRIAL: previous_dir = opposite_dir[traversal_path[-1]]
        reverse_path.pop()
        # add the back step to traversal path
        traversal_path.append(previous_dir)
        # travel back
        player.travel(previous_dir)
    # traverse a random direction
    else:
        # go whatever direction is the last of the unexplored paths
        direction = visited[player.current_room.id][-1]
        # remove it
        visited[player.current_room.id].pop()
        # add direction to traversal_path
        traversal_path.append(direction)
        # add the opposite direction to the reverse path
        reverse_path.append(opposite_dir[direction])
        # travel direction
        player.travel(direction)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
