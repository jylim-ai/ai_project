import logo from './logo.svg';
import { useState } from "react";
import axios from "axios";
import './App.css';

function App() {


  const [resumeFile, setResumeFile] = useState(null);
  const [jobs, setJobs] = useState([]);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", resumeFile); // key "file" is important

    try {
      const res = await axios.post("http://localhost:8000/match_resume", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      setJobs(res.data.jobs_result);
      console.log(jobs);
    } catch (err) {
      console.error(err);
    }
  };



  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        
      </header>

      <div className="app-container">
        <h1>AI Job Matching Agent</h1>

        <form onSubmit={handleSubmit} className="resume-form">
          <h2>Choose your resume file (.pdf)</h2>
          <h2>Scan your resume</h2>
          <h2>Find job that matches your resume</h2>
          <input
            type="file"
            accept=".txt,.pdf,.doc,.docx"
            onChange={handleFileChange}
            style={{ marginTop: "15px" }}
          />
          <button type="submit">Find Jobs</button>
        </form>

        <div>
          {jobs?.length > 0 && <h2 style={{ color: "#111827", marginBottom: "20px" }}>Top Jobs:</h2>}
          {jobs?.map((job, index) => (
            <div key={index} className="job-card">
              <strong>{job.job_title || "No Title"}</strong> - {job.company}
              <br />
              <a href={job.URL} target="_blank" rel="noopener noreferrer">
                View Job
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
