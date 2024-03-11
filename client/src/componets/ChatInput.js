import { useState } from "react";
import './ChatInput.css'

export function ChatInput({ onSendMessage, sendingMessage }) {
    const [inputText, setInputText] = useState('');
  
    const handleSubmit = (e) => {
      e.preventDefault();
      const trimmedInput = inputText.trim();
      if (trimmedInput) {
        onSendMessage(trimmedInput);
        setInputText('');
      }
    };
  
    return (
      <div class='chat_input'>
        <form onSubmit={handleSubmit} className="chat_form">
          {sendingMessage && <div class= 'loader'></div>}
          <input
            class='chat_input_area'
            type="text"
            value={inputText}
            placeholder="Ask a question..."
            onChange={(e) => setInputText(e.target.value)}
          />
          <div class='chat_input_button'>
            <button type="submit">↥</button>
          </div>
        </form>
      </div>
    );
  }