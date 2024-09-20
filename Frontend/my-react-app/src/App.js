import './App.css';
import { useRef } from 'react';
import {
    TextField
} from "@mui/material";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';

function App() {
    // Create a reference to the hidden file input element
  const hiddenFileInput = useRef(null);

  const handleClick = event => {
    hiddenFileInput.current.click();
  };

  // Call a function (passed as a prop from the parent component)
  // to handle the user-selected file
  const handleChange = event => {
    const fileUploaded = event.target.files[0];
    // TODO we have the file, now process it
  };

  return (
    <div className="App">
      <header className="App-header">
        <button className="button-upload" onClick={handleClick}>
            Upload a file
        </button>
        <input
            type="file"
            onChange={handleChange}
            ref={hiddenFileInput}
            style={{display: 'none'}} // Make the file input element invisible
        />
      </header>

      <div className="bodyChat">
        <div className="inputField" >
            <TextField id="userInput" variant="standard" fullWidth
                InputLabelProps={{
                    style: {
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        width: '100%',
                        color: 'white'
                    }
                }}
                sx={{
                    input: {
                        color: "white",
                        borderBottom: "2px solid gray",
                    },
                    "& .MuiInput-underline:after": {
                        borderBottomColor: "orange"
                    }
                }}
                onKeyDown={(ev) => {
                     if (ev.key === 'Enter') {
                         //postUserInput()
                         ev.target.value = ""
                     }
                }}
                onChange={(ev) => {
                     //setInputTextVal(ev.target.value)
                }}
                //value={inputTextVal}
            />
        </div>
            <div className="questionBoxRightIcon">
                 <ArrowUpwardIcon className="arrowUp" style={{color: 'black'}} />
             </div>
       </div>
    </div>
  );
}

export default App;
