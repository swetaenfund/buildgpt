const options = {
    method: 'GET',
    headers: {
      accept: 'application/json',
      authorization: 'Bearer Q2JW7JjrikwnThChjwkCgfm1mtQfnN5p'
    }
  };
  
  let lastMessageId = null;
  
  function fetchMessages() {
    console.log('Fetching messages...');
    fetch('https://gate.whapi.cloud/messages/list/120363317761180470%40g.us?count=100', options)
      .then(response => response.json())
      .then(response => {
        console.log('Parsed response:', response);
        if (response.groups && response.groups.length > 0) {
          const group = response.groups.find(g => g.id === '120363317761180470@g.us');
          if (group && group.last_message) {
            const newMessage = group.last_message;
            if (lastMessageId !== newMessage.id) {
              lastMessageId = newMessage.id;
              console.log('New message:', newMessage);
            } else {
              console.log('No new messages.');
            }
          } else {
            console.log('No messages found.');
          }
        } else {
          console.log('No groups found.');
        }
      })
      .catch(err => {
        console.error('Fetch error:', err);
      });
  }
  
  // Poll the API every 2 seconds
  setInterval(fetchMessages, 2000);
  