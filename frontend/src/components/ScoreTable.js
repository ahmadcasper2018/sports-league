import React, { useEffect, useState } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import IconButton from "@mui/material/IconButton";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";
import { TextField, Button } from "@mui/material";
import FileUpload from "./FileUpload";
import {useRecoilState} from "recoil";
import {is_pushed as isPushedAtom} from "../atoms/authAtom";
import { useNavigate } from 'react-router-dom';
import { sessionState as xState } from '../atoms/authAtom';

export default function ScoreTable() {
  const [data, setData] = useState([]);
  const [editingRow, setEditingRow] = useState(null);
  const [isPushed, setIsPushed] = useRecoilState(isPushedAtom);
  const [sessionState, setSessionState] = useRecoilState(xState);
  const navigate = useNavigate();
  const token = localStorage.getItem("token")
const checkStatus = (response) => {
    if (response.status === 401) {
        localStorage.removeItem("token");
        setSessionState(false);
        navigate('/login');

      }
    else{
      return response;
    }
}
  const [editFormData, setEditFormData] = useState({
    team_one: "",
    score_one: "",
    team_two: "",
    score_two: "",
  });
  const [addingRow, setAddingRow] = useState(false);
  const [addFormData, setAddFormData] = useState({
    team_one: "",
    score_one: "",
    team_two: "",
    score_two: "",
  });

  useEffect(() => {
    // Fetch data from the API
    fetch(`${process.env.REACT_APP_API_BASE_URL}/game/`,{
      method: "GET",
       headers: {
          Authorization: `Bearer ${token}`,
        },
    })
      .then((response) => checkStatus(response))
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log(error));
  }, []);

  const fetchData = () => {
    fetch(`${process.env.REACT_APP_API_BASE_URL}/game/`,{
      method: "GET",
      headers: {
          Authorization: `Bearer ${token}`,
        },
    })
         .then((response) => checkStatus(response))
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log(error));
  };

  const handleDelete = (id) => {
    fetch(`${process.env.REACT_APP_API_BASE_URL}/game/${id}/`, {
      method: "DELETE",
      headers: {
          Authorization: `Bearer ${token}`,
        },
    })
         .then((response) => checkStatus(response))
      .then(() => {
        const updatedData = data.filter((row) => row.id !== id);
        setData(updatedData);
        setIsPushed(true);
      })
      .catch((error) => console.log(error));
  };

  const handleEdit = (row) => {
    setEditingRow(row.id);
    setEditFormData({
      team_one: row.team_one,
      score_one: row.score_one,
      team_two: row.team_two,
      score_two: row.score_two,
    });
  };

  const handleEditFormChange = (e) => {
    setEditFormData({
      ...editFormData,
      [e.target.name]: e.target.value,
    });
  };

const handleFileSelect = (formData) => {
  fetch(`${process.env.REACT_APP_API_BASE_URL}/game/upload-games-csv/`, {
    method: "POST",
    body: formData,
    headers: {
          Authorization: `Bearer ${token}`,
        },
  })
       .then((response) => checkStatus(response))
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      console.log('Upload game');
      setIsPushed(true);
    })
    .catch((error) => console.log(error));
};


  const handleEditFormSubmit = (e, id) => {
    e.preventDefault();

    fetch(`${process.env.REACT_APP_API_BASE_URL}/game/${id}/`, {
      method: "PUT",
       Authorization: `Bearer ${token}`,
      headers: {
        "Content-Type": "application/json",
         Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(editFormData),
    })
         .then((response) => checkStatus(response))
      .then((response) => response.json())
      .then(() => {
        fetchData();
        setEditingRow(null);
        setEditFormData({
          team_one: "",
          score_one: "",
          team_two: "",
          score_two: "",
        });
        setIsPushed(true);
      })
      .catch((error) => console.log(error));
  };

  const handleAdd = () => {
    setAddingRow(true);
  };

  const handleAddFormChange = (e) => {
    setAddFormData({
      ...addFormData,
      [e.target.name]: e.target.value,
    });
  };

  const handleAddFormSubmit = (e) => {
    e.preventDefault();

    fetch(`${process.env.REACT_APP_API_BASE_URL}/game/`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
         Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(addFormData),
    })
         .then((response) => checkStatus(response))
      .then((response) => response.json())
      .then(() => {
        fetchData();
        setAddingRow(false);
        setAddFormData({
          team_one: "",
          score_one: "",
          team_two: "",
          score_two: "",
        });
        setIsPushed(true);
      })
      .catch((error) => console.log(error));
  };

  const isEditing = (row) => {
    return editingRow === row.id;
  };

  const isAdding = () => {
    return addingRow;
  };

  return (
    <>
      <div style={{ maxHeight: "400px", overflowY: "auto" }}>
        <TableContainer component={Paper} sx={{ margin: "0 0%" }}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Team One</TableCell>
                <TableCell align="right">Score One</TableCell>
                <TableCell>Team Two</TableCell>
                <TableCell align="right">Score Two</TableCell>
                <TableCell align="center">
                  {isAdding() ? (
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={handleAddFormSubmit}
                    >
                      Save
                    </Button>
                  ) : (
                    <IconButton color="primary" onClick={handleAdd}>
                      <AddIcon />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow key={row.id}>
                  <TableCell>
                    {isEditing(row) ? (
                      <TextField
                        name="team_one"
                        value={editFormData.team_one}
                        onChange={handleEditFormChange}
                      />
                    ) : (
                      row.team_one
                    )}
                  </TableCell>
                  <TableCell align="right">
                    {isEditing(row) ? (
                      <TextField
                        name="score_one"
                        value={editFormData.score_one}
                        onChange={handleEditFormChange}
                      />
                    ) : (
                      row.score_one
                    )}
                  </TableCell>
                  <TableCell>
                    {isEditing(row) ? (
                      <TextField
                        name="team_two"
                        value={editFormData.team_two}
                        onChange={handleEditFormChange}
                      />
                    ) : (
                      row.team_two
                    )}
                  </TableCell>
                  <TableCell align="right">
                    {isEditing(row) ? (
                      <TextField
                        name="score_two"
                        value={editFormData.score_two}
                        onChange={handleEditFormChange}
                      />
                    ) : (
                      row.score_two
                    )}
                  </TableCell>
                  <TableCell>
                    {isEditing(row) ? (
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={(e) => handleEditFormSubmit(e, row.id)}
                      >
                        Save
                      </Button>
                    ) : (
                      <IconButton
                        color="primary"
                        onClick={() => handleEdit(row)}
                      >
                        <EditIcon />
                      </IconButton>
                    )}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      color="secondary"
                      onClick={() => handleDelete(row.id)}
                    >
                      <DeleteOutlineIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
              {isAdding() && (
                <TableRow>
                  <TableCell>
                    <TextField
                      name="team_one"
                      value={addFormData.team_one}
                      onChange={handleAddFormChange}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <TextField
                      name="score_one"
                      value={addFormData.score_one}
                      onChange={handleAddFormChange}
                    />
                  </TableCell>
                  <TableCell>
                    <TextField
                      name="team_two"
                      value={addFormData.team_two}
                      onChange={handleAddFormChange}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <TextField
                      name="score_two"
                      value={addFormData.score_two}
                      onChange={handleAddFormChange}
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={handleAddFormSubmit}
                    >
                      Save
                    </Button>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </div>

     <div style={{ paddingTop: '5%', paddingBottom: '5%' }}>
        <FileUpload onFileSelect={handleFileSelect} />
      </div>
    </>
  );
}
