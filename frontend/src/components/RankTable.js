import React, { useState, useEffect } from "react";
import { useRecoilState } from "recoil";
import { useNavigate } from 'react-router-dom';
import { is_pushed as isPushedAtom } from '../atoms/authAtom';
import { sessionState as xState } from '../atoms/authAtom';

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";




export default function RankTable() {
  const [data, setData] = useState([]);
  const navigate = useNavigate();
  const [scoreStrategies, setScoreStrategies] = useState([]);
  const [rankStrategies, setRankStrategies] = useState([]);
  const [selectedScoreStrategy, setSelectedScoreStrategy] = useState("");
  const [selectedRankStrategy, setSelectedRankStrategy] = useState("");
  const [isPushed, setIsPushed] = useRecoilState(isPushedAtom);
  const [xstate, setSessionState] = useRecoilState(xState);

  const token = localStorage.getItem("token")
  const checkStatus = (response) => {
    if (response.status === 401) {
        localStorage.removeItem("token");
        setSessionState(false);
        navigate('/login');

      }
  }


  useEffect(() => {
    const fetchGameRankData = async () => {
      try {
        // Fetch rank data
        const rankResponse = await fetch(`${process.env.REACT_APP_API_BASE_URL}/game/rank/`,{ headers: {
          Authorization: `Bearer ${token}`,
        }});
        checkStatus(rankResponse);
        const rankData = await rankResponse.json();
        setData(rankData);

        // Fetch score strategies
        const scoreStrategiesResponse = await fetch(
          `${process.env.REACT_APP_API_BASE_URL}/game/score-strategies/`,{ headers: {
          Authorization: `Bearer ${token}`,
        }}
        );

        checkStatus(scoreStrategiesResponse);
        const scoreStrategiesData = await scoreStrategiesResponse.json();
        setScoreStrategies(
          scoreStrategiesData.strategies.map((strategy) => strategy)
        );

        // Fetch rank strategies
        const rankStrategiesResponse = await fetch(
          `${process.env.REACT_APP_API_BASE_URL}/game/rank-strategies/`,{ headers: {
          Authorization: `Bearer ${token}`,
        }}
        );
        checkStatus(rankStrategiesResponse);
        const rankStrategiesData = await rankStrategiesResponse.json();
        setRankStrategies(
          rankStrategiesData.strategies.map((strategy) => strategy)
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchGameRankData();
  }, [isPushed]); // Trigger the effect when isPushed changes

  useEffect(() => {
    const fetchRankTableData = async () => {
      try {
        const url = `${process.env.REACT_APP_API_BASE_URL}/game/rank/?score_strategy=${selectedScoreStrategy}&rank_strategy=${selectedRankStrategy}`;
        const response = await fetch(url,{ headers: {
          Authorization: `Bearer ${token}`,
        }});
        checkStatus(response);
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("Error fetching rank table data:", error);
      }
    };

    fetchRankTableData();
  }, [selectedScoreStrategy]);





  useEffect(() => {
    const fetchRankTableDataTwo = async () => {
      try {
        const url = `${process.env.REACT_APP_API_BASE_URL}/game/rank/?rank_strategy=${selectedRankStrategy}&score_strategy=${selectedScoreStrategy}`;
        const response = await fetch(url,{ headers: {
          Authorization: `Bearer ${token}`,
        }});
        checkStatus(response);
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("Error fetching rank table data:", error);
      }
    };

    fetchRankTableDataTwo();
  }, [selectedRankStrategy]);



  const handleScoreStrategyChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedScoreStrategy(selectedValue);
  };

  const handleRankStrategyChange = (event) => {
    setSelectedRankStrategy(event.target.value);
  };

  useEffect(() => {
    if (isPushed) {
      setIsPushed(false); // Reset is_pushed to false after re-render
    }
  }, [isPushed, setIsPushed]);

  return (
    <>
      <div style={{ marginLeft: "25%", marginRight: "25%" }}>
        <TableContainer component={Paper}>
          <Table
            sx={{ minWidth: 650 }}
            aria-label="game rank table"
            key={selectedScoreStrategy}
          >
            <TableHead>
              <TableRow>
                <TableCell>Ranking</TableCell>
                <TableCell>Team</TableCell>
                <TableCell align="right">Points</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row, index) => (
                <TableRow key={row.team}>
                  <TableCell component="th" scope="row">
                    {index + 1}
                  </TableCell>
                  <TableCell>{row.team}</TableCell>
                  <TableCell align="right">{row.total_score}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>

      <div style={{ marginLeft: "25%", marginRight: "25%", marginTop: "20px" }}>
        <FormControl fullWidth>
          <InputLabel id="score-strategy-label">Scoring Method</InputLabel>
          <Select
            labelId="score-strategy-label"
            id="score-strategy-select"
            value={selectedScoreStrategy}
            onChange={handleScoreStrategyChange}
          >
            {scoreStrategies.map((strategy) => (
              <MenuItem key={strategy} value={strategy}>
                {strategy}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>

      <div style={{ marginLeft: "25%", marginRight: "25%", marginTop: "10px" }}>
        <FormControl fullWidth>
          <InputLabel id="rank-strategy-label">Rank Strategy</InputLabel>
          <Select
            labelId="rank-strategy-label"
            id="rank-strategy-select"
            value={selectedRankStrategy}
            onChange={handleRankStrategyChange}
          >
            {rankStrategies.map((strategy) => (
              <MenuItem key={strategy} value={strategy}>
                {strategy}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
    </>
  );
}
