import React from 'react';
import './App.css';
import { getlocationslist } from './api';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'
import Select from 'react-select';
import { Redirect } from 'react-router-dom';


class ChargeSecond extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            locations: [],
            region: '',
            thereare: true
        }
        this.getLocations = this.getLocations.bind(this);
        this.handleclick = this.handleclick.bind(this);

    }

    //    componentDidMount() {
    //        this.getLocations();
    //    }
    componentDidMount() {
        if (this.props.location.state) {
            this.setState({ region: this.props.location.state.region_name });
            this.getLocations(this.props.location.state.region_name);
        }
        else {
            this.setState({ region: "redirect" });
            console.log("i will redirect bro");
        }
    }

    getLocations(region) {
        console.log("about to get loxations");
        getlocationslist(region, localStorage.getItem('token'))  //
            .then(json => { //   

                console.log(json.data);  //

                this.setState({
                    locations: json.data.LocationsList //json.data.
                })
            })
            .catch(err => {
                if (err.response.status == 402) {
                    this.setState({ thereare: false });
                    console.log("no data!");
                }
            });
        console.log("i got locations");
        console.log(this.state.locations)
    }


    handleclick(id) {
        console.log("clicked");

        this.props.history.push({
            pathname: '/chargethird',
            state: { location_id: id }
        });

    }


    render() {
        if (this.state.region !== "redirect")
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
                            {this.state.thereare ?
                                <div>
                                    <h2>Choose charging station</h2>
                                    <p>Choose in which of the following locations is the charging point where you will charge your car.</p>
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>ID</th>
                                                <th>Address</th>
                                                <th>Postal Code</th>
                                                <th>Region</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {this.state.locations.map((element, key) =>
                                                <tr onClick={() => this.handleclick(element.id)} key={key}>
                                                    <td>{element.id}</td>
                                                    <td>{element.address}</td>
                                                    <td>{element.address_postal_code}</td>
                                                    <td>{element.address_region}</td>
                                                </tr>
                                            )}
                                        </tbody>
                                    </table>

                                </div>
                                :
                                <div>
                                    <p>There are no open charging stations in region {this.state.region}</p> </div>
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
export default ChargeSecond;