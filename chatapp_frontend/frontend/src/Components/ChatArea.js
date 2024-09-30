import React, { useState, useEffect } from 'react';

const ChatArea = ({ token, chatId }) => {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token || !chatId) {
      setError('Missing token or chatId');
      return;
    }

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${chatId}/?token=${token}`);

    ws.onopen = () => {
      console.log('WebSocket connection opened');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    ws.onerror = (event) => {
      console.error('WebSocket error:', event);
      setError('WebSocket connection failed');
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      ws.close();
    };
  }, [token, chatId]);

  return (
    <div>
      {error && <div>{error}</div>}
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message.message}</li>
        ))}
      </ul>
    </div>
  );
};

export default ChatArea;
