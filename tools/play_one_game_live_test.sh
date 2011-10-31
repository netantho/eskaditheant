#!/usr/bin/env sh
./playgame.py -So --end_wait=0.25 --player_seed=42 --verbose --log_dir game_logs --turns 100 --map_file maps/maze/maze_02p_02.map "$@" \
	"python ../bot/MyBot.py" \
	"python sample_bots/python/HunterBot.py" |
java -jar visualizer.jar
