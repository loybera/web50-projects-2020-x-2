
$(document).ready(function() {
    document.getElementById('btn_leave_room').style.visibility = 'hidden';
    
 
    $('div.inbox_chat').on("click", "div.chat_list", function(){
        var channel = $(this).attr('id');
        var label = $('h5#'+channel+'_name').text() 

        document.getElementById("msgs_top_label_room").innerHTML=channel;
        document.getElementById("msgs_top_label").innerHTML=label;
        document.getElementById('btn_leave_room').style.visibility = 'visible';


        $(".msg_history").hide();
        $(".msg_history#msg_history_"+channel).show();
        $('div.chat_list').not(this).removeClass('active_chat')
        $(this).addClass('active_chat');
        $("#room_name").val(channel);

    });
  
    // Add a new post with given contents to DOM.
    const in_msg_template = Handlebars.compile(document.querySelector('#in_msg_template').innerHTML);
    function add_in_msg(channel, post, audit_data) {

        // Create new post.
        const msg = in_msg_template({'contents1': post, 'contents2': audit_data});

        // Add post to DOM.
        var divId = 'msg_history_'+channel;
        document.querySelector('#'+divId).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    const out_msg_template = Handlebars.compile(document.querySelector('#out_msg_template').innerHTML);
    function add_out_msg(channel, post, audit_data) {

        // Create new post.
        const msg = out_msg_template({'contents1': post, 'contents2': audit_data});

        // Add post to DOM.
        var divId = 'msg_history_'+channel;
        document.querySelector('#'+divId).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }
    const join_chn_template = Handlebars.compile(document.querySelector('#join_chn_template').innerHTML);
    function add_channel(channel, label) {

        // Create new post.
        const msg = join_chn_template({'contents1': channel, 'contents2': label});

        // Add post to DOM.
        var divId = 'inbox_chat';
        document.querySelector('#'+divId).innerHTML += msg;
        // scroll down to show new DOM
        var objDiv = document.getElementById(divId);
        objDiv.scrollTop = objDiv.scrollHeight;
    }

   
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

  window.onload = function() {
   
    list = document.getElementsByClassName("chat_list")
    
    for (var i = 0; i < list.length; i++){
    
        channel = list[i].getAttribute('id');
        console.log("emit join room: "+channel);
        socket.emit('join', {room:channel});
        
      }
     
    if (list.length>0){
        $(".msg_history").hide();
        $(".msg_history#msg_history_"+list[0].getAttribute('id')).show();
    }

};
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
    //   $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    var channel = document.getElementById("room_name").value;
    if (channel) {
        if (msg.user.toUpperCase()==$('#nickname').val().toUpperCase()){
            add_out_msg(channel=channel, post=msg.data, audit_data=msg.user.toUpperCase() + ' | '+ msg.time );
        } else {    
            add_in_msg(channel=channel, post=msg.data,  audit_data=msg.user.toUpperCase() + ' | '+ msg.time);
        }
        // $('#msgs_'+channel).append('<li>' + $('<div/>').text(   msg .data ).html());
    }else {$('#log').append('<li>' + $('<div/>').text(   msg .data ).html());}

      if (cb)
          cb();
  });

  socket.on('my_response', function(msg, cb) {
      $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
      if (msg.messages !== undefined){
        for (var i = 0; i < msg.messages.length; i++){
            json_msg = JSON.parse(msg.messages[i])
            console.log(json_msg);

            // add_in_msg(msg.messages[i], 'User' + ' | '+ 'Fecha Hora');
            if (json_msg.user.toUpperCase()==$('#nickname').val().toUpperCase()){
                add_out_msg(channel=msg.room, post=json_msg.post, audit_data=json_msg.user.toUpperCase() + ' | '+ json_msg.time );
            } else {    
                add_in_msg(channel=msg.room, post=json_msg.post, audit_data=json_msg.user.toUpperCase() + ' | '+ json_msg.time);
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
  $('form#create').submit(function(event) {
    socket.emit('join', {room: $('#create_room').val()});
    return false;
   });

  $('form#join').submit(function(event) {
        $('div.modal_chat_list').click(function() {
            var channel = $(this).attr('id');
            var label = $('h5#'+channel+'_name').text() 

            document.getElementById("msgs_top_label_room").innerHTML=channel;
            document.getElementById("msgs_top_label").innerHTML=label;
            document.getElementById('btn_leave_room').style.visibility = 'visible';
    

            $(".msg_history").hide();
            var msgHistory = document.createElement("div").addClass("msg_history");
            msgHistory.id = "msg_history_"+channel;
            document.getElementById("msgs").appendChild(msgHistory);
            
            $(".msg_history#msg_history_"+channel).show();
            $('div.chat_list').not($("#"+channel)).removeClass('active_chat')
            $("#room_name").val(channel);
            $('#myChannelModal .close').click();
            
            if($(".chat_list#"+channel).length == 0) {
                add_channel(channel, label);
                $(".modal_chat_list#"+channel).remove();
                $(".chat_list#"+channel).addClass('active_chat');

            } else {
                $(".modal_chat_list#"+channel).remove();
            }


            
            socket.emit('join', {room: channel});
        });


    // socket.emit('join', {room: $('#join_room').val()});
      return false;
  });
  $('form#leave').submit(function(event) {
      socket.emit('leave', {room: $('#msgs_top_label_room').val()});
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