1. Folder Structure

   eventplanner

        ├──README.md 

        ├──app.py 

        ├──GoogleCalendar_setup.py 

        ├──credentials.json 

        ├──static

        │   ├──css

        │   └──js

        │       └──eventplannerJSfile.js

        └──templates 

            ├──eventpage.html

            ├──loginpage.html 

            └──userpage.html


3. Backend Architecture

    Python, Flask


4. Routes/Endpoints


5. DBscheme

    MongoDB


users = 

            { "_id": ObjectId(), 

            "username":"", 
            
            "email":"", 
            
            "password":"", 
            
            "events_participated":[] } 



event = 

            { "_id": ObjectId(), 

            "eventname":"", 
            
            "participants_list":[], 
            
            "location":"", 
            
            "timezone":"", 
            
            "start":"", 
            
            "end":"", 
            
            "checklist":[] }



5. Frontend Architecture

    HTML, CSS, JavaScript



6. Future Update Plan

Error and General Update

consider edge cases

debug google calendar error


Advanced Functions

google map API

--> show event location

connect to google drive 

-->help participants easily share photos

implement a function to delete information

-->including user account and checklist

add an eventcode copy button
