
import React from 'react';
import './App.css';
import { getpointslist } from './api';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'
import Select from 'react-select';
import { Redirect } from 'react-router-dom';


class ChargeThird extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            points: [],
            location_id: '',
            thereare: true
        }
        this.getPoints = this.getPoints.bind(this);
        this.handleclick = this.handleclick.bind(this);

    }

    //    componentDidMount() {
    //        this.getPoints();
    //    }
    componentDidMount() {
        if (this.props.location.state) {
            this.setState({ location_id: this.props.location.state.location_id });
            this.getPoints(this.props.location.state.location_id);
        }
        else {
            this.setState({ location_id: "redirect" });
            console.log("i will redirect bro");
        }
    }

    getPoints(location_id) {
        console.log("about to get points");
        getpointslist(location_id, localStorage.getItem('token'))  //
            .then(json => { //   

                console.log(json.data);  //

                this.setState({
                    points: json.data.PointsList //json.data.
                })
            })
            .catch(err => {
                if (err.response.status == 402) {
                    this.setState({ thereare: false });
                    console.log("no data!");
                }
            });
        console.log("i got location_ids");
        console.log(this.state.points)
    }


    handleclick(point_obj) {
        console.log("clicked");

        this.props.history.push({
            pathname: '/programselect',
            state: { point: point_obj }
        });

    }


    render() {
        if (this.state.location_id !== "redirect")
            return (

                <div className="loginformdiv">
                    <Header />
                    <div className="topnav">
                        <a href="/charge">Charge car</a>
                        <a href="/mapchooseregion">Points on map</a>
                        <a href="/monthlybill">Monthly bill</a>
                        <a href="/logout" className="floatmenu">Log out</a>
                        <a href="/profile" className="floatmenu">Profile</a>
                    </div>
                    <div className="row3">
                        <div className="maintext">
                            {this.state.thereare ?
                                <div>
                                    <h2>Choose charging point</h2>
                                    <p>Choose in which of the following charging points you will charge your car.</p>
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>ID</th>
                                                <th>Fast charge cost</th>
                                                <th>Slow charge cost</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {this.state.points.map((element, key) =>
                                                <tr onClick={() => this.handleclick(element)} key={key}>
                                                    <td>{element.PointID}</td>
                                                    <td>{element.Fast_Charge_Cost}</td>
                                                    <td>{element.Slow_Charge_Cost}</td>
                                                </tr>
                                            )}
                                        </tbody>
                                    </table>

                                </div>
                                :
                                <div>
                                    <p>There are no available charging points in charging station {this.state.location_id}</p> </div>
                            }
                        </div>
                    </div>
                    <Footer />
                </div>

            );
        else {
            return (
                <Redirect to="/charge" />
            );
        }
    }
}
export default ChargeThird;