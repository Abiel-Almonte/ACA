import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import { Home } from './componets/Home'
import { Login } from './componets/Login'
import { Chat } from './componets/Chat'

// App component managing the login and chat interface
function App() {
  const [username, setUsername] = useState('');

  const handleLogin = (username) => setUsername(username);
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element= {!username ? <Login onLogin={handleLogin}/> : <Chat username={username} />} />
      </Routes>
    </Router>
  );
}

export default App;
