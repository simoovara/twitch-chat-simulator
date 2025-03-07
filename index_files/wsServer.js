const http = require('http');
const WsServer = require('ws');

const server = http.createServer();
const wss = new WsServer.Server({ server });

wss.on('connection', (ws) => {
  console.log('Client connected');
  ws.send('Hello from server!');

  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message.toString());
      console.log('Received message:', data);
      // Broadcast the message to all connected clients
      wss.clients.forEach(client => {
        if (client.readyState === WsServer.OPEN) {
          client.send(JSON.stringify(data));
        }
      });
    } catch (error) {
      console.error('Error parsing JSON:', error);
    }
  });
});

server.listen(8080, () => {
  console.log('Server is listening on port 8080');
});