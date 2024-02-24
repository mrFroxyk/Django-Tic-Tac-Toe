// const socket = new WebSocket('ws:/192.168.3.2:8000/online');
// socket.onopen = function (e) {
//     socket.send(JSON.stringify({
//         type: 'handshake',
//         message: 'Hello from Js client'
//     }));
// };
//
// socket.onmessage = function (event) {
//     try {
//         const data = JSON.parse(event.data)
//         if (data.type === 'websocket.message'){
//             console.log('Message:', data.message);
//         }
//     } catch (e) {
//         console.log('Error:', e.message);
//     }
// };
