//loginpage
function login() {
    $.ajax({
        type: 'POST',
        url:'/login',
        data:{email_give: $('#loginemail').val(), pw_give: $('#loginpw').val()},

        success: function(response){
            if (response['result']=='success'){
                $.cookie('mytoken', response['token']); 
                alert('login complete')
                window.location.href = '/'
            }
            else {
                alert(response['msg'])
            }
        }
    })
}

function register(){
    let useremail = $('#useremail').val();
    let userpw = $('#userpw').val();
    let username = $('#username').val();

    if(username.trim() === ''){
        alert('User name cannot be blank.');
        return;
    }

    $.ajax({
        type: 'POST',
        url: '/user',
        data: {
            useremail_give: useremail,
            userpw_give: userpw,
            username_give: username
        },
        success: function(response){
            if (response['result']=='success'){
                alert('sign up complete')
                window.location.href = '/loginpage'
            }
            else {
                alert(response['msg'])
            }
        }
    })
}

//userpage
function logout(){
    $.removeCookie('mytoken');
    alert('logout complete')
    window.location.href='/loginpage'
}

function event_detail(eventcode) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            type: 'GET',
            url: '/event/' + eventcode + '/info1',
            data: {},
            success: function (response) {
                if(response["result"]=="success"){
                    console.log(response);
                    resolve(response);
                }
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}

function createevent(){
    const eventname = $('#event-name').val();
    if (eventname.trim() === '') {
        alert('Event name cannot be blank.');
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/event',
        data: {eventname_give: eventname},
        success: function(response){
            if(response["result"]=="success"){
                console.log(response)
                let eventcode = response["eventcode"];
                EnterEventandUpdateParticipants(eventcode);
            }
        },
        error: function(error){
            console.error("Error creating new event: ", error)
        }
    })
}

//eventpage

function username_get(userid){
    return new Promise(function (resolve, reject){
        $.ajax({
            type: 'GET',
            url: '/user/'+ userid +'/username',
            data: {},
            success: function(response){
                console.log(response);
                resolve(response);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}

function user_leave(){
    //potential error
    for (let i=0;i<participants_list.length;i++){
        $.ajax({
            type: 'DELETE',
            url: '/user/'+ participants_list[i] + '/event',
            data: {eventcode_give:'{{eventcode}}'},
            success: function(response){
                console.log(response)
            }
        })
    }
    event_delete();
}
