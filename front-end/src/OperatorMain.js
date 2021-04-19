import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import granazi from './granazi.png';
import specificicon from './specificicon.png';

class StatisticsMain extends React.Component {


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
        <div className="row2">
          <div className="maintext2">
            <h2>Welcome {localStorage.getItem('username')}!</h2>
            <p>You can easily manage your stations, or see statistics!</p>
          </div>
          <div className="column3">

            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/managestations" >
                  <div className="flip-card-front">
                    <img src={granazi} style={{ width: '130px', height: '130px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Manage stations</h1>
                    <p>Click here to add or update a station!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="column3">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/statistics" >
                  <div className="flip-card-front">
                    <img src={specificicon} style={{ width: '130px', height: '130px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>See statistics</h1>
                    <p>Click here to see statistics for sessions done in your stations!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>

        </div >

        <Footer />
      </div >

    );
  }
}
export default StatisticsMain;