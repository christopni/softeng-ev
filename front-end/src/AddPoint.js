import React from 'react';
import { displaylocations } from './api';
import { UserContext } from './UserContext';
import { Redirect } from 'react-router';
import { Header, Footer } from './HeaderFooter';

class AddPoint extends React.Component {

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
                this.props.history.push('/FailManageStation')
            });
    }


    handleclick = (id) => {
        console.log("clicked");
        this.props.history.push({
            pathname: '/addpointchooseprovider',
            state: { location_id: id }
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
                    <h2>Click the location of stations to which you want to add a station</h2>
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
                                <tr onClick={() => this.handleclick(element.LocationID)} key={key}>
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
}

export default AddPoint;

