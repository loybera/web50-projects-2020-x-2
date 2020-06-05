$(document).ready(function() {

    function fn_Title_Case(string) {
        var sentence = string.toLowerCase().split(" ");
        for(var i = 0; i< sentence.length; i++){
           sentence[i] = sentence[i][0].toUpperCase() + sentence[i].slice(1);
        }
     sentence.join(" ");
     return sentence[0];
     }

  // name of the namespace (optional).
  namespace = '/chat';

  // Connect to the Socket.IO server.
  //     http[s]://<domain>:<port>[/<namespace>]
  var socket = io(namespace);

    // template for admin messages 
    const broadcast_msg_template = Handlebars.compile(document.querySelector('#broadcast_msg_template').innerHTML);
    function add_broadcast_msg(channel, post, post_info) {

        // Create new post.
        const msg = broadcast_msg_template({'post': post, 'post_info': post_info});
        // Add post to DOM.
        var divId = 'msg_history_'+ channel;

        // Add post to DOM in the channel.
        if (document.querySelector('#'+divId) == null){
            console.log('add_broad: msg_history_'+channel+' no existe como ID');
        } 
        else {
            document.querySelector('#'+divId).innerHTML += msg;
        }



        
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    // template for input message (others message) 
    const in_msg_template = Handlebars.compile(document.querySelector('#in_msg_template').innerHTML);
    function add_in_msg(channel, post, post_user_to, post_user_from, post_info, post_image, post_id) {

        // Create new post.
        const msg = in_msg_template({'post': post,  'post_user_from': post_user_from, 'post_user_to': post_user_to, 'post_info': post_info, 'post_image': post_image, 'post_id': post_id});

        // Add post to DOM.
        var divId = 'msg_history_'+ channel;
        if (document.querySelector('#'+divId)  == null){
            console.log('add_in: msg_history_'+channel+' no existe como ID');
        } 
        else {
            document.querySelector('#'+divId).innerHTML += msg;
        }
         // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    // template for output message (own message) 
    const out_msg_template = Handlebars.compile(document.querySelector('#out_msg_template').innerHTML);
    function add_out_msg(channel, post, post_user_from, post_info, post_id) {

        // Create new post.
        const msg = out_msg_template({'post': post, 'post_user_from':post_user_from, 'post_info': post_info, 'post_id': post_id});

        // Add post to DOM.
        var divId = 'msg_history_'+channel;
        if (document.querySelector('#'+divId) == null){
            console.log('add_out: msg_history_'+channel+' no existe como ID');
        } 
        else {
            document.querySelector('#'+divId).innerHTML += msg;
        }

        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    // template for channel list joined div  (lateral left bar)
    const join_chn_template = Handlebars.compile(document.querySelector('#join_chn_template').innerHTML);
    function add_channel(parentElement, channel, channel_label, channel_image, channel_type, channel_user_from, channel_user_to) {

        // Create new post.
        const msg = join_chn_template({'channel': channel, 'channel_label': channel_label, 'channel_image': channel_image, 'channel_type': channel_type, 'channel_user_from': channel_user_from, 'channel_user_to': channel_user_to});

        // Add post to DOM.
        if (document.querySelector('#'+parentElement) == null){
            console.log("error to create channel in channel list joined");
        }
        else {
            document.querySelector('#'+parentElement).innerHTML += msg;
        }
        // scroll down to show new DOM
        var objDiv = document.getElementById(parentElement);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    // template for modal windows with channels for join
    const modal_join_chn_template = Handlebars.compile(document.querySelector('#modal_join_chn_template').innerHTML);
    function add_channel_modal(parentElement, channel, channel_label, channel_image, channel_type, channel_user_from, channel_user_to) {

        // Create new post.
        const msg = modal_join_chn_template({'channel': channel, 'channel_label': channel_label, 'channel_image': channel_image, 'channel_type': channel_type, 'channel_user_from': channel_user_from, 'channel_user_to': channel_user_to});

        // Add post to DOM.
        // document.querySelector('#'+parentElement).innerHTML += msg;
        document.getElementById(parentElement).innerHTML +=msg;

    }

    // Initialize user channels join it at load
    //   window.onload = function() {
    
    list = document.getElementsByClassName("chat_list")
    username = $('#username').val();
    username_label = $('#username_label').val();
    // user_from = $('#user_id').val().toUpperCase();

    for (var i = 0; i < list.length; i++){
    
        channel = list[i].getAttribute('id');
        channel_type = document.getElementById(channel+"_type").value;
        if ( channel_type == 'PUBLIC'){
            console.log("emit public join room: "+channel);
            socket.emit('join', {room:channel, room_type: channel_type});
        } else {
            console.log("emit private join room: "+channel);
            socket.emit('join_user', {room:channel, room_type: channel_type, user_from: username, create_room: 'False' });
    
        }        
    }
    
    if (list.length>0){
        $(".msg_history").hide();
        $("#type_msg").hide();
        $(".msg_history#msg_history_0").show();
        $("#type_msg_0").show();


    }
    else
    {
        $("#type_msg").hide();
        $("#type_msg_0").show();
    }

    // };

    document.getElementById('btn_leave_room').style.visibility = 'hidden';
    
    
     
    //-------------------------------------------------------------
    //  click en chat list
    // change msg history and  header
    //-------------------------------------------------------------
    $('div.inbox_chat').on("click", "div.chat_list", function(){
        var channel = $(this).attr('id');
        var channel_label = $('h5#'+channel+'_name').text() 
        var channel_image = $('img#'+channel+'_img').attr('src');
        var channel_type =  $('input#'+channel+'_type').attr('value');

        // document.getElementById("msgs_top_label_room").innerHTML=channel;
        document.getElementById("msgs_top_label").innerHTML=channel_label;
        document.getElementById("msgs_top_img").src = channel_image;

        if (channel_type == 'PRIVATE'){
            document.getElementById('btn_leave_room').style.visibility = 'visible'; //for now, may be be 'hidden'
            document.getElementById('btn_leave_user_to_value').value= channel;
        } else {
            document.getElementById('btn_leave_room').style.visibility = 'visible';
            document.getElementById('btn_leave_user_to_value').value= channel;

        }
        document.getElementById('btn_leave_room_value').value= channel;


        $(".msg_history").hide();
        $(".msg_history#msg_history_"+channel).show();
        $("#type_msg").show();
        $("#type_msg_0").hide();
        $('div.chat_list').not(this).removeClass('active_chat')
        $(this).addClass('active_chat');
        $("#room_name").val(channel);
        $("#room_type").val(channel_type);

    });

    function fn_join_user(user_to, user_from, channel, channel_label, channel_image, channel_type ) {
        //fix image path 
        
        // change top label room name
        document.getElementById("msgs_top_label").innerHTML = channel_label;
        document.getElementById("msgs_top_img").src = channel_image;
        document.getElementById('btn_leave_room').style.visibility = 'show';
        document.getElementById('btn_leave_room_value').value= channel;
        document.getElementById('btn_leave_user_to_value').value= user_to;


        var create_room = 'True';
        if (document.getElementById(channel) == null){
            //add user to channel list
            // if($(".chat_list#"+channel).length == 0) {
                var divId = 'inbox_chat';
                add_channel(divId, channel, fn_Title_Case(channel_label), channel_image, channel_type, user_from, user_to);
                $('div.chat_list').not($("#"+channel)).removeClass('active_chat')
                $(".chat_list#"+channel).addClass('active_chat');
                $("#room_name").val(channel);
                $("#room_type").val(channel_type);
                $("#type_msg").show();
                $("#type_msg_0").hide();
        
            } else {
            //active user in channel list
                create_room = 'False';
                $('div.chat_list').not($("#"+channel)).removeClass('active_chat')
                $(".chat_list#"+channel).addClass('active_chat');
                $("#room_name").val(channel);
                $("#room_type").val(channel_type);
                $("#type_msg").show();
                $("#type_msg_0").hide();
        }

        // add chat message history box
        $(".msg_history").hide();
        if (document.getElementById( "msg_history_"+channel) == null){

            var attrId = document.createAttribute("id");
            attrId.value= "msg_history_"+channel;

            var msgHistory = document.createElement("div");
            msgHistory.classList.add("msg_history");
            msgHistory.setAttributeNode(attrId);

            msgBefore =  document.getElementsByClassName("type_msg")[0];
            document.getElementById("msgs").insertBefore(msgHistory, msgBefore);

            //sent create room-user
            socket.emit('join_user', {room: channel, user_from: user_from, user_to: user_to, create_room: create_room, room_type: channel_type});


        } else {
            $(".msg_history#msg_history_"+channel).show();
        }

       
    }

    
    // channel name for private conversation, ordenated alphabetically
    function fn_get_channel(userto, userfrom){
        var str = [userto, userfrom];
        str.sort();
        return str[0]+'__to__'+str[1];

    }
    //-------------------------------------------------------------
    //  click en chat to user
    // add new channel user to user 
    //-------------------------------------------------------------
    $(document).on('click','div.received_withd_msg',function () {

        //only if click into the public channel to go to private channel
        if ($("#room_type").attr('value') == 'PUBLIC'){

            var msg_id = $(this).attr('id');
            var user_to = $("#received_msg_user_from_"+msg_id).attr('value');
            
            //TODO: delete received_msg_user_+channel from template_in

            // var from_channel = $("#channel__"+msg_id).attr('value');
            var user_from = username;
            var channel = fn_get_channel(user_to, user_from);
            var channel_label = fn_Title_Case(user_to);
            var channel_image = $("#received_msg_user_img_"+msg_id).attr('value');
            var channel_type = 'PRIVATE';

            fn_join_user( user_to, user_from, channel, channel_label, channel_image, channel_type);

        }
        return false


    });


  
  // Event handler for new connections.
  // The callback function is invoked when a connection with the
  // server is established.
  socket.on('connect', function() {
      socket.emit('my_event', {data: 'I\'m connected!'});
  });

  // Event handler for server sent data.
  // The callback function is invoked whenever the server emits data
  // to the client. The data is then displayed in the "Received"
  // section of the page.
  socket.on('my_room', function(msg, cb) {
    // console.log("recibe canal:"+channel);
    var channel = msg.room; //document.getElementById("room_name").value;
    if (channel) {

        if (msg.user_from  == username){
                add_out_msg(channel=channel, post=msg.data, post_user_from=msg.user_from, post_info= msg.time, post_id=msg.id );
        } else {
            if (msg.user_from=='admin'){
                add_broadcast_msg(channel=channel, post=msg.data, post_info=msg.time);
            } else {    
                add_in_msg(channel=channel, post=msg.data, post_user_to= msg.user_to, post_user_from= msg.user_from, post_info=msg.time, post_image=msg.user_image, post_id=msg.id);
            }   

        }
     }else {
        $('#log').append('<li>No channel:' + $('<div/>').text(   msg .data ).html());
        // scroll down to show new DOM
        var objDiv = document.getElementById("log");
        objDiv.scrollTop = objDiv.scrollHeight;
    }

      if (cb)
          cb();
  });

  socket.on('my_response', function(msg, cb) {
      $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
      // scroll down to show new DOM
      var objDiv = document.getElementById("log");
      objDiv.scrollTop = objDiv.scrollHeight;

      if (msg.messages !== undefined && msg.messages !== null){
        for (var i = 0; i < msg.messages.length; i++){
            json_msg = JSON.parse(msg.messages[i])
            console.log(json_msg);

            if (json_msg.user_from == username ){
                    add_out_msg(channel=msg.room, post=json_msg.post, post_user_from=json_msg.user_from, post_info= json_msg.time, post_id=json_msg.id);
            } else {
                if (json_msg.user_from =='admin'){
                    add_broadcast_msg(channel=msg.room, post=json_msg.post, post_info=json_msg.time);
                } else { 
                    add_in_msg(channel=msg.room, post=json_msg.post, post_user_to= json_msg.user_to, post_user_from= json_msg.user_from, post_info= json_msg.time, post_image= json_msg.user_from_img, post_id=json_msg.id);
                }
            }
      } 
    }
    if (cb)
        cb();
  });

  socket.on('my_join_user', function(msg, cb) {
    // Log with scroll down to show new DOM
    $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    var objDiv = document.getElementById("log");
    objDiv.scrollTop = objDiv.scrollHeight;

    var channel = msg.room;
    var channel_type = 'PRIVATE';
    var user_image = "/static/img/user/"+msg.user_image+".png";

    console.log('compare '+username + 'user_to: '+msg.user_to);

    // if user logged is the user destination join the channel
    if (username == msg.user_to  ){
        console.log('OK'+username + 'user_to: '+msg.user_to);
        //join if not exists
        if($(".chat_list#"+channel).length > 0) {
            console.log("channel user already conected");
        } else {
            fn_join_user(msg.user_from, msg.user_to, msg.room, msg.user_from, user_image, channel_type);
        }
    }

    
    if (cb)
    cb();
});

  socket.on('my_response_user', function(msg, cb) {
    $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    // scroll down to show new DOM
    var objDiv = document.getElementById("log");
    objDiv.scrollTop = objDiv.scrollHeight;
    var channel = msg.room;
    console.log(msg.room, msg.original_room);
    if (msg.room != msg.original_room){
        console.log('update room:'+msg.room +' instead of '+ msg.original_room);
        //must to change the div id
        document.getElementById(msg.original_room).id = msg.room;
        var user_from = msg.user_from;
        var channel_label = fn_Title_Case(msg.user_to);
        var channel_type = 'PRIVATE';

        // change top label room name
        document.getElementById('btn_leave_room_value').value= channel;
        document.getElementById('btn_leave_user_to_value').value= msg.user_to;

        $("#room_name").val(channel);
        $("#room_type").val(channel_type);
        $("#type_msg").show();
        $("#type_msg_0").hide();

        // add chat message history box
        $(".msg_history").hide();
        $(".msg_history_#"+msg.original_room).remove();

        var attrId = document.createAttribute("id");
        attrId.value= "msg_history_"+channel;
    
        var msgHistory = document.createElement("div");
        msgHistory.classList.add("msg_history");
    
        msgHistory.setAttributeNode(attrId);
        msgBefore =  document.getElementsByClassName("type_msg")[0];
        document.getElementById("msgs").insertBefore(msgHistory, msgBefore);

    }

    if (msg.messages !== undefined && msg.messages !== null){
      for (var i = 0; i < msg.messages.length; i++){
          json_msg = JSON.parse(msg.messages[i])
          console.log(json_msg);

          // add_in_msg(msg.messages[i], 'User' + ' | '+ 'Fecha Hora');
          if (json_msg.user_from == username){
                add_out_msg(channel=msg.room, post=json_msg.post, post_user_from=json_msg.user_from, post_info=  json_msg.time, post_id=json_msg.id);
          } else {
              if (json_msg.user_from=='admin'){
                  add_broadcast_msg(channel=msg.room, post=json_msg.post, post_info=json_msg.time);
              } else { 
                  add_in_msg(channel=msg.room, post=json_msg.post, post_user_to= json_msg.user_to, post_user_from= json_msg.user_from, post_info= json_msg.time, post_image= json_msg.user_from_img, post_id=json_msg.id);
              }
          }
    } 
  }
  if (cb)
      cb();
});
 
  // Handlers for the different forms in the page.
  // These accept data from the user and send it to the server in a
  // variety of ways
  $('form#emit').submit(function(event) {
      socket.emit('my_event', {data: $('#emit_data').val()});
      $('#emit_data').val('');
      return false;
  });
  $('form#broadcast').submit(function(event) {
      socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
      return false;
  });



  // Create public channel 
  $('form#create').submit(function(event) {

    var channel_label = $('#create_room').val();
    var channel_image = '/static/img/user/new-channel.png';
    var channel_type = 'PUBLIC';

    // make channel id
    channel = channel_label.replace(/[^A-Z0-9]+/ig, "").toLowerCase();

    // document.getElementById("msgs_top_label_room").innerHTML = channel;
    document.getElementById("msgs_top_label").innerHTML = channel_label;
    document.getElementById("msgs_top_img").src = channel_image;

    document.getElementById('btn_leave_room').style.visibility = 'visible';
    document.getElementById('btn_leave_room_value').value= channel;  
    document.getElementById('btn_leave_user_to_value').value= channel;

    

    $(".msg_history").hide();
    var attrId = document.createAttribute("id");
    attrId.value= "msg_history_"+channel;

    var msgHistory = document.createElement("div");
    msgHistory.classList.add("msg_history");

    msgHistory.setAttributeNode(attrId);
    msgBefore =  document.getElementsByClassName("type_msg")[0];
    document.getElementById("msgs").insertBefore(msgHistory, msgBefore);

    $('div.chat_list').not($("#"+channel)).removeClass('active_chat')
    $("#room_name").val(channel);
    $("#room_type").val(channel_type);
    $('#room_data').val('');
    
    $('#modal_new_close').click();
    
    if($(".chat_list#"+channel).length == 0) {
        var divId = 'inbox_chat';
        add_channel(divId, channel, channel_label, channel_image, channel_type, username, channel);
        $(".chat_list#"+channel).addClass('active_chat');
        $("#type_msg").show();
        $("#type_msg_0").hide();


    } else {
        $(".modal_chat_list#"+channel).remove();
    }
    
    socket.emit('join', {room: channel, create_room: 'True', room_type: 'PUBLIC', data: channel_label});
    return false;
   });

  $('form#join').submit(function(event) {
        $('div.modal_chat_list').click(function() {


            var channel = $(this).attr('id');
            var channel_label = $('h5#'+channel+'_name').text();
            var channel_image = $('img#'+channel+'_img').attr('src');
            var channel_type = $('input#'+channel+'_type').attr('value');

            document.getElementById("msgs_top_label").innerHTML=channel_label;
            document.getElementById("msgs_top_img").src = channel_image;
            document.getElementById('btn_leave_room').style.visibility = 'visible';
            document.getElementById('btn_leave_room_value').value= channel;
            document.getElementById('btn_leave_user_to_value').value= channel;

            
    

            $(".msg_history").hide();
            
            if (document.getElementById("msg_history_"+channel) == null){
                var attrId = document.createAttribute("id");
                attrId.value= "msg_history_"+channel;

                var msgHistory = document.createElement("div");
                msgHistory.classList.add("msg_history");

                msgHistory.setAttributeNode(attrId);
                msgBefore =  document.getElementsByClassName("type_msg")[0];
                document.getElementById("msgs").insertBefore(msgHistory, msgBefore);

            } else {
                $(".msg_history#msg_history_"+channel).show();
            }

            $('div.chat_list').not($("#"+channel)).removeClass('active_chat')
            $("#room_name").val(channel);
            $("#room_type").val(channel_type);
            $('#room_data').val('');
            
            $('#modal_join_close').click();
            
            if($(".chat_list#"+channel).length == 0) {
                var divId = 'inbox_chat';
                add_channel(divId, channel, channel_label, channel_image, channel_type, username, channel);
                $(".modal_chat_list#"+channel).remove();
                $(".chat_list#"+channel).addClass('active_chat');
                $("#type_msg").show();
                $("#type_msg_0").hide();


            } else {
                $(".modal_chat_list#"+channel).remove();
            }

            
            socket.emit('join', {room: channel, room_type: channel_type});
            // broadcasting TO ROOM
            socket.emit('my_room_event', {room: channel, data: fn_Title_Case(username)  +' has entered', user_from: 'admin', user_to: channel, room_type: channel_type});

        });


       return false;
  });

  $('form#leave').submit(function(event) {
    
        var channel = $("#btn_leave_room_value").val();
        var user_to = $("#btn_leave_user_to_value").val();

        var channel_label = $("#msgs_top_label").text(); 
        
        var channel_type = $('input#'+channel+'_type').attr('value');

        var channel_image = $('img#'+channel+'_img').attr('src');

        document.getElementById("msgs_top_label").innerHTML='';
        document.getElementById('btn_leave_room').style.visibility = 'hidden';
        document.getElementById('btn_leave_room_value').value= '';
        document.getElementById('btn_leave_user_to_value').value= '';


        $(".msg_history").hide();
        $("#msg_history_0").show();
        $("#type_msg").hide();
        $("#type_msg_0").show();

        var divId = 'modal_inbox_chat';
        add_channel_modal(divId, channel, channel_label, channel_image, channel_type, username, channel);
         $('div.chat_list#'+channel).remove();
 
        socket.emit('leave', {room: channel});
  
        return false;
  });
  
  $('form#send_room').submit(function(event) {
      var room_type='PUBLIC';  
      var channel = $('#room_name').val();
      var user_to = $('#btn_leave_user_to_value').val();
      var data = $('#room_data').val();

      if ($("#room_type").val()=='PRIVATE'){
          room_type='PRIVATE'
      } 
    
      socket.emit('my_room_event', {room: channel, data: data, user_from: username, user_to: user_to, room_type: room_type });
        $('#room_data').val('');


        



      return false;
  });

  $('form#close').submit(function(event) {
      socket.emit('close_room', {room: $('#close_room').val()});
      return false;
  });

  $('form#disconnect').submit(function(event) {
      socket.emit('disconnect_request');
      form.submit()
      return false;
  });

});