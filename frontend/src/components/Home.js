import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import RankTable from "./RankTable";
import ScoreTable from "./ScoreTable";
import { useRecoilValue } from 'recoil';
import { loggedUserNameState } from "../atoms/authAtom";

const Home = () => {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  const [showRedirectMessage, setShowRedirectMessage] = useState(false);
  const username = useRecoilValue(loggedUserNameState)

  useEffect(() => {
    // Check if the token is empty
    if (!token || token === '') {
      // Display the redirect message
      setShowRedirectMessage(true);

      // Redirect to the login page after 5 seconds
      const redirectTimer = setTimeout(() => {
        navigate('/login'); // Replace '/login' with the actual path to your login page
      }, 3000);

      // Cleanup the timer when the component unmounts or when the token becomes available
      return () => clearTimeout(redirectTimer);
    }
  }, [token, navigate]);

  const handleLogout = () => {
    // Clear the token from local storage
    localStorage.removeItem("token");

    // Redirect to the login page
    navigate('/login'); // Replace '/login' with the actual path to your login page
  };

  // Render the component contents
  return (
    <>

      {showRedirectMessage ? (
        <div>You are not logged in. Redirecting to the login page...</div>
      ) : (
        <>
           <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Welcome {username}
          </Typography>
          <Button color="inherit" onClick={handleLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
          <ScoreTable />
          <RankTable />
        </>
      )}
    </>
  );
};

export default Home;
