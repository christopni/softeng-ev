
import React from 'react';
import './App.css';
import { getpointslist } from './api';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'
import Select from 'react-select';
import { Redirect } from 'react-router-dom';


class ProgramSelect extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            sbattery: '',
            fbattery: '',
            point: '',
            error: false
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handler1change = this.handler1change.bind(this);
        this.handler2change = this.handler2change.bind(this);

    }

    //    componentDidMount() {
    //        this.getPoints();
    //    }
    componentDidMount() {
        if (this.props.location.state) {
            console.log("We did it");
            console.log(this.props.location.state.point)
            this.setState({ point: this.props.location.state.point });
        }
        else {
            this.setState({ point: "redirect" });
            console.log("OH NO");
        }
    }


    handler1change(event) {
        this.setState({ sbattery: event.target.value });
    }

    handler2change(event) {
        this.setState({ fbattery: event.target.value });
    }

    handleSubmit(event) {
        console.log("clicked");
        console.log(this.state.sbattery);
        console.log(this.state.fbattery);
        if (this.state.sbattery < this.state.fbattery) {
            let energy = this.state.fbattery - this.state.sbattery;
            let slow_val = energy * this.state.point.Slow_Charge_Cost;
            let fast_val = energy * this.state.point.Fast_Charge_Cost;
            this.setState({ error: false })
            console.log("i will proceed!");
            this.props.history.push({
                pathname: '/priceselect',
                state: {
                    point: this.state.point.PointID,
                    slow_price: slow_val,
                    fast_price: fast_val,
                    energy_amount: energy
                }
            });
        }
        else {
            this.setState({ error: true })
        }
        event.preventDefault();

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

                            <h2>Charging options</h2>
                            <p>Please, enter your current battery and the target battery percentage.</p>
                            <div className="programform">
                                <form onSubmit={this.handleSubmit}>
                                    <input id="sbattery" type="number" min="0" max="100" step="0.01" onChange={this.handler1change} value={this.state.sbattery} required />
                                    <input id="fbattery" type="number" min="0" max="100" step="0.01" onChange={this.handler2change} value={this.state.fbattery} required />
                                    <button className="" type="submit"> Submit </button>
                                </form>
                            </div>
                            {this.state.error ?
                                <p>The target battery has to be bigger than the current!</p>
                                : <> </>
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
export default ProgramSelect;