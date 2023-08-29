#RESTful API 
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, redirect, url_for, request
import certifi
from bson.objectid import ObjectId
import hashlib
import datetime
import jwt
from setup import GoogleCalendar
import googleapiclient

app = Flask(__name__)

ca = certifi.where()

#mongodb connection
uri = "mongodb+srv://testuser:jeYttReIgKgnxLUr@toyprojectevent.e7iuhkk.mongodb.net/"
client = MongoClient(uri, tlsCAFile=ca)
db = client.event

SECRET_KEY = 'tokenkey'


#first page
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try: 
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload["userid"]
        username = payload["username"]
        return render_template('userpage.html', userid=userid, username=username)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("loginpage"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("loginpage", msg="login info does not exist"))

#html template
@app.route('/loginpage')
def loginpage(): 
    msg = request.args.get("msg")
    return render_template('loginpage.html', msg=msg)

@app.route('/event/<eventcode>')
def eventpage(eventcode):
    return render_template('eventpage.html', eventcode=eventcode)

#[sign up api]
@app.route('/user', methods=['POST'])
def api_register():
    username_receive = request.form['username_give']
    useremail_receive = request.form['useremail_give']
    userpw_receive = request.form['userpw_give']
    
    userid = ObjectId()
    
    pw_hash = hashlib.sha256(userpw_receive.encode('utf-8')).hexdigest()

    db.users.insert_one({
        '_id':userid,
        'username':username_receive, 
        'email':useremail_receive, 
        'password':pw_hash,
        'events_participated':[]})
    return jsonify({'result':'success'})

#[sign in api]
@app.route('/login', methods=['POST'])
def api_login():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'email':email_receive, 'password':pw_hash})
    
    #jwt token
    if result is not None:
        userid = result.get('_id')
        username = result.get('username')
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800),
            'userid': str(userid),
            'username': username,
            'email': email_receive
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result':'success', 'token':token})
    else:
        return jsonify({'result':'fail', 'msg':'email and password do not match'})

#[user's eventlist get api]
@app.route('/user/<userid>/eventlist', methods=['GET'])
def userinfo(userid):
    userdata = db.users.find_one({"_id":ObjectId(userid)},{"events_participated":True})
    info = list(userdata.get("events_participated"))
    if info is None:
        return jsonify({'result':'None'})
    return jsonify({'result':'success', 'eventlist':info})

#[user's name get api]
@app.route('/user/<userid>/username', methods=['GET'])
def username_search(userid):
    data = db.users.find_one({'_id':ObjectId(userid)}, {'username':True})
    username = data.get('username')
    return jsonify({'result':'success', 'username':username})

#[events participated update api]
@app.route('/user/<userid>/eventsparticipated', methods=['PUT'])
def eventsparticipated_update(userid):
    eventcode_receive = request.form['eventcode_give']
    db.users.update_one({"_id":ObjectId(userid)},{"$addToSet": {"events_participated":eventcode_receive}})
    return jsonify({'result':'success'})

#[delete eventcode from user's events participated list api]
@app.route('/user/<userid>/event', methods=['DELETE'])
def eventcode_delete(userid):
    eventcode_receive = request.form['eventcode_give']
    db.users.update_one({'_id':ObjectId(userid)},{'$pull':{'events_participated':eventcode_receive}})
    return jsonify({'result':'success'})

#[event create api]
@app.route('/event', methods=['POST'])
def newevent():
    eventname_receive = request.form['eventname_give']
    eventcode = ObjectId()
    doc = {
        '_id': eventcode,
        'eventname':eventname_receive,
        'participants_list':[],
        'location':'',
        'timezone':'',
        'start':'',
        'end':'',
        'checklist':[]
    }
    db.events.insert_one(doc)
    return jsonify({'result':'success', 'eventcode':str(eventcode)})

#[participants list update api]
@app.route('/event/<eventcode>/participantslist', methods=['PUT'])
def participants_update(eventcode):
    userid_receive = request.form['userid_give']
    db.events.update_one({'_id':ObjectId(eventcode)},{"$addToSet":{'participants_list':userid_receive}})
    return jsonify({'result':'success'})

#[delete userid from event's participants list api]
@app.route('/event/<eventcode>/participantslist', methods=['DELETE'])
def participant_delete(eventcode):
    userid_receive = request.form['userid_give']
    db.events.update_one({'_id':ObjectId(eventcode)},{'$pull':{'participants_list':userid_receive}})
    return jsonify({'result':'success'})

#[event delete api]
@app.route('/event/<eventcode>', methods=['DELETE'])
def event_delete(eventcode):
    db.events.delete_one({'_id':ObjectId(eventcode)})
    return jsonify({'result':'success'})

