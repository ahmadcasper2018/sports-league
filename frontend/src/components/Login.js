import React, { useState } from "react";
import { TextField, Button, Box, Typography } from "@mui/material";
import { useRecoilState } from "recoil";
import { tokenState } from "../atoms/authAtom";
import { useNavigate, Link } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useRecoilState(tokenState);

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setToken(data.access);
        navigate("/home");
        toast.success("Login successful!", { autoClose: 5000 });
      } else {
        toast.error(data.detail || "Login failed", { autoClose: 5000 });
      }
    } catch (error) {
      console.error("Error during login:", error);
      toast.error("An error occurred during login", { autoClose: 5000 });
    }
  };

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height="100vh"
    >
      <Box>
        <Typography variant="h4" align="center" gutterBottom>
          Login
        </Typography>
        <TextField
          label="Username"
          value={username}
          onChange={handleUsernameChange}
          fullWidth
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={handlePasswordChange}
          fullWidth
        />
        <Box display="flex" justifyContent="space-between" mt={2}>
          <Button variant="contained" color="primary" onClick={handleLogin}>
            Login
          </Button>
          <Link to="/register">
            <Button variant="outlined" color="primary">
              Register
            </Button>
          </Link>
        </Box>
      </Box>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={true}
      />
    </Box>
  );
}