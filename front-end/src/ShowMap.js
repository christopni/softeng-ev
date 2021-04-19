import React from 'react';
import ReactDOM from 'react-dom';
import ReactMapGL, { Marker } from 'react-map-gl';
import { displaycoordinates } from './api';
import { UserContext } from './UserContext';
import mapboxgl from 'mapbox-gl';
import './App.css';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';


mapboxgl.accessToken = 'pk.eyJ1IjoiZnJvY2hyIiwiYSI6ImNrbTdwZDRhZjEwZHgyb253bmM4a2I0ODIifQ.yr5LJsTYL43HVAJH2w3kCA';


class ShowMap extends React.Component {

  static contextType = UserContext;

  constructor(props) {
    super(props);
    this.state = {
      coordinates: [],
      zoom: 8,
      address_region: ''
    }
  }
  componentDidMount() {
    if (this.props.location.state) {
      this.setState({ address_region: this.props.location.state.address_region })
      displaycoordinates(this.props.location.state.address_region)
        .then(json => {
          //console.log(json)
          this.setState({ coordinates: json.data.LocationsList })
          //console.log(this.state.coordinates)

          var map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [this.state.coordinates[0].longitude, this.state.coordinates[0].latitude],
            zoom: this.state.zoom


          });

          for (var i = 0; i < this.state.coordinates.length; i++) {
            var marker = new mapboxgl.Marker()
              .setLngLat([this.state.coordinates[i].longitude, this.state.coordinates[i].latitude])
              .addTo(map);
          }
        })
        .catch(err => {
          this.props.history.push('/FailManageStation')
        });
    }
    else {
      this.setState({ address_region: 'redirect' });
    }
    /*displaycoordinates()
        .then(json => {
            this.setState({ coordinates: json.data.LocationsList })

        })*/

    /*const {coordinates} = this.state

    coordinates.forEach((id) => {
      console.log("yea")
      var marker = new mapboxgl.Marker()
        .setLngLat([parseFloat(id.longitude), parseFloat(id.latitude)])
        .addTo(map);
    })*/
    //console.log(this.state.coordinates.length)



  }

  render() {
    if (this.state.address_region !== "redirect") {

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
          <div className="row3" style={{ padding: '60px 20px' }}>
            <h2>Charging stations in {this.state.address_region}</h2>
            <div ref={el => this.mapContainer = el} style={{ width: '100%', height: '100vh' }}>

            </div>

          </div>

          <Footer />
        </div>

      );
    }
    else {
      return (
        <Redirect to="/mapchooseregion" />
      )
    }

  }
}
export default ShowMap;