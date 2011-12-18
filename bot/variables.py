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

log_enabled = 0

move_attempts = 2

idle_time_remaining = 0
idle_time_ini = 0.20
idle_time_per_ant = 2