rm *.zip
(replace "log_enabled = 1" "log_enabled = 0" -- variables.py)
zip -r bot.zip ants.py MyBot.py variables.py lib/