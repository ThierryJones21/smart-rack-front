import React, { useState, useRef } from 'react';
import Button from '@mui/material/Button';

export function DelayedButton({ firstAction, secondAction }) {
  const [waiting, setWaiting] = useState(false);
  const timeoutRef = useRef(null);

  function handleClick() {
    setWaiting(true);
    timeoutRef.current = setTimeout(() => {
      firstAction();
      timeoutRef.current = setTimeout(() => {
        secondAction();
        setWaiting(false);
      }, 10000);
    }, 10000);
  }

  function handleStop() {
    clearTimeout(timeoutRef.current);
    console.log('Stop action');
    setWaiting(false);
  }

  return (
    <>
      <Button
        variant='contained'
        disabled={waiting}
        onClick={waiting ? handleStop : handleClick}
      >
        {waiting ? 'Waiting...' : 'Start'}
      </Button>
    </>
  );
}
