import React from 'react';
import { displayinfoop } from './api';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import iconfinder_Charging_station_6956548 from './iconfinder_Charging_station_6956548.png';

class ProfileOp extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            namee: '',
            id: ''
        }
    }

    componentDidMount() {
        displayinfoop()
            .then(json => {
                this.setState({ namee: json.data.Name, id: json.data.ID })

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
                    <a href="/managestations">Manage Stations</a>
                    <a href="/statistics">Statistics</a>
                    <a href="/logout" className="floatmenu">Log out</a>
                    <a href="/profile" className="floatmenu">Profile</a>
                </div>
                <div className="roww">
                    <div className="columnmain2">
                        <div className="flip-card2">
                            <div className="flip-card-inner2">
                                <div className="flip-card-front2">
                                    <img src={iconfinder_Charging_station_6956548} style={{ width: '250px', height: '250px' }} />
                                </div>
                                <div className="flip-card-back2">
                                    <h1 style={{ paddingBottom: '20px' }}>Name:     {this.state.namee}</h1>
                                    <h1 style={{ paddingBottom: '20px' }}>ID:     {this.state.id}</h1>
                                    <h1 style={{ paddingBottom: '20px' }}>Username:     {this.context.username}</h1>
                                    <h1>Type:     {this.context.user}</h1>
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

export default ProfileOp;

