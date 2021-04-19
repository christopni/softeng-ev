import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import { UserContext } from './UserContext';
class SuccessManageLocation extends React.Component {

    static contextType = UserContext;

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
                <div className="row3">
                    <h2 style={{ color: '#03ff00' }}>Success!</h2>
                    <h2 style={{ color: '#03ff00' }}>Everything went smoothly.</h2>
                    <button className="button28" type="submit" onClick={() => { this.props.history.push('/'); }} style={{ width: '180px', height: '57px' }}>Back to Manage Locations of Stations</button>
                </div>

                <Footer />
            </div>

        );
    }
}
export default SuccessManageLocation;