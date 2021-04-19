import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'

class MonthlyBill extends React.Component {

  static contextType = UserContext;
  constructor(props) {
    super(props);
    this.state = {
      paid: "undefined",
      bills: []
    }
    this.handleclick = this.handleclick.bind(this);
    this.getYourBills = this.getYourBills.bind(this);
  }

  componentDidMount() {
    this.getYourBills();
  }

  getYourBills() {
    unpaidbills(this.context.token)  //
      .then(json => { //   

        console.log(json);  //

        this.setState({
          bills: json.data.ChargesList, //json.data.
          paid: "false"
        })
      })
      .catch(err => {
        if (err.response.status == 402) {
          this.setState({
            paid: "true"
          })
        }
      })

  }

  handleclick(id) {
    console.log("clicked and should be paid");
    console.log(id, this.context.token);
    //    this.props.history.push('/paymentresult');

    paymonth(id, this.context.token)
      .then(() =>
        this.props.history.push({
          pathname: '/paymentresult',
          state: { result: "success" }
        })
      )
      .catch(err => {
        this.props.history.push({
          pathname: '/paymentresult',
          state: { result: "error" }
        })
      });

  }

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
            <h2>Pay unpaid monthly bills!</h2>
            <p>You can see the bills for months you haven't paid yet, and pay them if you want!</p>
            {this.state.paid == "undefined" ?
              <div className="paddingg"></div>
              :
              this.state.paid == "true" ?
                <div className="positivemessage">
                  <p>You have no unpaid monthly bills!</p>
                </div>
                : <div className="allbilltables">

                  {this.state.bills.map((element, key) =>
                    <table className="billtable">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Month</th>
                          <th>Year</th>
                          <th>Total cost</th>
                          <th>Pay</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr key={key}>
                          <td>{element.id}</td>
                          <td>{element.month > 9 ? element.month : "0" + element.month}</td>
                          <td>{element.year}</td>
                          <td>{element.total_amount}</td>
                          <td>
                            <button onClick={() => this.handleclick(element.id)}>Pay!</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  )}

                </div>
            }
          </div>

        </div>
        <Footer />
      </div>

    );
  }
}
export default MonthlyBill;