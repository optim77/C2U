import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom'; // Import BrowserRouter
import reportWebVitals from './reportWebVitals';
import Main from "./Main";
import 'bootstrap/dist/css/bootstrap.css';
import './styles/style.css'

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <BrowserRouter>
        <Main />
    </BrowserRouter>
);
