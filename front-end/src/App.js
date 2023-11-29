import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RegisterLogin from "./components/RegisterLogin";
import Game from "./components/Game/Game";
import Congratulations from "./components/Congratulations";
import WelcomePage from "./components/WelcomePage";
import Leaderboard from "./components/LeaderBoard";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<RegisterLogin />} />
        <Route path="/game" element={<Game />} />
        <Route path="/" element={<WelcomePage />} />
        <Route path="/congratulations" element={<Congratulations />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </Router>
  );
}

export default App;
