import React from 'react';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import { UserContext } from './UserContext';
class FailManageStation extends React.Component {

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
                    <h2 style={{ color: '#db0d0d' }}>Oops!</h2>
                    <h2 style={{ color: '#db0d0d' }}>Something went wrong.</h2>
                    <button className="button28" type="submit" onClick={() => { this.props.history.push('/managepoints'); }} style={{ width: '180px', height: '42px' }}>Try Again</button>
                </div>

                <Footer />
            </div>

        );
    }
}
export default FailManageStation;