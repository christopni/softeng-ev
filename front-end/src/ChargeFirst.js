import React from 'react';
import './App.css';
import { getregionslist } from './api';
import { Header, Footer } from './HeaderFooter';
import chargeicon from './chargeicon.png';
import mapicon from './mapicon.png';
import billicon from './billicon.png';
import { unpaidbills, paymonth } from './api';
import { UserContext } from './UserContext';
import example3 from './example3.json'
import Select from 'react-select';

class ChargeFirst extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            regions: [],
            selected_region: '',
            inserted: true
        }
        this.getRegions = this.getRegions.bind(this);
        this.changeregion = this.changeregion.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    componentDidMount() {
        this.getRegions();
    }

    getRegions() {
        getregionslist(localStorage.getItem('token'))  //
            .then(json => { //   

                console.log(json.data);  //

                this.setState({
                    regions: json.data.LocationsList //json.data.
                })
            });
        console.log("i got regions");
        console.log(this.state)
    }



    changeregion(event) {
        this.setState({ selected_region: event.target.value });
        console.log(event.target.value);
        console.log("what");
    }

    handleSubmit(event) {
        console.log(this.state.selected_region);
        if (this.state.selected_region == '') {
            this.setState({ inserted: false })
        }
        else {
            this.setState({ inserted: true })
            this.props.history.push({
                pathname: '/chargesecond',
                state: { region_name: this.state.selected_region }
            });
        }
        event.preventDefault();

    }


    render() {
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
                        <h2>Choose region</h2>
                        <p>Choose in which of the following regions is the charging point where you will charge your car.</p>
                        <form onSubmit={this.handleSubmit}>
                            <select className="regions" onChange={this.changeregion} value={this.state.selected_region}>

                                {this.state.regions.map((element, key) =>

                                    <option key={element.address_region} value={element.address_region}>{element.address_region}</option>
                                )}
                            </select>


                            <button className="otherbutton" type="submit"> Submit </button>

                        </form>

                    </div>
                    <div className="paddinggg" />

                </div>
                <Footer />
            </div>

        );
    }
}
export default ChargeFirst;