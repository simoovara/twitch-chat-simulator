const ws = new WebSocket("ws://localhost:8080");

ws.onopen = () => {
    console.log('Connected to the server');
};

ws.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);

        $("#textfield").val(data.messageContent);
        chat();
    } catch (error) {
        console.error('Error parsing JSON:', error);
    }
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};