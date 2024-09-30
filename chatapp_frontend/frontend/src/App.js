import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Register from './Components/Register';
import Login from './Components/Login';
import ChatArea from './Components/ChatArea';
import SendMessage from './Components/SendMessage';

function App() {
  const token = "your_jwt_token"; // Replace with actual token
  const chatId = "2"; // Replace with actual chat ID

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/login' element={<Login/>}></Route>
        <Route path='/register' element={<Register/>}></Route>
        <Route path='/chat' element={<><ChatArea token={token} chatId={chatId} /><SendMessage/></>}></Route>
        <Route path="/user/:id" element={<ChatArea token={token} chatId={chatId} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
