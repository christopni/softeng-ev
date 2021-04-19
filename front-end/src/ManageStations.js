import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import iconfinder_plus_24_103172 from './iconfinder_plus_24_103172.png';
import iconfinder_icons_edit_1564503 from './iconfinder_icons_edit_1564503.png';
import iconfinder_plug_1608796 from './iconfinder_plug_1608796.png'

class ManageStations extends React.Component {



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
        <div className="row23">
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/addlocationofstations" >
                  <div className="flip-card-front">
                    <img src={iconfinder_plus_24_103172} style={{ width: '120px', height: '120px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Add Location</h1>
                    <p>Click here to add a location of stations wherever you like!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/ChooseLocation" >
                  <div className="flip-card-front">
                    <img src={iconfinder_icons_edit_1564503} style={{ width: '120px', height: '120px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Update Location</h1>
                    <p>Click here to update one of your locations of stations!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/ManagePoints" >
                  <div className="flip-card-front">
                    <img src={iconfinder_plug_1608796} style={{ width: '120px', height: '120px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Stations</h1>
                    <p>Click here to add, delete or edit a station!</p>
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
export default ManageStations;