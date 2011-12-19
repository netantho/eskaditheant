BOT0="python ../bot/MyBot.py $(cat maze2p.sh)"
BOT1="python sample_bots/python/HunterBot.py"
MAP="maps/maze/maze_02p_01.map"
TURNS="100"
LOADTIME="2000"
TURNTIME="400"
python aichallenge/ants/playgame.py "$BOT0" "$BOT1" --map_file $MAP --log_dir eskadi --turns $TURNS --verbose --log_error -e --turntime $TURNTIME --loadtime=$LOADTIME