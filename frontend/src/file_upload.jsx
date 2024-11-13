import axios from 'axios';
import React, { useState } from 'react';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);  // Added state for error message

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setErrorMessage(null);  // Reset error message when a new file is selected
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setErrorMessage(null);  // Reset any previous error message

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Ensure the content type is set correctly
        },
      });

      setResponseData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error uploading file:', error);

      // Check if the error response contains a message and set it to state
      if (error.response && error.response.data && error.response.data.error) {
        setErrorMessage(error.response.data.error);
      } else {
        setErrorMessage('An unknown error occurred.');
      }
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Upload CSV File</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>

      {/* Display error message if there's an error */}
      {errorMessage && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          <strong>{errorMessage}</strong>
        </div>
      )}

      {/* Display the processed data if available */}
      {responseData && (
        <div>
          <h2>Processed Data</h2>
          <pre>{JSON.stringify(responseData.data, null, 2)}</pre>

          <h2>Data Types Before Inference</h2>
          <pre>{JSON.stringify(responseData.data_types_before, null, 2)}</pre>

          <h2>Data Types After Inference</h2>
          <pre>{JSON.stringify(responseData.data_types_after, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
