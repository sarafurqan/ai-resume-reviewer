import React, { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import { CircularProgress, LinearProgress } from "@mui/material";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
    multiple: false,
  });
  

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a resume.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/upload_resume/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Upload failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto", textAlign: "center" }}>
      <h2>Upload Resume for ATS Analysis</h2>

      {/* Drag & Drop File Upload */}
      <div {...getRootProps()} style={{
        border: "2px dashed #007bff",
        padding: "20px",
        cursor: "pointer",
        marginBottom: "10px"
      }}>
        <input {...getInputProps()} />
        {file ? <p>{file.name}</p> : <p>Drag & drop a resume here, or click to select one</p>}
      </div>

      {/* Job Description Input */}
      <textarea
        placeholder="Paste job description (optional)"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        rows="4"
        style={{ width: "100%", marginBottom: "10px", padding: "10px" }}
      />

      {/* Upload Button */}
      <button onClick={handleUpload} disabled={loading} style={{
        padding: "10px 20px",
        background: "#007bff",
        color: "white",
        border: "none",
        cursor: "pointer"
      }}>
        {loading ? "Uploading..." : "Upload & Analyze"}
      </button>

      {/* Loading Indicator */}
      {loading && <CircularProgress style={{ marginTop: "20px" }} />}

      {/* Display Results */}
      {response && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>Results:</h3>

          {/* ATS Score Progress Bar */}
          {response?.ats_results && (
            <div style={{ marginBottom: "20px" }}>
              <h3>ATS Score:</h3>
              <LinearProgress
                variant="determinate"
                value={response.ats_results.ats_score || 0}
                style={{ height: "10px", borderRadius: "5px" }}
              />
              <p><strong>{response.ats_results.ats_score}%</strong> ATS match</p>
            </div>
          )}

          {/* Keyword Matching Pie Chart */}
          {response?.ats_results?.keyword_analysis && (
            <div style={{ marginBottom: "20px" }}>
              <h3>Keyword Match Analysis</h3>
              <Pie
                data={{
                  labels: ["Matched Keywords", "Missing Keywords"],
                  datasets: [
                    {
                      data: [
                        response.ats_results.keyword_analysis.matched_keywords.length,
                        100 - response.ats_results.keyword_analysis.matched_keywords.length,
                      ],
                      backgroundColor: ["#4caf50", "#f44336"],
                    },
                  ],
                }}
              />
            </div>
          )}

          {/* Extracted Skills */}
          {response?.skills_extracted && (
            <div>
              <h3>Extracted Skills:</h3>
              <p>{response.skills_extracted.skills_extracted?.join(", ") || "No skills detected"}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
