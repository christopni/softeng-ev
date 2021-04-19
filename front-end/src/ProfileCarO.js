import React from 'react';
import { displayinfocar } from './api';
import { UserContext } from './UserContext';
import { Header, Footer } from './HeaderFooter';
import image_car_owner from './image_car_owner.png';

class ProfileCarO extends React.Component {

    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            card: '',
            id: '',
            phone: '',
            brand: '',
            model: '',
            year: ''

        }
    }

    componentDidMount() {
        displayinfocar()
            .then(json => {
                this.setState({ id: json.data.ID, card: json.data.CardNumber, phone: json.data.Phone, brand: json.data.BrandType, model: json.data.Model, year: json.data.ReleaseYear })

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
                    <a href="/charge">Charge car</a>
                    <a href="/mapchooseregion">Points on map</a>
                    <a href="/monthlybill">Monthly bill</a>
                    <a href="/logout" className="floatmenu">Log out</a>
                    <a href="/profile" className="floatmenu">Profile</a>
                </div>
                <div className="roww">
                    <div className="columnmain2">
                        <div className="flip-card2">
                            <div className="flip-card-inner2">
                                <div className="flip-card-front2">
                                    <img src={image_car_owner} style={{ width: '250px', height: '250px' }} />
                                </div>
                                <div className="flip-card-back2car">
                                    <h1 style={{ paddingBottom: '10px' }}>Username:     {this.context.username}</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>ID:     {this.state.id}</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>Car:     {this.state.brand} {this.state.model} {this.state.year}</h1>
                                    <h1 style={{ paddingBottom: '10px' }}>Phone:     {this.state.phone}</h1>
                                    <h1 style={{ paddingBottom: '20px' }}>Card:     {this.state.card}</h1>
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

export default ProfileCarO;

