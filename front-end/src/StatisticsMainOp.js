import React from 'react';
import { locationsoperate } from './api';
import { Bar, Line } from 'react-chartjs-2';
import example2 from './example2';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';
import { UserContext } from './UserContext';


export default class StatisticsMainOp extends React.Component {
  static contextType = UserContext;

  constructor(props) {
    super(props);
    this.state = {
      locations: []
    }
    this.getYourStations = this.getYourStations.bind(this);
    this.handleclick = this.handleclick.bind(this);
  }

  componentDidMount() {
    this.getYourStations();
  }

  getYourStations() {
    locationsoperate(this.context.token)  //
      .then(json => { //   

        console.log(json);  //

        this.setState({
          locations: json.data.LocationsList //json.data.
        })
      })

  }

  handleclick = (id) => {
    console.log("clicked");
    this.props.history.push({
      pathname: '/specificstats',
      state: { location_id: id }
    });
  }

  render() {
    return (
      <div className="chartspagediv">
        <Header />
        <div className="topnav">
          <a href="/managestations">Manage Stations</a>
          <a href="/statistics">Statistics</a>
          <a href="/logout" className="floatmenu">Log out</a>
          <a href="/profile" className="floatmenu">Profile</a>
        </div>
        <div className="row1">
          <div className="chartstext">
            <h1>Charts and statistics</h1>
            <p>
              You can choose one of the following charging stations you operate, in order to see detailed charts concerning the sessions done there.
            </p>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Address</th>
                  <th>Region</th>
                </tr>
              </thead>
              <tbody>
                {this.state.locations.map((element, key) =>
                  <tr onClick={() => this.handleclick(element.LocationID)} key={key}>
                    <td>{element.LocationID}</td>
                    <td>{element.Address}</td>
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
