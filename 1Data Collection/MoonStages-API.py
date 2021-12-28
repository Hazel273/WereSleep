###
#this script gets the stage of the moon at the current time from the Farmsense API
#and then inserts the data into the SQL database
#
#Run this script as a Cron Job once every 12 hours
###

#import relevant libraries
#MySQL to insert into the database
import mysql.connector
#requests to make HTTP requests to the API
import requests
#The current unix timestamp as the API needs it
import time
import json

#create a MySQL connector to connect to the correct database 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="WereSleep65000",
  database="esp_data"
)
#request the moon data at the current time from the farmsense API
r = requests.get("https://api.farmsense.net/v1/moonphases/?d=" + str(int(time.time())))
#get the farmsense API response
responseString = r.text
#load the response as a JSON file
moon = json.loads(responseString)
#get the dictionary out from the JSON file
moon = moon[0]
#get all of the variables of intrest out of the dictionary and into separate variables
phase = moon["Phase"]
illumination= moon['Illumination']
age= moon['Age']
diameter= moon['AngularDiameter']
#start the MySQL cursor
mycursor = mydb.cursor()
#create the SQL query with the desired variables
sql = "INSERT INTO MoonData (phase, illumination, age, diameter) VALUES (%s, %s, %s, %s)"
val = (phase, illumination,age,diameter)
#execute the SQL query
mycursor.execute(sql, val)
mydb.commit()