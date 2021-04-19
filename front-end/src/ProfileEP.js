import React from 'react';
import { displayinfoep } from './api';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import iconfinder_storm_727681 from './iconfinder_storm_727681.png';

class ProfileEP extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            namee: '',
            id: '',
            fast: '',
            slow: ''
        }
    }

    componentDidMount() {
        displayinfoep()
            .then(json => {
                this.setState({ namee: json.data.Name, id: json.data.ID, fast: json.data.Fast_Charge_Cost, slow: json.data.Slow_Charge_Cost })

            })
            .catch(err => {
                this.props.history.push('/FailManageLocation')
            });
    }

    render() {
        return (
            <div className="loginformdiv">
                <Header />
                <div className="topnav">
                    <a href="/statistics">General Statistics</a>
                    <a href="/specificpoint">Specific Statistics</a>
                    <a href="/logout" className="floatmenu">Log out</a>
                    <a href="/profile" className="floatmenu">Profile</a>
                </div>
                <div className="roww">
                    <div className="columnmain2">
                        <div className="flip-card2">
                            <div className="flip-card-inner2">
                                <div className="flip-card-front2">
                                    <img src={iconfinder_storm_727681} style={{ width: '250px', height: '250px' }} />
                                </div>
                                <div className="flip-card-back2car">
                                    <h1 style={{ paddingBottom: '10px' }}>Name:     {this.state.namee}</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>ID:     {this.state.id}</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>Fast charge cost:     {this.state.fast} $ per kWh</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>Slow charge cost:     {this.state.slow} $ per kWh</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>Username:     {this.context.username}</h1>
                                    <h1>Type: EnergyProvider</h1>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
                <Footer />
            </div>
        )
    }
}

export default ProfileEP;

