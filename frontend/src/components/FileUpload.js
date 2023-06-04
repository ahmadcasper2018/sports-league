import React, { useState } from "react";
import { Button } from "@mui/material";
import {is_pushed as isPushedAtom} from "../atoms/authAtom";
import {useRecoilState} from "recoil";
const FileUpload = ({ onFileSelect }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isPushed, setIsPushed] = useRecoilState(isPushedAtom);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("csv_file", selectedFile);

      // Call the onFileSelect function with the form data
      onFileSelect(formData);
    }
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <Button variant="contained" color="primary" onClick={handleFileUpload}>
        Upload
      </Button>
    </div>
  );
};

export default FileUpload;
