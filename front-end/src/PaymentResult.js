import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json';
import Error from './Error.js';

class PaymentResult extends React.Component {

  static contextType = UserContext;


  render() {
    if (this.props.location.state) {
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
            {this.props.location.state.result == "error" ?
              <div className="paymerror">
                <h2 style={{ color: '#db0d0d' }}>An error occured.</h2>
                <button className="button28" type="submit" onClick={() => { this.props.history.push('/'); }} style={{ width: '180px', height: '42px' }}>Back to main page</button>

              </div>
              :
              <div>
                <h2 style={{ color: '#03ff00' }}>The payment was succesfull!</h2>
                <button className="button28" type="submit" onClick={() => { this.props.history.push('/'); }} style={{ width: '180px', height: '57px' }}>Back to main page</button>
              </div>
            }
          </div>
          <Footer />
        </div>

      );
    }
    else {
      return (
        <Error />
      );
    }
  }
}
export default PaymentResult;