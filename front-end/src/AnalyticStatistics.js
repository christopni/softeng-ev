import React from 'react';
import { stationsprovide } from './api';
import { Bar, Line } from 'react-chartjs-2';
import example1 from './example1';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';
import { UserContext } from './UserContext';


export default class AnalyticStatistics extends React.Component {
  static contextType = UserContext;

  constructor(props) {
    super(props);
    this.state = {
      stations: []
    }
    this.getStationsYouProvide = this.getStationsYouProvide.bind(this);
    this.handleclick = this.handleclick.bind(this);
  }

  componentDidMount() {
    this.getStationsYouProvide();
  }

  getStationsYouProvide() {
    stationsprovide(this.context.token)  //
      .then(json => { //   

        console.log(json.data);  //

        this.setState({
          stations: json.data.StationsList //json.data.
        })
      })

  }

  handleclick = (id) => {
    console.log("clicked");
    this.props.history.push({
      pathname: '/specificstats',
      state: { station_id: id }
    });
  }

  render() {
    return (
      <div className="chartspagediv">
        <Header />
        <div className="topnav">
          <a href="/statistics">General Statistics</a>
          <a href="/specificpoint">Specific Statistics</a>
          <a href="/logout" className="floatmenu">Log out</a>
          <a href="/profile" className="floatmenu">Profile</a>
        </div>
        <div className="row1">
          <div className="chartstext">
            <h1>Charts and statistics</h1>
            <p>
              You can choose one of the following charging stations you provide, in order to see detailed charts concerning the sessions done there.
            </p>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Address</th>
                  <th>Operator</th>
                  <th>Location ID</th>
                  <th>Region</th>
                </tr>
              </thead>
              <tbody>
                {this.state.stations.map((element, key) =>
                  <tr onClick={() => this.handleclick(element.StationID)} key={key}>
                    <td>{element.StationID}</td>
                    <td>{element.Address}</td>
                    <td>{element.OperatorName}</td>
                    <td>{element.LocationID}</td>
                    <td>{element.AddressRegion}</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

        </div>
        <Footer />
      </div>
    );
  }
}
