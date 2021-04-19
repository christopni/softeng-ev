import React from 'react';
import { addlocation } from './api';
import './App.css';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';

class AddLocationOfStations extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props)
        this.state = {
            address: '',
            address_postal_code: '',
            address_region: '',
            phone: '',
            open_hour: '',
            close_hour: ''
        }
    }

    changeHandler = e => {
        this.setState({ [e.target.name]: e.target.value })
    }

    handleSubmit = e => {
        e.preventDefault()
        console.log(this.state);
        addlocation(this.state)
            .then(() => {
                //console.log(json)
                this.props.history.push('/SuccessManageLocation')
            })
            .catch(err => {
                this.props.history.push('/FailManageLocation')
            });
    }


    render() {
        const { address, address_postal_code, address_region, phone, open_hour, close_hour } = this.state
        return (
            <div className="loginformdiv">
                <Header />
                <div className="topnav">
                    <a href="/managestations">Manage Stations</a>
                    <a href="/statistics">Statistics</a>
                    <a href="/logout" className="floatmenu">Log out</a>
                    <a href="/profile" className="floatmenu">Profile</a>
                </div>
                <div className="row">
                    <div className="column left">
                        <h2>Add a new Location of Stations</h2>
                        <p>Specify the characteristics of the Station.</p>
                    </div>
                    <div className="column right">
                        <form onSubmit={this.handleSubmit}>
                            <div>
                                <label for="addrs">Address</label>
                                <input type="text" id="addrs" name="address" placeholder="Address" value={address} onChange={this.changeHandler} />
                            </div><div>
                                <label for="addrspcode">Postal Code</label>
                                <input type="text" id="addrspcode" name="address_postal_code" placeholder="Postal Code" value={address_postal_code} onChange={this.changeHandler} />
                            </div><div>
                                <label for="addrsregion">Area</label>
                                <input type="text" id="addrsregion" name="address_region" placeholder="Area" value={address_region} onChange={this.changeHandler} />
                            </div><div>
                                <label for="phone">Phone Number</label>
                                <input type="text" id="phone" name="phone" placeholder="Phone Number" value={phone} onChange={this.changeHandler} />
                            </div><div>
                                <label for="ohours">Opening Hours</label>
                                <input type="text" id="ohours" name="open_hour" placeholder="Opening Hours" value={open_hour} onChange={this.changeHandler} />
                            </div><div>
                                <label for="chours">Closing Hours</label>
                                <input type="text" id="chours" name="close_hour" placeholder="Closing Hours" value={close_hour} onChange={this.changeHandler} />
                            </div>
                            <div className="rowform">
                                <button className="" type="submit"> Submit </button>
                            </div>

                        </form>
                    </div>
                </div>
                <Footer />
            </div>
        );
    }
}

export default AddLocationOfStations;

