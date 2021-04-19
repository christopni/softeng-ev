import React from 'react';
import { updatelocation } from './api';
import './App.css';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';

class UpdateLocationOfStations extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props)
        this.state = {
            location_id: '',
            phone: '',
            open_hour: '',
            close_hour: ''
        }
    }


    componentDidMount() {
        if (this.props.location.state) {
            this.setState({ location_id: this.props.location.state.location_id, phone: this.props.location.state.phone, open_hour: this.props.location.state.open_hour, close_hour: this.props.location.state.close_hour })
        }
        else {
            this.setState({ location_id: 'redirect', phone: 'redirect', open_hour: 'redirect', close_hour: 'redirect' });
        }
    }


    changeHandler = e => {
        this.setState({ [e.target.name]: e.target.value })
    }

    handleSubmit = e => {
        e.preventDefault()
        console.log(this.state);
        updatelocation(this.state)
            .then(() => {
                //console.log(json)
                this.props.history.push('/SuccessManageLocation')
            })
            .catch(err => {
                this.props.history.push('/FailManageLocation')
            });
    }


    render() {
        const { location_id, phone, open_hour, close_hour } = this.state
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
                        <div className="column left">
                            <h2>Here you can edit the Location of Stations you picked!</h2>
                            <p>You can change one or more of the given attributes.</p>
                        </div>
                        <div className="column right">
                            <form onSubmit={this.handleSubmit}>
                                <div>
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
        else {
            return (
                <Redirect to="/failmanagelocation" />
            )
        }
    }
}

export default UpdateLocationOfStations;

