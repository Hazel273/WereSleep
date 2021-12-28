import datetime as dt
import sqlalchemy as db
import pandas as pd
import datetime as dt

###
#This function loads and processes the data in the same way Processing.ipynb does, see there for documentation
###
def DataLoader(source):
    engine = db.create_engine(source)
    #read the four tables
    MoonData = pd.read_sql_table("MoonData", engine)
    SensorDataRoom = pd.read_sql_table("SensorDataRoom", engine)
    SensorDataWindow = pd.read_sql_table("SensorDataWindow", engine)
    SleepData = pd.read_sql_table("SleepData", engine)
    #disconnect from the server
    engine.dispose()

    
    #clean up data
    MoonData = MoonData[["reading_time","illumination","age","diameter"]]

    SensorDataRoom = SensorDataRoom[["reading_time", "value1", "value2", "value3" ]]
    SensorDataRoom[["value1", "value2", "value3"]] = SensorDataRoom[["value1", "value2", "value3"]].apply(pd.to_numeric)
    SensorDataRoom.rename(columns={'value1': 'RedRoom', 'value2': 'GreenRoom', 'value3': 'BlueRoom'}, inplace=True)

    SensorDataWindow = SensorDataWindow[["reading_time", "value1", "value2", "value3" ]]
    SensorDataWindow[["value1", "value2", "value3"]] = SensorDataWindow[["value1", "value2", "value3"]].apply(pd.to_numeric)
    SensorDataWindow.rename(columns={'value1': 'RedWindow', 'value2': 'GreenWindow', 'value3': 'BlueWindow'}, inplace=True)

    SleepData["State"].replace({"sleep_tracking_paused": "sleep_tracking_stopped", "sleep_tracking_resumed": "sleep_tracking_started", "awake": "sleep_tracking_stopped", "not_awake": "sleep_tracking_started"}, inplace=True)
    SleepData["State"].replace({"sleep_tracking_stopped": 0, "sleep_tracking_started": 1, "light_sleep": 2, "deep_sleep": 3, "rem": 4}, inplace=True)
    del SleepData["id"]

    MoonData["reading_time"] = MoonData["reading_time"].apply(pd.to_datetime)
    SensorDataRoom["reading_time"] = SensorDataRoom["reading_time"].apply(pd.to_datetime)
    SensorDataWindow["reading_time"] = SensorDataWindow["reading_time"].apply(pd.to_datetime)
    SleepData["reading_time"] = SleepData["reading_time"].apply(pd.to_datetime)

    MoonData.set_index(keys = "reading_time", inplace = True)
    SensorDataRoom.set_index(keys = "reading_time", inplace = True)
    SensorDataWindow.set_index(keys = "reading_time", inplace = True)
    SleepData.set_index(keys = "reading_time", inplace = True)

    #we resample the moon data to have the values land on a 1 min interval
    MoonData =  MoonData.resample("60s").max()
    #then we interpolate using a quadratic function the moon data for each minute
    MoonData = MoonData.interpolate(method='quadratic', limit_direction='forward', axis=0)

    #for the sensor inputs we resample and the frontfill any missing data, meaning samples are copied forward to fill in voids
    SensorDataRoom = SensorDataRoom.asfreq(freq="60s", method="ffill")
    SensorDataWindow = SensorDataWindow.asfreq(freq="60s", method="ffill")

    #we resample the sleep data to have the values land on a 1 min interval
    SleepData = SleepData.resample("60s").max()
    #then we resample and the frontfill any missing data, meaning samples are copied forward to fill in voids
    SleepData = SleepData.interpolate(method='ffill', limit_direction='forward', axis=0)


    #The four data sets are merged together as they now all use the same reading time structure
    CompleteData = pd.merge_asof(MoonData,SensorDataRoom, on="reading_time", )
    CompleteData = pd.merge_asof(CompleteData,SensorDataWindow, on="reading_time", )
    CompleteData = pd.merge_asof(CompleteData,SleepData, on="reading_time", )
    #we fill in any missing values with zeros (only for the beginning of the sleep state)
    CompleteData.fillna(value=0, inplace = True)

    CompleteDataSmoothed = CompleteData.rolling(30).mean()
    CompleteDataSmoothed["reading_time"] = CompleteData["reading_time"]
    CompleteDataLimited = CompleteDataSmoothed[(CompleteDataSmoothed["reading_time"].dt.time > dt.time(20,00,00)) | (CompleteDataSmoothed["reading_time"].dt.time < dt.time(8,00,00))]

    return CompleteDataLimited, CompleteDataSmoothed, CompleteData

###
#This function finds the last completed sleep cycle (from sleep tracking started to stopped) and calculates the average sleep value as well as time between the two points
#It reloads the Sleep data as it is easier to use than the interpolated data
###
def sleepCalc(source,CompleteData):
    #open a SQL connection
    engine = db.create_engine(source)
    #read the table table
    SleepData = pd.read_sql_table("SleepData", engine)
    #disconnect from the server
    engine.dispose()
    #reindex and resample to get the same structure as the exiting data
    SleepData.set_index(keys = "reading_time", inplace = True)
    SleepData = SleepData.resample("60s").max()
    
	#Create a sublist of Sleepdat when "sleep_tracking_x" is true, and then get the last value from it
    starts = SleepData.loc[SleepData["State"] == "sleep_tracking_started"].tail(1)
    ends = SleepData.loc[SleepData["State"] == "sleep_tracking_stopped"].tail(1)
	#then get the index of said value
    startsTime = starts.index[0]
    endsTime = ends.index[0]
	#since the data is indexed based on time the index difference is the time spend asleep
    sleepTime = endsTime-startsTime
   
	#If the value found above maps to the complete database use the same trick to get the index of that time in the main database
    compStart = CompleteData.loc[CompleteData["reading_time"] == startsTime]
    if len(compStart) == 0:
		#but if the mapping fails, find the index of the last time the state was in the one we are interested in
        compStart = CompleteData.loc[CompleteData["State"] == 1].tail(1).index[0]
    else:
        compStart = compStart.index[0]
	#If the value found above maps to the complete database use the same trick to get the index of that time in the main database
    compEnd = CompleteData.loc[CompleteData["reading_time"] == endsTime]
    if len(compEnd) == 0:
		#but if the mapping fails, find the index of the last time the state was in the one we are interested in
        compEnd = CompleteData.loc[CompleteData["State"] == 0].tail(1).index[0]
    else:
        compEnd = compEnd.index[0]
	#we now have the data where we were asleep during the day
    night = CompleteData.loc[compStart:compEnd]
    #And avaraging the sleep depth during that period we can quantize sleep quality 
    sleepScore = night["State"].mean()
	#return the values of interest 
    return sleepTime, sleepScore


#CompleteDataLimited, CompleteDataSmoothed, CompleteData = DataLoader('mysql+pymysql://processing:WereSleep65000@192.168.0.110/esp_data')
#sleepTime, sleepScore = sleepCalc('mysql+pymysql://processing:WereSleep65000@192.168.0.110/esp_data', CompleteData)
