###
#This file generates the web app with the user dashboard
###
#import relevant libraries
#dash is the webapp framework
import dash
from dash import dcc, html, dash_table
#bootstrap components for the visuals
import dash_bootstrap_components as dbc
#plotly and pandas are used for the mathematical displays
import plotly.express as px
import pandas as pd
#To do some calculations with time
import datetime as dt
#this file holds additional functions needed to make this code readable
import AdditionalFun as af
#defines the Dash app and loads in the CSS for the visuals 
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
#This loads the data from the SQL server
CompleteDataLimited, CompleteDataSmoothed, CompleteData = af.DataLoader('mysql+pymysql://processing:WereSleep65000@192.168.0.110/esp_data')

####here all the plots and visuals are defined
#shows you the current day
today = "on the night of " + str(dt.date.today())
##calculates the sleep time and score, see AdditionalFun.py
sleepTime, sleepScore = af.sleepCalc('mysql+pymysql://processing:WereSleep65000@192.168.0.110/esp_data',CompleteData)
#gets the last illumination value present and then coverts it to a percentage
Illumination = str(round(CompleteDataSmoothed["illumination"].iat[-1]*100,2))
#gets the last age of the moon
Cycle = str(round(CompleteDataSmoothed["age"].iat[-1]))
#sums the amount of light outside
totalLightOutside = (CompleteData["RedWindow"].iat[-1]) + (CompleteData["GreenWindow"].iat[-1]) + (CompleteData["BlueWindow"].iat[-1])
#takes the average of the sleep values
avLightOutside = str(round(totalLightOutside/3))
#finds the maximum value between the three colours and returns the column ID of the highest one
maxColour = CompleteData[["RedWindow","GreenWindow","BlueWindow"]].tail(1).idxmax(axis=1)

#defines the line graphs with all the data
figComplete = px.line(CompleteData,x = "reading_time", y= ["illumination",	"age",	"diameter",	"RedRoom",	"GreenRoom",	"BlueRoom",	"RedWindow",	"GreenWindow",	"BlueWindow",	"State" ])
figCompleteDataSmoothed = px.line(CompleteDataSmoothed,x = "reading_time", y= ["illumination",	"age",	"diameter",	"RedRoom",	"GreenRoom",	"BlueRoom",	"RedWindow",	"GreenWindow",	"BlueWindow",	"State" ])
figCompleteDataLimited = px.scatter(CompleteDataLimited,x = "reading_time", y= ["illumination",	"age",	"diameter",	"RedRoom",	"GreenRoom",	"BlueRoom",	"RedWindow",	"GreenWindow",	"BlueWindow",	"State" ])
#defines the box plots
boxComplete = px.box(CompleteData, y= ["illumination",	"age",	"diameter",	"RedRoom",	"GreenRoom",	"BlueRoom",	"RedWindow",	"GreenWindow",	"BlueWindow",	"State" ])
boxCompleteDataLimited = px.box(CompleteDataLimited, y= ["illumination",	"age",	"diameter",	"RedRoom",	"GreenRoom",	"BlueRoom",	"RedWindow",	"GreenWindow",	"BlueWindow",	"State" ])

#builds the correlation table from the data
corrTable = abs(round(CompleteDataLimited.corr(),2))
#removes the redundant data from the corelation table
corrList = corrTable.tail(1).sort_values("State", axis=1,ascending= False)
del corrList["State"]
#gets the top 3 correlations and their values
best1 = corrList.columns[0]
best1corr = corrList[corrList.columns[0]].iloc[0]
best2 = corrList.columns[1]
best2corr = corrList[corrList.columns[1]].iloc[0]
best3 = corrList.columns[2]
best3corr = corrList[corrList.columns[2]].iloc[0]

###
#this section is the layout of the webpage
#It just takes the data above and adds text to make it look better, as well as defining the layout using html-like structure
###
app.layout = html.Center(children=[
    html.H1(children='WereSleep Data Dashboard',style={'padding': 20}),
    html.Div(children='A live data dashboard showing your most recent sleep performance and factors that might affect it. At the end of the page, you will see which of these factors we found are relevant and which are not.'),

    
    html.H2(children='Sleep Statistics',style={'padding': 30}),
    html.Div(children='How well you slept last night.'),
    html.Div(children=today),
    dbc.Row([
            dbc.Col([
                html.Div(children="you slept for:"),
                html.H2(children=str(sleepTime)[7:] + " hours"),
            ]),
            dbc.Col([
                html.Div(children="With a sleep score of:"),
                html.H2(children = str(round(sleepScore,2)) + "/4"),
            ]), 
        ]),
    
    html.H2(children='Moon & Light Statistics',style={'padding': 30}),
    html.Div(children='The current state of the moon and the light values outside your window.'),
    dbc.Row([
            dbc.Col([
                html.Div(children="The moon is currently"),
                html.H2(children=Illumination + "%"),
                html.Div(children="of its maximum illumination"),
            ]),
            dbc.Col([
                html.Div(children="The moon is"),
                html.H2(children=Cycle+ " days"),
                html.Div(children="Through its lunar cycle"),
            ]),
            dbc.Col([
                html.Div(children="The light outside is "),
                html.H2(children = avLightOutside),
                html.Div(children="units of light on average, with the brighest colour being " + maxColour),
            ]), 
        ]),
    html.H2(children='Time-series Analysis',style={'padding': 30}),
    html.Div(children='''
        The data gathered so far in this experiment and the current running correlations.
        The graphs are fully interactable, click the home icon in the top left corner to reset the axis, and you can enable and disable variables by clicking on their name to look at specific values and correlations.

    ''',style={'padding': 10}),
    html.H3(children="The top 3 values that affect sleep the most are:",style={'padding': 10}),
    dbc.Row([
            dbc.Col([
                html.Div(children= best1 + " with a correlation factor of"),
                html.H2(children=best1corr),
            ]),dbc.Col([
                html.Div(children= best2 + " with a correlation factor of"),
                html.H2(children=best2corr),
            ]),dbc.Col([
                html.Div(children= best3 + " with a correlation factor of"),
                html.H2(children=best3corr),
            ]),
        ]),
    html.H3(children='Table showing all the correlations',style={'padding': 10}),
    html.Div([
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in corrList.columns],
    data=corrList.to_dict('records'),
    )]),

     
    html.H3(children='The complete dataset',style={'padding': 10}),
    dcc.Graph(
        id='figComplete',
        figure=figComplete
    ),
    html.H2(children='Additional visuals',style={'padding': 30}),
    html.Div(children='complete data about the project for you to analyse'),
    html.H3(children='The complete data smoothed over 30s intervals',style={'padding': 10}),
    dcc.Graph(
        id='figCompleteDataSmoothed',
        figure=figCompleteDataSmoothed
    ),
    html.H3(children='The complete data smoothed over 30s intervals with the day removed',style={'padding': 10}),
    dcc.Graph(
        id='figCompleteDataLimited',
        figure=figCompleteDataLimited
    ),
      dbc.Row([
            dbc.Col([
                html.H3(children='Box plot for complete data',style={'padding': 10}),
                dcc.Graph(
                    id='boxCompleteData',
                    figure=boxComplete
                ),
            ]), 
            dbc.Col([
                html.H3(children='Box plot for limited data',style={'padding': 10}),
                dcc.Graph(
                    id='boxCompleteDataLimited',
                    figure=boxCompleteDataLimited
                ),
            ]), 
        ]),
],style={'padding': 10})


#These two lines define the location of the webapp and run it
if __name__ == '__main__':
    app.run_server(debug=False,port=8080,host="0.0.0.0")
