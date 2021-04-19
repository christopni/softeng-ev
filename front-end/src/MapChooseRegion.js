import React from 'react';
import { displayregions } from './api';
import { UserContext } from './UserContext';
import { Redirect } from 'react-router';
import { Header, Footer } from './HeaderFooter';

class MapChooseRegion extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            regions: [],
            selected_region: ''
        }
        this.changeregion = this.changeregion.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        displayregions()
            .then(json => {
                this.setState({ regions: json.data.LocationsList })

            })
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
                pathname: '/showmap',
                state: { address_region: this.state.selected_region }
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
                <div className="row" style={{ padding: '50px 10px' }}>
                    <h2>Choose a region to see the locations of stations on map.</h2>
                    <form onSubmit={this.handleSubmit}>
                        <select className="regions" onChange={this.changeregion} value={this.state.selected_region}>

                            {this.state.regions.map((element, key) =>

                                <option key={element.address_region} value={element.address_region}>{element.address_region}</option>
                            )}
                        </select>


                        <button className="otherbutton" type="submit"> Submit </button>

                    </form>
                </div>
                <Footer />
            </div>
        )
    }
}

export default MapChooseRegion;

