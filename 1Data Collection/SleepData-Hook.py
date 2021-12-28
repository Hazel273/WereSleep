###
#This script continiously listens to a specific port for POST requests
#The sleep as android app is set to post to this specific port
#and then inserts the data into the SQL database
#
#Run this script as a service on the server to ensure no posts are missed
###

#import relevant libraries
#flask to allow python to interact with the internet
from flask import Flask, request, abort
#flask MySQL add-on to allow it to save to the database
from flask_mysqldb import MySQL

#define a flask app
app = Flask(__name__)
#give the flask app the credentials to connect to the SQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'WereSleep65000'
app.config['MYSQL_DB'] = 'esp_data'
#create an instance of MySQL
mysql = MySQL(app)
#open the flask app to ip/sdh:5000 (SleepDataHook)
@app.route('/sdh', methods=['POST'])
#define the webhook
def webhook():
    #if we get a HTTP POST request
    if request.method == 'POST':
        #start the MySQL cursor
        cursor = mysql.connection.cursor()
        #create the SQL query with the desired variables
        #so take only the "event" from the JSON file, as the rest of the data is irrelevant
        cursor.execute("INSERT INTO SleepData (State) VALUES ('"+ request.json["event"] +"')")
        #execute the SQL query
        mysql.connection.commit()
        #close the SQL connection
        cursor.close()
        #Return a success message
        return 'success', 200
    #If it is not a HTTP POST (so for example a GET request that a browser would make) Return the HTML 400 error
    else:
        abort(400)
#Open the webhook
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
