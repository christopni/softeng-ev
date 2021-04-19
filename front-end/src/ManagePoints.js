import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import iconfinder_write_126582 from './iconfinder_write_126582.png';
import iconfinder_icons_add_1564491 from './iconfinder_icons_add_1564491.png';
import iconfinder_icons_delete_1564502 from './iconfinder_icons_delete_1564502.png'

class ManagePoints extends React.Component {


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
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/AddPoint" >
                  <div className="flip-card-front">
                    <img src={iconfinder_icons_add_1564491} style={{ width: '120px', height: '120px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Add Station</h1>
                    <p>Click here to add a station wherever you like!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/UpdatePoint" >
                  <div className="flip-card-front">
                    <img src={iconfinder_write_126582} style={{ width: '120px', height: '120px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Update Station</h1>
                    <p>Click here to update one of your stations!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/DeletePoint" >
                  <div className="flip-card-front">
                    <img src={iconfinder_icons_delete_1564502} style={{ width: '120px', height: '120px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Delete Station</h1>
                    <p>Click here to delete one of your stations!</p>
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
export default ManagePoints;