## WereSleep code breakdown 

The website will be found at:

http://86.21.74.57:56000

Unless my ISP changes my IP, in which case contact me

# 1Data Collection

Light Sensor.cpp - The code for the ESP-32

MoonStages-API.py - The script that gets data from Farmsense, trigger this with a Cron Job once every 12h

post-room-data.php - The code that posts the light data to the SQL database

post-window-data.php - The code that posts the light data to the SQL database

SleepData-Hook.py - The webhook that listens out for sleep events, run this as a service to avoid data loss

# 2Data Processing

Processing.ipynb - The Jupiter Notebook that was used for data analysis

# 3Data Presentation

app.py - the Dash App that the user interacts with

AdditnalFun.py - Functions needed by the Dash App

# 4Data

The data stored as .csv and .sql files as separate tables for the time period between 01/12/2021 and 24/12/2021
