
import React from 'react';
import './App.css';
import { paymentverif } from './api';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { UserContext } from './UserContext';
import example3 from './example3.json'
import Select from 'react-select';
import { Redirect } from 'react-router-dom';


class Pay extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            point: '',
            protocol: '',
            amount: '',
            energy_amount: '',
            pays: false
        }
        this.cashhandler = this.cashhandler.bind(this);
        this.cardhandler = this.cardhandler.bind(this);
        this.doit = this.doit.bind(this);

    }

    componentDidMount() {
        if (this.props.location.state) {
            console.log("oh fuck");
            console.log(this.props.location.state)
            this.setState({
                point: this.props.location.state.point,
                protocol: this.props.location.state.protocol,
                amount: this.props.location.state.amount,
                energy_amount: this.props.location.state.energy_amount,
                pays: this.props.location.state.pays
            });
            console.log(this.state.point);

            if (!this.props.location.state.pays) {
                this.doit();
            }
        }
        else {
            this.setState({ point: "redirect" });
            console.log("OH NO");
        }
    }


    doit() {
        paymentverif(localStorage.getItem('token'), "monthly", this.props.location.state.protocol, this.props.location.state.energy_amount, this.props.location.state.amount, this.props.location.state.point)
            .then(() => {
                console.log("ok");
            })
            .catch(err => {
                console.log(err);
            });
        console.log("verified for user that doesnt pay now");
    }

    cashhandler() {
        console.log("clicked");
        console.log(this.state);
        paymentverif(localStorage.getItem('token'), "cash", this.state.protocol, this.state.energy_amount, this.state.amount, this.state.point)
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

    cardhandler() {
        console.log("clicked");
        paymentverif(localStorage.getItem('token'), "card", this.state.protocol, this.state.energy_amount, this.state.amount, this.state.point)
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
        if (this.state.point !== "redirect")
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

                            {!this.state.pays ?
                                <>
                                    <h2 style={{ color: '#03ff00' }}>Charging is completed! The total amount of {this.props.location.state.amount}$ has been added to your monthly bill!</h2>
                                    <button className="" type="submit" onClick={() => { this.props.history.push('/'); }} style={{ width: '220px', height: '42px' }}>Back to main page</button>
                                </>
                                : <div className="cashcard">
                                    <h3>Charging is completed! The total amount is {this.props.location.state.amount} $</h3>
                                    <button onClick={this.cashhandler}>Pay with cash</button>
                                    <button onClick={this.cardhandler}>Pay with card</button>
                                </div>
                            }

                        </div>
                    </div>
                    <Footer />
                </div>

            );
        else {
            return (
                <Redirect to="/charge" />
            );
        }
    }
}
export default Pay;