#[event information get api]
@app.route('/event/<eventcode>/info1', methods=['GET'])
#called in several pages
def event_info(eventcode):
    eventdata = db.events.find_one({'_id':ObjectId(eventcode)},{'eventname':True, 'start':True, 'end':True})
    eventname = eventdata.get('eventname')
    eventstart = eventdata.get('start')
    eventend = eventdata.get('end')
    return jsonify({'result':'success','eventname':eventname, 'start':eventstart, 'end':eventend})

@app.route('/event/<eventcode>/info2', methods=['GET'])
#called in one page
def view_event(eventcode):
    eventdata2 = db.events.find_one({'_id':ObjectId(eventcode)},{'participants_list':True, 'location':True, 'timezone':True,'checklist':True})
    participants = list(eventdata2.get('participants_list'))
    location = str(eventdata2.get('location'))
    timezone = str(eventdata2.get('timezone'))
    checklist = list(eventdata2.get('checklist'))
    return jsonify({'result':'success','participants':participants,'location':location,'eventtimezone':timezone,'checklist':checklist})

#[checklist post api]
@app.route('/event/<eventcode>/checklist', methods=['POST'])
def post_eventinfo(eventcode):
    item_receive = request.form['item_give']
    db.events.update_one({'_id':ObjectId(eventcode)},{'$addToSet':{'checklist':item_receive}})
    return jsonify({'result':'success'})

#[event information update api]
@app.route('/event/<eventcode>/location', methods=['PUT'])
def update_location(eventcode):
    #change event location
    location_receive = request.form['location_give']
    db.events.update_one({'_id':ObjectId(eventcode)}, {'$set': {'location':location_receive}})
    return jsonify({'result':'success'})
@app.route('/event/<eventcode>/time', methods=['PUT'])
def update_eventstartend(eventcode):
    #change event start and end date/time
    timezone_receive = request.form['timezone_give']
    start_receive = request.form['start_give']
    end_receive = request.form['end_give']
    db.events.update_one({'_id':ObjectId(eventcode)}, {'$set': {'timezone':timezone_receive, 'start':start_receive,'end':end_receive}})
    #end update
    return jsonify({'result':'success'})

    #add and delete event checklist
"""
@app.route('/event/<eventcode>/checklist', methods=['PUT'])
def update_checklist():
    
    return jsonify()

#[checklist item delete api]
@app.route('/event/<eventcode>/checklist', methods=['DELETE'])
def item_delete(eventcode):
    item_receive = request.form['item_give']
    db.events.update_one({'_id':ObjectId(eventcode)},{'$pull':{'checklist':item_receive}})
    return jsonify({'result':'success'})
"""


#[google calendar API]
@app.route('/event/<eventcode>/calendar', methods=['POST'])
def calendar_create(eventcode):
    try:
        eventinfo = db.events.find_one({'_id':ObjectId(eventcode)},{'_id':False})
        eventname = eventinfo.get('eventname')
        eventlocation = eventinfo.get('location')
        participants = list(eventinfo.get('participants_list'))
        start = eventinfo.get("start")
        end = eventinfo.get("end")
        timezone = eventinfo.get("timezone")

        
        attendees = []
        for i in range(len(participants)):
            attendeeinfo = db.users.find_one({'_id':ObjectId(participants[i])},{'email':True})
            attendeeemail = attendeeinfo.get("email")
            attendees += [{'email':attendeeemail}]
        
        event = {
            'summary': eventname,
            'location': eventlocation,
            'description': '',
            'start': {'dateTime': start, 'timeZone': timezone},
            'end': {'dateTime': end, 'timeZone': timezone},
            'attendees': attendees,
        }
        print(event)
        
        google_calendar = GoogleCalendar()
        google_calendar.set_google_calendar(event)
        
        eventID = event['id']
        return jsonify({'result':'event created', 'gceventid':eventID})
    
    except googleapiclient.errors.HttpError:
        return jsonify({'result':'httperror'})

"""
@app.route('/event/<eventcode>/calendar', methods=['PUT'])
def calendar_update(eventcode):
    service = get_service()
    update_receive = request.form['update_give']
    event = service.events().get(calendarId='primary', eventId='eventId').execute()
    event[''] = update_receive
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
"""

@app.route('/event/<eventcode>/calendar', methods=['DELETE'])
def calendar_delete(eventcode):
    try:
        service.events().delete(calendarId='primary', eventId='eventId').execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event in google calendar")
#case: already deleted event in google calendar seperately, not in this web app

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug = True)