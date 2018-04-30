$(function () {
            // Decide between ws:// and wss://
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
            console.log("Connecting to " + ws_path);
            var socket = new ReconnectingWebSocket(ws_path);

            // Handle incoming messages
            socket.onmessage = function (message) {
                // Decode the JSON
                console.log("Got websocket message " + message.data);
                var data = JSON.parse(message.data);
                // Handle errors
                if (data.error) {
                    alert(data.error);
                    return;
                }
                // Handle joining
                if (data.join) {
                    console.log("Joining room " + data.join);
                    var roomdiv = $(

                        "<div class='col-sm-3 col-sm-offset-1 frame' id='room-" + data.join + "'> " +
                        "<lable class='navbar-brand'style='text-align:center;height:200px;width:265px;color:white;background-color:#FF6666'>" + data.title + "</lable>" +
                            "<ul class='messages'></ul>"+
                            "<div>"+
                                "<form><div class='msj-rta macro' style='width:260px' >"+
                                    '<div  style="background:whitesmoke">'+
                                        '<input class="mytext" placeholder="Type a message"/></div>'+
                                        '<button  class="btn btn-info btn-sm"><span class="glyphicon glyphicon-share-alt"></span></button></div>'+
                                        '</form>'+
                                '</div></div>'
                        );
                    // Hook up send button to send a message
                    roomdiv.find("form").on("submit", function () {
                        socket.send(JSON.stringify({
                            "command": "send",
                            "room": data.join,
                            "message": roomdiv.find("input").val()
                        }));
                        roomdiv.find("input").val("");
                        return false;
                    });
                    $("#chats").append(roomdiv);
                    // Handle leaving
                } else if (data.leave) {
                    console.log("Leaving room " + data.leave);
                    $("#room-" + data.leave).remove();
                    // Handle getting a message
                } else if (data.message || data.msg_type != 0) {
                    var msgdiv = $("#room-" + data.room + " .messages");
                    var ok_msg = "";
                    // msg types are defined in chat/settings.py
                    switch (data.msg_type) {
                        case 0:
                             var time = new Date();
                             var current_user = $("#user_id").html();
                             if(parseInt(data.user_id) == parseInt(current_user)){
                                 ok_msg = '<li style="width:100%;">' +
                                '<div class="msj-rta macro">' +
                                '<div class="text text-r">' +
                                '<p>'+data.message+'</p>' +
                                '<p><small>'+time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds()+'</small></p>' +
                                '</div>' +
                                '<div class="avatar" style="padding:0px 0px 0px 10px !important"><a href="/OOTD/profile/'+data.user_id+'">'+ data.username +'</a></div>' +
                                '</li>'}
                             else{
                                ok_msg = '<li style="width:100%;">' +
                                '<div class="msj macro">' +
                                '<div class="avatar" style="padding:0px 0px 0px 10px !important"><a href="/OOTD/profile/'+data.user_id+'">'+ data.username +'</a></div>' +
                                '<div class="text text-r">' +
                                '<p style="text-align:right">'+data.message+'</p>' +
                                '<p><small>'+time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds()+'</small></p>' +
                                '</div>' +
                                '</li>'
                             }
                            break;
                        case 1:
                            // Warning / Advice messages
                            ok_msg = "<div class='contextual-message text-warning'>" + data.message +
                                    "</div>";
                            break;
                        case 2:
                            // Alert / Danger messages
                            ok_msg = "<div class='contextual-message text-danger'>" + data.message +
                                    "</div>";
                            break;
                        case 3:
                            // "Muted" messages
                            ok_msg = "<div class='contextual-message text-muted'>" + data.message +
                                    "</div>";
                            break;
                        case 4:
                            // User joined room
                            ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                                    " joined the room!" +
                                    "</div>";
                            break;
                        case 5:
                            // User left room
                            ok_msg = "<div class='contextual-message text-muted'>" + data.username +
                                    " left the room!" +
                                    "</div>";
                            break;
                        default:
                            console.log("Unsupported message type!");
                            return;
                    }
                    msgdiv.append(ok_msg);

                    msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
                } else {
                    console.log("Cannot handle message!");
                }
            };

            // Says if we joined a room or not by if there's a div for it
            inRoom = function (roomId) {
                return $("#room-" + roomId).length > 0;
            };

            // Room join/leave
            $("li.list-group-item").click(function () {
                roomId = $(this).attr("data-room-id");
                if (inRoom(roomId)) {
                    // Leave room
                    $(this).removeClass("joined");
                    socket.send(JSON.stringify({
                        "command": "leave",
                        "room": roomId
                    }));
                } else {
                    // Join room
                    $(this).addClass("joined");
                    socket.send(JSON.stringify({
                        "command": "join",
                        "room": roomId
                    }));
                }
            });

            // Helpful debugging
            socket.onopen = function () {
                console.log("Connected to chat socket");
            };
            socket.onclose = function () {
                console.log("Disconnected from chat socket");
            }
        });