import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import analyticicon from './analyticicon.png';
import specificicon from './specificicon.png';

class StatisticsMain extends React.Component {


  render() {
    return (

      <div className="loginformdiv">
        <Header />
        <div className="topnav">
          <a href="/statistics">General Statistics</a>
          <a href="/specificpoint">Specific Statistics</a>
          <a href="/logout" className="floatmenu">Log out</a>
          <a href="/profile" className="floatmenu">Profile</a>
        </div>
        <div className="row2">
        <div className="maintext2">
            <h2>Welcome {localStorage.getItem('username')}!</h2>
          </div>
          <div className="column3">
            <div className="flip-card3">
              <div className="flip-card-inner3">
                <a href="/statistics" >
                  <div className="flip-card-front3">
                    <img src={analyticicon} style={{ width: '120px', height: '120px' }} />
                    <h1>Statistics for all your charging points</h1>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="column3">
            <div className="flip-card3">
              <div className="flip-card-inner3">
                <a href="/specificpoint" >
                  <div className="flip-card-front3">
                    <img src={specificicon} style={{ width: '120px', height: '120px' }} />
                    <h1>Statistics for one of your charging points</h1>
                  </div>
                </a>
              </div>
            </div>
          </div>

        </div>

        <Footer />
      </div>

    );
  }
}
export default StatisticsMain;