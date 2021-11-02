# ddnsPorkbun
Python script using requests to update DNS A records hosted by PorkBun (DDNS)

Copy config.sample to config.py
Update with your DNS zones and API key

Script will query your DNS zones for A records and update all A records resolve to something outside of the 10.5.0.0/16 netblock to the current public IP of the host running the script. 
