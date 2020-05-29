document.addEventListener('DOMContentLoaded', () => {
  console.info(location);

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure buttons
  socket.on('connect', () => {

      // Each button should emit a "submit vote" event
      document.querySelectorAll('button').forEach(button => {
          button.onclick = () => {
              const selection = button.dataset.vote;
              socket.emit('message', {'selection': selection});
          };
      });
  });

  // When a new vote is announced, add to the unordered list
  socket.on('vote totals', data => {
      document.querySelector('#yes').innerHTML = data.yes;
      document.querySelector('#no').innerHTML = data.no;
      document.querySelector('#maybe').innerHTML = data.maybe;
  });
  

  // const socket = io()

  // socket.emit('message', 'Bienvenido')

  channel_id = document.querySelector('#channel_id').value;  
  console.info("channel:"+channel_id);

  socket.on('message', room=channel_id, function(msg) {
    $('#messages').append('<li>' + msg + '</li>')
  })

  $('#send').on('click', function() {
    socket.send($('#myMessage').val());
    $('#myMessage').val('');
  })

  socket.onmessage= function(msg) {
    alert('got reply '+msg);
  };

});


 