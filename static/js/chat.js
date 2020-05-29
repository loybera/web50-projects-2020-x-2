$(document).ready(function() {

    // Use a "/test" namespace.
  // An application can open a connection on multiple namespaces, and
  // Socket.IO will multiplex all those connections on a single
  // physical channel. If you don't care about multiple channels, you
  // can set the namespace to an empty string.
  namespace = '/project2';

  // Connect to the Socket.IO server.
  // The connection URL has the following format, relative to the current page:
  //     http[s]://<domain>:<port>[/<namespace>]
  var socket = io(namespace);

  // Initialize user channels join it at load
  //   window.onload = function() {
    
    list = document.getElementsByClassName("chat_list")
    
    for (var i = 0; i < list.length; i++){
    
        channel = list[i].getAttribute('id');
        console.log("emit join room: "+channel);
        socket.emit('join', {room:channel});
        
    }
    
    if (list.length>0){
        $(".msg_history").hide();
        $(".msg_history#msg_history_0").show();
        $(".type_msg").hide();
    }
    else
    {
        $(".type_msg").hide();
    }

    // };

    document.getElementById('btn_leave_room').style.visibility = 'hidden';
    
 
    $('div.inbox_chat').on("click", "div.chat_list", function(){
        var channel = $(this).attr('id');
        var channel_label = $('h5#'+channel+'_name').text() 
        var channel_image = $('img#'+channel+'_img').attr('src');

        // document.getElementById("msgs_top_label_room").innerHTML=channel;
        document.getElementById("msgs_top_label").innerHTML=channel_label;
        document.getElementById("msgs_top_img").src = channel_image;

        document.getElementById('btn_leave_room').style.visibility = 'visible';
        document.getElementById('btn_leave_room_value').value= channel;


        $(".msg_history").hide();
        $(".msg_history#msg_history_"+channel).show();
        $(".type_msg").show();
        $('div.chat_list').not(this).removeClass('active_chat')
        $(this).addClass('active_chat');
        $("#room_name").val(channel);

    });

  
    $('div.msg_history').on("click", "a.message_id", function(){
        var msg_id = $(this).attr('id');
        var channel_label = $('h5#'+channel+'_name').text() 
        var channel_image = $('img#'+channel+'_img').attr('src');

        // document.getElementById("msgs_top_label_room").innerHTML=channel;
        document.getElementById("msgs_top_label").innerHTML=channel_label;
        document.getElementById("msgs_top_img").src = channel_image;

        document.getElementById('btn_leave_room').style.visibility = 'visible';
        document.getElementById('btn_leave_room_value').value= channel;


        $(".msg_history").hide();
        $(".msg_history#msg_history_"+channel).show();
        $(".type_msg").show();
        $('div.chat_list').not(this).removeClass('active_chat')
        $(this).addClass('active_chat');
        $("#room_name").val(channel);

    });


    // Add a new post with given contents to DOM.
    const broadcast_msg_template = Handlebars.compile(document.querySelector('#broadcast_msg_template').innerHTML);
    function add_broadcast_msg(channel, post, post_info) {

        // Create new post.
        const msg = broadcast_msg_template({'post': post, 'post_info': post_info});

        // Add post to DOM.
        var divId = 'msg_history_'+channel;
        document.querySelector('#'+divId).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }
    // Add a new post with given contents to DOM.
    const in_msg_template = Handlebars.compile(document.querySelector('#in_msg_template').innerHTML);
    function add_in_msg(channel, post, post_info, post_image, post_id) {

        // Create new post.
        const msg = in_msg_template({'post': post, 'post_info': post_info, 'post_image': post_image, 'post_id': post_id});

        // Add post to DOM.
        var divId = 'msg_history_'+channel;
        document.querySelector('#'+divId).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    const out_msg_template = Handlebars.compile(document.querySelector('#out_msg_template').innerHTML);
    function add_out_msg(channel, post, post_info, post_id) {

        // Create new post.
        const msg = out_msg_template({'post': post, 'post_info': post_info, 'post_id': post_id});

        // Add post to DOM.
        var divId = 'msg_history_'+channel;
        document.querySelector('#'+divId).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }
    const join_chn_template = Handlebars.compile(document.querySelector('#join_chn_template').innerHTML);
    function add_channel(parentElement, channel, channel_label, channel_image) {

        // Create new post.
        const msg = join_chn_template({'channel': channel, 'channel_label': channel_label, 'channel_image': channel_image});

        // Add post to DOM.
        document.querySelector('#'+parentElement).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(parentElement);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    const modal_join_chn_template = Handlebars.compile(document.querySelector('#modal_join_chn_template').innerHTML);
    function add_channel_modal(parentElement, channel, channel_label, channel_image) {

        // Create new post.
        const msg = modal_join_chn_template({'channel': channel, 'channel_label': channel_label, 'channel_image': channel_image});

        // Add post to DOM.
        // document.querySelector('#'+parentElement).innerHTML += msg;
        document.getElementById(parentElement).innerHTML +=msg;

    }
  
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
    var channel = document.getElementById("room_name").value;
    if (channel) {

        if (msg.user.toUpperCase()==$('#nickname').val().toUpperCase()){
            add_out_msg(channel=channel, post=msg.data, post_info=msg.user.toUpperCase() + ' | '+ msg.time, post_id=msg.id );
        } else {
            if (msg.user.toUpperCase()=='ADMIN'){
                    add_broadcast_msg(channel=channel, post=msg.data, post_info=msg.time);
            } else {    
                add_in_msg(channel=channel, post=msg.data,  post_info=msg.user_from.toUpperCase() + ' | '+ msg.time, post_image=msg.user_from_img, post_id=msg.id);
            }
        }
        // $('#msgs_'+channel).append('<li>' + $('<div/>').text(   msg .data ).html());
    }else {
        $('#log').append('<li>' + $('<div/>').text(   msg .data ).html());
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

      if (msg.messages !== undefined){
        for (var i = 0; i < msg.messages.length; i++){
            json_msg = JSON.parse(msg.messages[i])
            console.log(json_msg);

            // add_in_msg(msg.messages[i], 'User' + ' | '+ 'Fecha Hora');
            if (json_msg.user.toUpperCase()==$('#nickname').val().toUpperCase()){
                add_out_msg(channel=msg.room, post=json_msg.post, post_info=json_msg.user_from.toUpperCase() + ' | '+ json_msg.time, post_id=json_msg.id);
            } else {
                if (json_msg.user.toUpperCase()=='ADMIN'){
                    add_broadcast_msg(channel=msg.room, post=json_msg.post, post_info=json_msg.time);
                } else { 
                    add_in_msg(channel=msg.room, post=json_msg.post, post_info=json_msg.user_from.toUpperCase() + ' | '+ json_msg.time, post_image= json_msg.user_from_img, post_id=json_msg.id);
                }
            }
      } 
    }
    if (cb)
        cb();
  });

 
// Interval function that tests message latency by sending a "ping"
  // message. The server then responds with a "pong" message and the
  // round trip time is measured.
  var ping_pong_times = [];
  var start_time;
//   window.setInterval(function() {
//       start_time = (new Date).getTime();
//       socket.emit('my_ping');
//   }, 1000);

  // Handler for the "pong" message. When the pong is received, the
  // time from the ping is stored, and the average of the last 30
  // samples is average and displayed.
  socket.on('my_pong', function() {
      var latency = (new Date).getTime() - start_time;
      ping_pong_times.push(latency);
      ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
      var sum = 0;
      for (var i = 0; i < ping_pong_times.length; i++)
          sum += ping_pong_times[i];
      $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
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

//   // create private channel for user to user message
//   $('form#create_user').submit(function(event) {

//     var channel_label = $('#create_user').val();
//     var channel_image = '/static/img/user/newchannel.png';
//     var channel_image = $('img#message_'+channel+'_img').attr('src');

//     // make channel id
//     channel = channel_label.replace(/[^A-Z0-9]+/ig, "").toLowerCase();

//     // document.getElementById("msgs_top_label_room").innerHTML = channel;
//     document.getElementById("msgs_top_label").innerHTML = channel_label;
//     document.getElementById("msgs_top_img").src = channel_image;

//     document.getElementById('btn_leave_room').style.visibility = 'visible';
//     document.getElementById('btn_leave_room_value').value= channel;

//     $(".msg_history").hide();
//     var attrId = document.createAttribute("id");
//     attrId.value= "msg_history_"+channel;

//     var msgHistory = document.createElement("div");
//     msgHistory.classList.add("msg_history");

//     msgHistory.setAttributeNode(attrId);
//     msgBefore =  document.getElementsByClassName("type_msg")[0];
//     document.getElementById("msgs").insertBefore(msgHistory, msgBefore);

//     $('div.chat_list').not($("#"+channel)).removeClass('active_chat')
//     $("#room_name").val(channel);
//     $('#room_data').val('');
    
//     $('#modal_new_close').click();
    
//     if($(".chat_list#"+channel).length == 0) {
//         var divId = 'inbox_chat';
//         add_channel(divId, channel, channel_label, channel_image);
//         $(".chat_list#"+channel).addClass('active_chat');
//         $(".type_msg").show();


//     } else {
//         $(".modal_chat_list#"+channel).remove();
//     }
    
//     socket.emit('join', {room: channel, create_room: 'True', data: channel_label});
//     return false;
//    });

  // Create public channel 
  $('form#create').submit(function(event) {

    var channel_label = $('#create_room').val();
    var channel_image = '/static/img/user/newchannel.png';
    
    // make channel id
    channel = channel_label.replace(/[^A-Z0-9]+/ig, "").toLowerCase();

    // document.getElementById("msgs_top_label_room").innerHTML = channel;
    document.getElementById("msgs_top_label").innerHTML = channel_label;
    document.getElementById("msgs_top_img").src = channel_image;

    document.getElementById('btn_leave_room').style.visibility = 'visible';
    document.getElementById('btn_leave_room_value').value= channel;

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
    $('#room_data').val('');
    
    $('#modal_new_close').click();
    
    if($(".chat_list#"+channel).length == 0) {
        var divId = 'inbox_chat';
        add_channel(divId, channel, channel_label, channel_image);
        $(".chat_list#"+channel).addClass('active_chat');
        $(".type_msg").show();


    } else {
        $(".modal_chat_list#"+channel).remove();
    }
    
    socket.emit('join', {room: channel, create_room: 'True', data: channel_label});
    return false;
   });

  $('form#join').submit(function(event) {
        $('div.modal_chat_list').click(function() {

            var nickname = document.getElementById("nickname").value;

            var channel = $(this).attr('id');
            var channel_label = $('h5#'+channel+'_name').text();
            var channel_image = $('img#'+channel+'_img').attr('src');

            document.getElementById("msgs_top_label").innerHTML=channel_label;
            document.getElementById("msgs_top_img").src = channel_image;
            document.getElementById('btn_leave_room').style.visibility = 'visible';
            document.getElementById('btn_leave_room_value').value= channel;

            
    

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
            $('#room_data').val('');
            
            $('#modal_join_close').click();
            
            if($(".chat_list#"+channel).length == 0) {
                var divId = 'inbox_chat';
                add_channel(divId, channel, channel_label, channel_image);
                $(".modal_chat_list#"+channel).remove();
                $(".chat_list#"+channel).addClass('active_chat');
                $(".type_msg").show();


            } else {
                $(".modal_chat_list#"+channel).remove();
            }

            
            socket.emit('join', {room: channel});
            // broadcasting 
            socket.emit('my_room_event', {room: channel, data: nickname.toUpperCase() +' has entered', user: 'Admin'});

        });


    // socket.emit('join', {room: $('#join_room').val()});
      return false;
  });
  $('form#leave').submit(function(event) {
    
        var channel = $("#btn_leave_room_value").val();
        var channel_label = $("#msgs_top_label").text() 

        var channel_image = $('img#'+channel+'_img').attr('src');

        // document.getElementById("msgs_top_label_room").innerHTML='';
        document.getElementById("msgs_top_label").innerHTML='';
        document.getElementById('btn_leave_room').style.visibility = 'hidden';
        document.getElementById('btn_leave_room_value').value= '';


        $(".msg_history").hide();
        $("#msg_history_0").show();
        $(".type_msg").hide();

        var divId = 'modal_inbox_chat';
        add_channel_modal(divId, channel, channel_label, channel_image);
         $('div.chat_list#'+channel).remove();
 
        socket.emit('leave', {room: channel});
  
        return false;
  });
  
  $('form#send_room').submit(function(event) {
      socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val(), user:$('#nickname').val()});
      $('#room_data').val('');

      return false;
  });
  $('form#close').submit(function(event) {
      socket.emit('close_room', {room: $('#close_room').val()});
      return false;
  });
  $('form#disconnect').submit(function(event) {
      socket.emit('disconnect_request');
      return false;
  });

});