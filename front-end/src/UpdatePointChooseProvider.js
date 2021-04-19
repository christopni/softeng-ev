import React from 'react';
import { displayproviders, updatepointt } from './api';
import './App.css';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';

class UpdatePointChooseProvider extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props)
        this.state = {
            station_id: '',
            providers: []
        }
    }

    componentDidMount() {
        if (this.props.location.state) {
            this.setState({ station_id: this.props.location.state.station_id })
            displayproviders()
                .then(json => {
                    this.setState({ providers: json.data.ProvidersList })

                })
                .catch(err => {
                    this.props.history.push('/FailManageStation')
                });
        }
        else {
            this.setState({ station_id: 'redirect' });
        }
    }


    handleclick = (idd) => {
        updatepointt(this.state.station_id, idd)
            .then(() => {
                //console.log(json)
                this.props.history.push('/SuccessManageStation')
            })
            .catch(err => {
                this.props.history.push('/FailManageStation')
            });
    }


    render() {
        if (this.state.station_id !== "redirect") {
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
                        <h2>Click the Energy Provider you want for your station</h2>
                        <table id="prettytable">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Provider's Name</th>
                                    <th>Fast Charge Cost</th>
                                    <th>Slow Charge Cost</th>
                                </tr>
                            </thead>
                            <tbody>
                                {this.state.providers.map((element, key) =>
                                    <tr onClick={() => this.handleclick(element.ID)} key={key}>
                                        <td>{element.ID}</td>
                                        <td>{element.Name}</td>
                                        <td>{element.FastChargeCost}</td>
                                        <td>{element.LowChargeCost}</td>
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

export default UpdatePointChooseProvider;

