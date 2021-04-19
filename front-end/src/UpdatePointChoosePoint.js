import React from 'react';
import { displaypoints, } from './api';
import './App.css';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';

class UpdatePointChoosePoint extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props)
        this.state = {
            location_id: '',
            points: []
        }
    }

    componentDidMount() {
        if (this.props.location.state) {
            this.setState({ location_id: this.props.location.state.location_id })
            displaypoints(this.props.location.state.location_id)
                .then(json => {
                    this.setState({ points: json.data.PointsList })

                })
                .catch(err => {
                    this.props.history.push('/FailManageStation')
                });
        }
        else {
            this.setState({ location_id: 'redirect' });
        }
    }


    handleclick = (idd) => {
        this.props.history.push({
            pathname: '/updatepointchooseprovider',
            state: { station_id: idd }
        });
    }


    render() {
        if (this.state.location_id !== "redirect") {
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
                        <h2>Click the station you want to update</h2>
                        <table id="prettytable">
                            <thead>
                                <tr>
                                    <th>Station's ID</th>
                                    <th>Provider</th>
                                </tr>
                            </thead>
                            <tbody>
                                {this.state.points.map((element, key) =>
                                    <tr onClick={() => this.handleclick(element.PointID)} key={key}>
                                        <td>{element.PointID}</td>
                                        <td>{element.ProviderName}</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                    <Footer />
                </div>
            );
        }
        else {
            return (
                <Redirect to="/failmanagestation" />
            )
        }
    }
}

export default UpdatePointChoosePoint;

