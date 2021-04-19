import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'

class Error3 extends React.Component {

  render() {
    return (
      <div className="loginformdiv">
        <Header />
        <div className="topnav">
          <a href="/managestations">Manage Stations</a>
          <a href="/statistics">Statistics</a>
          <a href="/logout" className="floatmenu">Log out</a>
          <a href="/profile" className="floatmenu">Profile</a>
        </div>
        <div className="row3">
          <div className="paymerror">
            <h2>Error: The requested page was not found.</h2>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
}
export default Error3;