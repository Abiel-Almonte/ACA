import { useEffect, useState, useRef } from "react"
import './Chat.css'
import { ChatWindow } from "./ChatWindow";
import { ChatInput } from "./ChatInput";
import {ChatSidebar } from "./ChatSidebar";

const SERVER_URL = 'ws://localhost:8283';

function useWebSocket(url) {
    const [websocket, setWebsocket] = useState(null);
  
    useEffect(() => {
      const ws = new WebSocket(url);
      setWebsocket(ws);
  
      return () => {
        if (ws) {
          ws.close();
        }
      };
    }, [url]);
  
    return websocket;
  }

  export function Chat({ username }) {
    const [messages, setMessages] = useState([]);
    const [sendingMessage, setSendingMessage]= useState(false);
    const websocket = useWebSocket(`${SERVER_URL}?username=${username}`);
    const websocketRef = useRef(null);
    
  
    useEffect(() => {
      websocketRef.current = websocket;
  
      if (websocket) {
        let newMessage
        websocket.onmessage = (event) => {

          if(typeof event.data === "string" ){
            newMessage = {
              username:username,
              id: Date.now(),
              content: event.data,
              sender: 'bot',
            };
          }
          else{
            newMessage = {
              username:username,
              id: Date.now(),
              content: event.data,
              sender: 'server',
            };
          }
          setMessages((prevMessages) => [...prevMessages, newMessage]);
          setSendingMessage(false);
        };
      }
  
      return () => {
        if (websocketRef.current) {
          websocketRef.current.close();
        }
      };
    }, [websocket, username]);
  
    const sendMessage = (message) => {
      if (websocket && message.trim() !== '') {
        const newMessage = { 
          username: username,
          id: Date.now(),
          content: message,
          sender: 'user'
        };
        setMessages((prevMessages) => [...prevMessages, newMessage]);
        setSendingMessage(true);
        websocket.send(message);
      }
    };
  
    return (
      <div id="chat-grid">
        
        <div id="chat-window">
          <ChatWindow messages={messages} />
        </div>
        <div id='chat-input'>
          <ChatInput onSendMessage={sendMessage} sendingMessage={sendingMessage} />
        </div>
        <div id= 'chat-sidebar'>
          <ChatSidebar messages={messages} username={username} />
        </div>
      </div>
    );
  }