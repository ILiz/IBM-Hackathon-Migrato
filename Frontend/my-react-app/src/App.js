import './App.css';
import {v4 as uuidv4} from 'uuid';
import { useRef } from 'react';
import { useState } from "react";
import TextField from "@mui/material/TextField";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Logo from "./images/logo.png";
import User from "./images/user.png";

function App() {
  const hiddenFileInput = useRef(null);
  const [askDisabled, setAskDisabled] = useState(true);
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  
  //Called when a selected file is uploaded.
  const handleUploadFile = event => {
    hiddenFileInput.current.click();
  };
  
  //Called when the selected file changes.
  const onFileChanged = event => {
	console.log("Uploading document");
    uploadFile(event.target.files[0]);
  };
  
  //Uploads a file.
  const uploadFile = async file => {
    const formdata = new FormData();
    formdata.append("file_upload", file);

    fetch('http://127.0.0.1:8000/api/v1/documentSubmitIndexing', {
      method: 'POST',
      body: formdata // Here, stringContent or bufferContent would also work
    })
    .then(function(res) {
      return res.json();
    }).then(function(json) {
      console.log(json);
    });
	
	onFileUploadSuccess(file);
  };
  
  //Called when a file has been uploaded successfully.
  const onFileUploadSuccess = file => {
	const filename = file.name;
	console.log("Uploaded: " + filename);	
	setFiles(
	  [
		...files,
		{ uuid:uuidv4(), name:filename, url:"?" }//TODO: Create object from response with delete link etc.
	  ]
	);
  };
  
  //Called when the user question changes.
  const onQuestionChanged = question => {	
	setAskDisabled(!question);
  };
  
  //Called when the submit question button is clicked.
  const handleAskButtonClick = () => {
	handleSubmitQuestion(document.getElementById('userInput'));
  }
  
  //Called when the user question is submitted.  
  const handleSubmitQuestion = textfield => {
	const question = textfield.value;
	textfield.value = "";
	setAskDisabled(true);
	setMessages(
	  [
		...messages,
		{ uuid:uuidv4(), value:question, owner:"me" }
	  ]
	);
	
	console.log("Sending question: " + question);
	awaitAnswer(question);
  }
  
  //Await answer.
  const awaitAnswer = async question => {
    const formData = new FormData();
        formData.append("question", question);
        const response = await fetch('http://127.0.0.1:8000/api/v1/ragDocumentStreamIBM', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        console.log(data); // Response from Backend is stored here
        onAnswerSuccess(question, data["answer"]);
	};
  
  //Called when a LLM response has been received successfully.
  const onAnswerSuccess = (question, answer) => {
	setMessages(
	  [
		...messages,
		{ uuid:uuidv4(), value:question, owner:"me" },
		{ uuid:uuidv4(), value:answer, owner:"LLM" }
	  ]
	);
  };

  return (
	<div className="App">
		<header className="Top-bar">
			<div className="Top-bar-left">
			</div>
			<div className="Top-bar-center">
				<img src={Logo} alt="Logo" className="Image-logo"/>
			</div>
			<div className="Top-bar-right">
				<img src={User} alt="User" className="Image-user"/>
			</div>
		</header>
		
		<div className="Left-sidebar">
			<div className="Document-header">
				<h1 id="documentHeader">Documents</h1>
			</div>
			<div className="Document-list">
				<List id="documentList" >
					{files.map((file) => (
						<ListItem disablePadding key={file.uuid}>
							<ListItemButton>
								<ListItemText primary={file.name} />
							</ListItemButton>
						</ListItem>
					))}
				</List>
			</div>
			<div className="Document-buttons">
				<Button variant="contained" id="uploadButton" onClick={handleUploadFile} startIcon={<CloudUploadIcon />}>
					Upload document
				</Button>
				<input
					type="file"
					onChange={onFileChanged}
					ref={hiddenFileInput}
					style={{display: 'none'}} // Make the file input element invisible
				/>
			</div>
		</div>

		<div className="App-center">
			<div className="Chatbox">
				<div className="Feedback-box">
					<ul>
					{messages.map((message) => (
						<li key={message.uuid}>{message.value}</li>
					))}
					</ul>
				</div>
				<div className="Input-box" >
					<TextField id="userInput" placeholder="Ask something..." variant="standard"
						InputProps={{ 
							disableUnderline: true 
						}}
						sx={{
							input: {
								color: "black",
							}
						}}
						onKeyDown={(ev) => {
							 if (ev.key === 'Enter') {
								 handleSubmitQuestion(ev.target)
							 }
						}}
						onChange={(ev) => {
							 onQuestionChanged(ev.target.value)
						}}
					/>
					<div className="Input-buttons">
						<Button variant="contained" disabled={askDisabled} onClick={handleAskButtonClick} endIcon={<SendIcon />}>
						  Ask
						</Button>
					</div>
				</div>
			</div>
		</div>
		
	</div>
  );
}

export default App;
