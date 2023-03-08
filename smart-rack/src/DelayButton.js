import React, { useState, useEffect } from "react";

function DelayButton(props) {
  const [buttonText, setButtonText] = useState("Begin Set");
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    if (countdown > 0) {
      setTimeout(() => setCountdown(countdown - 1), 1000);
    } else {
      setButtonText("Set in Progress");
      props.onBeginSet();
      setTimeout(() => {
        setButtonText("Begin Set");
        props.onSetComplete();
        setCountdown(5);
      }, 10000);
    }
  }, [countdown, props]);

  function handleClick() {
    if (buttonText === "Begin Set") {
      setButtonText("Waiting 5s...");
    }
  }

  return <button onClick={handleClick}>{buttonText}</button>;
}

export default DelayButton;
