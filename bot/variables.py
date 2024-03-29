#!/usr/bin/env python

####################
# global variables #
####################

# track all moves for one turn, prevent collisions
# orders for the turn, new location as the key, old location as the value
orders = {}
# targets for the turn, location of the target food as the key, location of the assigned ant as the value
targets = {}

pathfinding = {}


##################
# configuration  #
##################

log_enabled = True
visualization_enabled = True

move_attempts = 1

idle_time_remaining = 0
idle_time_ini = 0.25
idle_time_per_ant = 4