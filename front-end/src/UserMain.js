import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { UserContext } from './UserContext';

class UserMain extends React.Component {

  static contextType = UserContext;
  constructor(props) {
    super(props);
  }
  /*  componentDidMount(){
      localStorage.removeItem('token');
          localStorage.removeItem('username');
          localStorage.removeItem('user');
  
          this.context.setUserData(null, null, null);
    } */

  render() {
    return (

      <div className="loginformdiv">
        <Header />
        <div className="topnav">
          <a href="/charge">Charge car</a>
          <a href="/mapchooseregion">Points on map</a>
          <a href="/monthlybill">Monthly bill</a>
          <a href="/logout" className="floatmenu">Log out</a>
          <a href="/profile" className="floatmenu">Profile</a>
        </div>
        <div className="row3">
          <div className="maintext">
            <h2>Welcome {this.context.username}!</h2>
            <p>You can easily charge your car, find nearby charging stations, or pay your monthly bill!</p>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/charge" >
                  <div className="flip-card-front">
                    <img src={chargeicon} style={{ width: '130px', height: '130px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Charge car</h1>
                    <p>Click here to charge your car with the program of your choice!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/mapchooseregion" >
                  <div className="flip-card-front">
                    <img src={mapicon} style={{ width: '130px', height: '130px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Stations on map</h1>
                    <p>Click here to find a nearby charging station!</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
          <div className="columnmain">
            <div className="flip-card">
              <div className="flip-card-inner">
                <a href="/monthlybill" >
                  <div className="flip-card-front">
                    <img src={billicon} style={{ width: '130px', height: '130px' }} />
                  </div>
                  <div className="flip-card-back">
                    <h1>Monthly bill</h1>
                    <p>Click here to see and pay your monthly bill!</p>
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
export default UserMain;