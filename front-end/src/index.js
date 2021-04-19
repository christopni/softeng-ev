import React from 'react';
import ReactDOM from 'react-dom';
//import {BrowserRouter, Switch, Route, useParams, Redirect} from "react-router-dom"
import './index.css';
import App from './App';

const userData = {
  token: localStorage.getItem('token'),
  username: localStorage.getItem('username'),
  user: localStorage.getItem('user')
};


ReactDOM.render(
  <React.StrictMode>
    <App userData={userData}/>
  </React.StrictMode>,
  document.getElementById('root')
);

/*
    <BrowserRouter>
      <Switch>
        <Route path="/" exact>
          <App userData={userData}/>
        </Route>
        <Route path="/ok">
          <Be />
        </Route>
      </Switch>
    </BrowserRouter>
*/