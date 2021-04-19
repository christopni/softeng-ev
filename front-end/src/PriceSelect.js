
import React from 'react';
import './App.css';
import { getpointslist, getusertype } from './api';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'
import Select from 'react-select';
import { Redirect } from 'react-router-dom';


class PriceSelect extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            point: '',
            slow_price: '',
            fast_price: '',
            energy_amount: '',
            userpays: ''
        }
        this.handleclick = this.handleclick.bind(this);

    }

    //    componentDidMount() {
    //        this.getPoints();
    //    }
    componentDidMount() {
        if (this.props.location.state) {
            console.log("oh fuck");
            console.log(this.props.location.state.point)
            this.setState({
                point: this.props.location.state.point,
                slow_price: Math.round(this.props.location.state.slow_price * 100) / 100,
                fast_price: Math.round(this.props.location.state.fast_price * 100) / 100,
                energy_amount: Math.round(this.props.location.state.energy_amount * 100) / 100
            });
            getusertype(localStorage.getItem('token'))
                .then(() => {
                    this.setState({ userpays: false })
                    console.log("will NOT pay now!");
                })
                .catch(err => {
                    if (err.response.status == 402) {
                        this.setState({ userpays: true });
                        console.log("will pay now!")
                    }
                });
        }
        else {
            this.setState({ point: "redirect" });
            console.log("OH NO");
        }
    }


    handleclick(event) {
        if (this.state.userpays !== '') {
            console.log("clicked");
            let price = event.target.getAttribute('prot') == "slow" ? this.state.slow_price : this.state.fast_price;
            let protocol = event.target.getAttribute('prot') == "slow" ? "slow" : "fast";
            this.props.history.push({
                pathname: '/pay',
                state: {
                    point: this.state.point,
                    protocol: protocol,
                    amount: price,
                    energy_amount: this.state.energy_amount,
                    pays: this.state.userpays
                }
            });
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
                            <p>Please, chose one of the following programs</p>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Protocol</th>
                                        <th>Total Cost</th>
                                    </tr>
                                </thead>
                                <tbody>

                                    <tr onClick={this.handleclick} prot="slow" key="slow">
                                        <td>Slow</td>
                                        <td>{this.state.slow_price}</td>
                                    </tr>
                                    <tr onClick={this.handleclick} prot="fast" key="fast">
                                        <td>Fast</td>
                                        <td>{this.state.fast_price}</td>
                                    </tr>

                                </tbody>
                            </table>

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
export default PriceSelect;