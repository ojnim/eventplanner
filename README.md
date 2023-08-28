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

2. Backend Architecture
    Python, Flask

3. Routes/Endpoints

4. DBscheme
    MongoDB

-users = { "_id": ObjectId(), 
            "username":"", 
            "email":"", 
            "password":"", 
            "events_participated":[] } 

-event = { "_id": ObjectId(), 
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
google map api
--> show event location
connect to google drive 
-->help participants easily share photos
implement a function to delete information
-->including user account and checklist
add an eventcode copy button