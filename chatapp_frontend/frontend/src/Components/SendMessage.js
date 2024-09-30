import React, { useState } from 'react';
import axios from 'axios';

const SendMessage = () => {
  const [message, setMessage] = useState('');

  const handleSendMessage = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/send_message/', {
        message,
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message"
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default SendMessage;
