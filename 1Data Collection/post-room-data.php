<?php
/*
This script takes the HTTP request and then uses SQL to insert the information into the database
This script is triggered by HTTP requests sent from the ESP-32s
If the LAMP server is setup correctly no additional prep work is needed 
*/
//give the php script the credentials to connect to the SQL database
$servername = "localhost";
$dbname = "esp_data";
$username = "root";
$password = "WereSleep65000";

//API key to ensure that data is coming from only the ESP-32s
$api_key_value = "tPmAT5Ab3j7F9Room";
//reset and initiate all of the variables 
$api_key = $value1 = $value2 = $value3 = $reading_time;
//if we get a HTTP POST request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    //get the API key from the POST request
    $api_key = test_input($_POST["api_key"]);
    //if the API key is correct
    if($api_key == $api_key_value) {
        //get all of the values from the POST request        
        $value1 = test_input($_POST["value1"]);
        $value2 = test_input($_POST["value2"]);
        $value3 = test_input($_POST["value3"]);
        $reading_time = test_input($_POST["reading_time"]);
        
        //Connect to the MySQL database
        $conn = new mysqli($servername, $username, $password, $dbname);
        //If it fails to connect
        if ($conn->connect_error) {
            //kill the connection
            die("Connection failed: " . $conn->connect_error);
        } 
        //create the SQL query
        $sql = "INSERT INTO SensorDataRoom (value1, value2, value3, reading_time)
        VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $reading_time . "')";
        //send the query and see if it was accepted
        if ($conn->query($sql) === TRUE) {
            //if it worked return success 
            echo "success";
        } 
        else {
            //if not return the error
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
        //kill the SQL connection
        $conn->close();
    }
    else {
        echo "Wrong API Key provided.";
    }

}
#If it is not a HTTP POST (so for example a GET request that a browser would make) return an error
else {
    echo "No data posted with HTTP POST.";
}
//function for cleaning up the data received
//any characters that are not numbers or letters are removed
function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
