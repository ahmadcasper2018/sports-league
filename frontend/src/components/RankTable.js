import React, { useState, useEffect } from "react";
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
  const [scoreStrategies, setScoreStrategies] = useState([]);
  const [rankStrategies, setRankStrategies] = useState([]);
  const [selectedScoreStrategy, setSelectedScoreStrategy] = useState("");
  const [selectedRankStrategy, setSelectedRankStrategy] = useState("");

  useEffect(() => {
    const fetchGameRankData = async () => {
      try {
        const rankResponse = await fetch("http://127.0.0.1:8000/game/rank/");
        const rankData = await rankResponse.json();
        setData(rankData);

        const scoreStrategiesResponse = await fetch(
          "http://127.0.0.1:8000/game/score-strategies/"
        );
        const scoreStrategiesData = await scoreStrategiesResponse.json();
        setScoreStrategies(
          scoreStrategiesData.strategies.map((strategy) => strategy)
        );

        const rankStrategiesResponse = await fetch(
          "http://127.0.0.1:8000/game/rank-strategies/"
        );
        const rankStrategiesData = await rankStrategiesResponse.json();
        setRankStrategies(
          rankStrategiesData.strategies.map((strategy) => strategy)
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchGameRankData();
  }, []);

  useEffect(() => {
    const fetchRankTableData = async () => {
      try {
        const url = `http://127.0.0.1:8000/game/rank/?score_strategy=${selectedScoreStrategy}`;
        const response = await fetch(url);
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("Error fetching rank table data:", error);
      }
    };

    fetchRankTableData();
  }, [selectedScoreStrategy]);

  const handleScoreStrategyChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedScoreStrategy(selectedValue);
  };

  const handleRankStrategyChange = (event) => {
    setSelectedRankStrategy(event.target.value);
  };

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
                <TableCell align="right">Total Score</TableCell>
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
