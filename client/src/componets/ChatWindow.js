import {useRef, useEffect} from "react"
import './ChatWindow.css'

export function ChatWindow({ messages }) {
    const formattedMessages = [];
    const chatWindowRef= useRef(null);
  
    useEffect(() => {
      if (chatWindowRef.current){
        chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
      }
    }, [messages]);
  
    // Iterate through each message
    for (let i = 0; i < messages.length; i++) {
      const currentMessage = messages[i];
  
      if (currentMessage.sender === 'bot') {
        // If the message is from the bot and not "<<Response Finished>>",
        // append its content to the last message's content if available,
        // otherwise push it as a new message
        if (currentMessage.content !== '<<Response Finished>>' && formattedMessages.length > 0 && formattedMessages[formattedMessages.length - 1].sender === 'bot') {
          formattedMessages[formattedMessages.length - 1].content += '' + currentMessage.content;
        } else {
          if (currentMessage.content !== ('<<Response Finished>>')){
            formattedMessages.push({
              id: currentMessage.id,
              content: currentMessage.content,
              sender: currentMessage.sender
            });
          }
        }
        
      } if (currentMessage.sender === 'user') {
        // For user messages, push them individually
        formattedMessages.push({
          id: currentMessage.id,
          content: currentMessage.content,
          sender: currentMessage.sender
        });
      }
    }
  
    return (
    <div className="chat_window">
      <div className="chat_area" ref={chatWindowRef}>
        {formattedMessages.map((message) => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className='bubble'>
            <pre>{message.content}</pre>
            </div>
          </div>
        ))}
      </div>
    </div>
    );
  }
  