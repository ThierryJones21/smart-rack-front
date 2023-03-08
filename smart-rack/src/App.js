import React from "react";
import Webcam from "react-webcam";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Webcam mirrored={true} />
    </div>
  );
}

export default App;