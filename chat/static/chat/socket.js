const socket = new WebSocket('ws://127.0.0.1:8000/online');
console.log("nice")
socket.onopen = function(e) {
  socket.send(JSON.stringify({
    message: 'Hello from Js client'
  }));
};

socket.onmessage = function(event) {
  try {
    console.log(event);
  } catch (e) {
    console.log('Error:', e.message);
  }
};