import React from "react";
import logo from "./logo.svg";
import "./App.css";
import CssBaseline from "@mui/material/CssBaseline";

function App() {
    return (
        <React.Fragment>
                <CssBaseline />
                <div className="App">
                    <header className="App-header">
                        <img src={logo} className="App-logo" alt="logo" />
                        <p>
                            Edit <code>src/App.tsx</code> and save to reload.
                        </p>
                        <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer">
                            Learn React
                        </a>
                    </header>
                </div>
        </React.Fragment>
    );
}

export default App;
