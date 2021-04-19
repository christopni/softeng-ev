import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import iconfinder_plus_24_103172 from './iconfinder_plus_24_103172.png';
import iconfinder_icons_edit_1564503 from './iconfinder_icons_edit_1564503.png';

class StatisticsMain extends React.Component {


  render() {
    return (

      <div className="loginformdiv">
        <Header />
        <div className="topnav">
          <a href="/be">About us</a>
          <a href="#">Link</a>
          <a href="#">Link</a>
          <a href="#" className="floatmenu">Link</a>
          <a href="#" className="floatmenu">Link</a>
        </div>
        <div class="row2">
          <div className="maintext">
              <p>You can see either general statistics for all the charging points, or specific for each one of them!</p>
          </div>
          <div class="column3">
            <div className="flip-card">
              <div className="flip-card-inner">
              <a href = "/statistics" >
                <div className="flip-card-front">
                <img src={iconfinder_plus_24_103172} style={{width: '120px' ,height: '120px'}}/>
                </div>
                <div className="flip-card-back">
                  <h1>Add Station</h1>
                  <p>Click here to add a station wherever you like!</p>
                </div>
                </a>
              </div>
            </div>
          </div>
          <div class="column3">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href = "/analytics" >
                <div className="flip-card-front">
                <img src={iconfinder_icons_edit_1564503} style={{width: '120px' ,height: '120px'}}/>
                </div>
                <div className="flip-card-back">
                  <h1>Update Station</h1>
                  <p>Click here to update a station that already exists!</p>
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