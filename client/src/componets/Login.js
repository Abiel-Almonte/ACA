import { useState } from "react"
import './Login.css'

export function Login({ onLogin }) {
  const [username, setUsername] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedUsername = username.trim();
    if (trimmedUsername) {
      onLogin(trimmedUsername);
    }
  };

  return (
    <div class='login_page'> 
      <div class='login'>
        <form onSubmit={handleSubmit}>
          <h1>Login</h1>
          <div class="login_box">
            <input
              name='input_text' required id= 'input_text' value={username} 
              onChange={(e) =>setUsername(e.target.value)}
            />
            <label>Name</label>
          </div>
            <div className='login_button'>
              <button id="login_button">Submit</button>
            </div>
        </form>
      </div>
    </div>
  );
}