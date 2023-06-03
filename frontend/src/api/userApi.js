import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000"; // Replace with your actual API base URL

export const createUser = (userData) => {
  return axios.post(`${BASE_URL}/users`, userData);
};

export const deleteUser = (userId) => {
  return axios.delete(`${BASE_URL}/users/${userId}`);
};

export const editUser = (userId, userData) => {
  return axios.put(`${BASE_URL}/users/${userId}`, userData);
};

export const loginUser = (credentials) => {
  return axios.post(`${BASE_URL}/login`, credentials);
};
