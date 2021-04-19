import React from 'react';
import { displaylocations } from './api';
import { UserContext } from './UserContext';
import { Redirect } from 'react-router';
import { Header, Footer } from './HeaderFooter';

class ChooseLocation extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            locations: []
        }
    }

    componentDidMount() {
        displaylocations()
            .then(json => {
                this.setState({ locations: json.data.LocationsList })

            })
            .catch(err => {
                this.props.history.push('/FailManageLocation')
            });
    }


    handleclick = (id, ph, oh, ch) => {
        console.log("clicked");
        this.props.history.push({
            pathname: '/updatelocationofstations',
            state: { location_id: id, phone: ph, open_hour: oh, close_hour: ch }
        });
    }


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
                <div className="row">
                    <h2>Click the location of stations you want to update</h2>
                    <table id="prettytable">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Address</th>
                                <th>Postal Code</th>
                                <th>Region</th>
                                <th>Phone</th>
                                <th>Open Hour</th>
                                <th>Close Hour</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.locations.map((element, key) =>
                                <tr onClick={() => this.handleclick(element.LocationID, element.Phone, element.OpenHours, element.CloseHours)} key={key}>
                                    <td>{element.LocationID}</td>
                                    <td>{element.Address}</td>
                                    <td>{element.AddressPostalCode}</td>
                                    <td>{element.AddressRegion}</td>
                                    <td>{element.Phone}</td>
                                    <td>{element.OpenHours}</td>
                                    <td>{element.CloseHours}</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
                <Footer />
            </div>
        )
    }

    /*render() {
        //const { address, address_postal_code, address_region, phone, open_hour, close_hour } = this.state
        return (
            <div className="loginformdiv">
                <Header />
                 onClick={() => this.handleclick(element.LocationID)}
                <div className="topnav">
                    <a href="/be">About us</a>
                    <a href="#">Link</a>
                    <a href="#">Link</a>
                    <a href="#" className="floatmenu">Link</a>
                    <a href="#" className="floatmenu">Link</a>
                </div>
                <div className="row">
                    <div className="column left">
                        <h2>Add a new Location of Stations</h2>
                        <p>Specify the characteristics of the Station.</p>
                    </div>
                    <div className="column right">
                        <form onSubmit={this.handleSubmit}>

                            <label for="addrs">Address</label>
                            <input type="text" id="addrs" name="address" placeholder="Address" value={address} onChange={this.changeHandler}></input>

                            <label for="addrspcode">Postal Code</label>
                            <input type="text" id="addrspcode" name="address_postal_code" placeholder="Postal Code" value={address_postal_code} onChange={this.changeHandler}></input>

                            <label for="addrsregion">Area</label>
                            <input type="text" id="addrsregion" name="address_region" placeholder="Area" value={address_region} onChange={this.changeHandler}></input>

                            <label for="phone">Phone Number</label>
                            <input type="text" id="phone" name="phone" placeholder="Phone Number" value={phone} onChange={this.changeHandler}></input>

                            <label for="ohours">Opening Hours</label>
                            <input type="text" id="ohours" name="open_hour" placeholder="Opening Hours" value={open_hour} onChange={this.changeHandler}></input>

                            <label for="chours">Closing Hours</label>
                            <input type="text" id="chours" name="close_hour" placeholder="Closing Hours" value={close_hour} onChange={this.changeHandler}></input>

                            <div className="rowform">
                                <button className="" type="submit"> Login </button>
                            </div>

                        </form>
                    </div>
                </div>
                <Footer />
            </div>
        );
    }*/
}

export default ChooseLocation;

