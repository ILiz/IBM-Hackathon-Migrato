import './App.css';
import { useRef } from 'react';
import { useState } from "react";
import { createElement } from 'react';
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
  const [list, setList] = useState();
  
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
	//console.log(fileUploaded['name'])
	//const formdata = new FormData();
	//formdata.append("file_upload", fileUploaded);
	//const response = await fetch('http://127.0.0.1:8000/api/v1/documentSubmitIndexing', {
	//	method: 'POST',
	//	body: formdata // Here, stringContent or bufferContent would also work
	//})
	//const data = await response.json();
	//if (data === "File uploaded and indexed") {
	//	setFilename(fileUploaded['name'])
    //}
	
	console.log(file);
	
	//let newFile = createElement(
	//  "h1",
	//  { className: 'greeting' },
	//  { style: { color: "blue" } },
	//  "This is a welcome text"
	//);
	//const newList = list.concat({newFile});
	//setList(newList);
  };
  
  //Called when the user question changes.
  const onQuestionChanged = event => {	
	setAskDisabled(!event.target.value);
  };
  
  //Called when the user question is submitted.
  const handleSubmitQuestion = event => {
	console.log(event.target.value);
	event.target.value = "";
	setAskDisabled(true);
	console.log("sending question") ;
	const fetchData = async () => {
	const formData = new FormData();
        formData.append("question", "What are System 1 and System 2?");
        const response = await fetch('http://127.0.0.1:8000/api/v1/ragDocumentStreamIBM', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        console.log(data); // Response from Backend is stored here
	};
	fetchData();
  }

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
				<List id="documentList" list={list}></List>
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
								 handleSubmitQuestion(ev)
							 }
						}}
						onChange={(ev) => {
							 onQuestionChanged(ev)
						}}
					/>
					<div className="Input-buttons">
						<Button variant="contained" disabled={askDisabled} endIcon={<SendIcon />}>
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
