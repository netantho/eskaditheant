rm *.zip
replace "log_enabled = True" "log_enabled = False" -- variables.py
replace "visualization_enabled = True" "visualization_enabled = False" -- variables.py
zip -r bot.zip ants.py MyBot.py variables.py lib/