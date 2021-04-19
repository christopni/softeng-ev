import React from 'react';
import { energysessions } from './api';
import { Bar, Line, Pie } from 'react-chartjs-2';
import example from './example';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';
import { pointsessions } from './api';


export default class SpecificStats extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      chart1Data: {},
      chart2Data: {},
      //      chart3Data: {},
      chart4Data: {},
      year: 2021,
      thereare: true,
      station_id: ""
    }
    this.changeyear = this.changeyear.bind(this);
    this.getChartData = this.getChartData.bind(this);
  }

  componentDidMount() {
    if (this.props.location.state) {
      this.setState({ station_id: this.props.location.state.station_id })
      this.getChartData(this.state.year, this.props.location.state.station_id);
    }
    else {
      this.setState({ station_id: "redirect" });
    }
  }

  changeyear(event) {
    this.setState({ year: event.target.value });
    this.getChartData(event.target.value, this.state.station_id);
  }

  getChartData(myyear, myid) {
    let ch1data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let ch2data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    //    let ch3data = [];
    let ch4data = [0, 0];
    let ch1labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    let ch2labels = ["Slow", "Fast"];
    //    let ch3labels = [];
    let token = localStorage.getItem('token');
    console.log("about to get data");
    pointsessions(myyear + "0101", myyear + "1231", token, myid)  //
      .then(json => { //   
        console.log(json.data);  //
        const sessionlist = json.data.ChargingSessionsList; //json.data αντί για example
        sessionlist.forEach(element => {
          let date = new Date(element.FinishedOn);
          let index = date.getMonth();
          ch1data[index]++;
          ch2data[index] += element.EnergyDelivered;
          element.Protocol == "fast" ?
            ch4data[1]++ :
            ch4data[0]++;

        })  //
        console.log(ch1data);
        this.setState({
          chart1Data: {
            labels: ch1labels,
            datasets: [
              {
                label: 'Sessions',
                fill: false,
                lineTension: 0,
                backgroundColor: 'rgba(75,192,192,1)',
                borderColor: 'rgba(0,0,0,1)',
                borderWidth: 2,
                data: ch1data
              }
            ]
          },
          chart2Data: {
            labels: ch1labels,
            datasets: [
              {
                label: 'Earnings',
                fill: false,
                lineTension: 0,
                backgroundColor: 'rgba(75,192,192,1)',
                borderColor: 'rgba(0,0,0,1)',
                borderWidth: 2,
                data: ch2data
              }
            ]
          },
          thereare: true,
          chart4Data: {
            labels: ch2labels,
            datasets: [
              {
                label: 'Earnings',
                fill: false,
                lineTension: 0,
                backgroundColor: ['rgb(86, 179, 255)', 'rgb(250, 129, 130)'],
                borderColor: 'rgba(0,0,0,1)',
                borderWidth: 2,
                data: ch4data
              }
            ]
          }
        })
      })//
      .catch(err => {
        if (err.response.status == 402) {
          this.setState({ thereare: false });
        }
      });

  }

  render() {
    if (this.state.station_id !== "redirect")
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
              <h1>Charts and statistics for charging point {this.state.station_id}</h1>
              <p>
                You have the opportunity to see statistics for the charging sessions done in the charging points you provide.
              </p>
              <h5>Watch charts for year:{' '}
                <select onChange={this.changeyear} value={this.state.year}>
                  <option key="2021" value="2021">2021</option>
                  <option key="2020" value="2020">2020</option>
                  <option key="2019" value="2019">2019</option>
                  <option key="2018" value="2018">2018</option>
                </select>
              </h5>
            </div>
            {this.state.thereare ?
              <div className="charts">
                <div className="chart">
                  <Bar
                    data={this.state.chart1Data}
                    options={{
                      title: {
                        display: true,
                        text: 'Sessions per month',
                        fontSize: 20,
                        fontFamily: "'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif"
                      },
                      scales: {
                        yAxes: [{
                          ticks: {
                            beginAtZero: true
                          }
                        }]
                      },
                      legend: {
                        display: true,
                        position: 'right',
                        fontFamily: "'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif"
                      }
                    }}
                  />
                </div>
                <div className="chart">
                  <Bar
                    data={this.state.chart2Data}
                    options={{
                      title: {
                        display: true,
                        text: 'Energy provided per month',
                        fontSize: 20,
                        fontFamily: "'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif"
                      },
                      scales: {
                        yAxes: [{
                          ticks: {
                            beginAtZero: true
                          }
                        }]
                      },
                      legend: {
                        display: true,
                        position: 'right'
                      }
                    }}
                  />
                </div>

                <div className="chart">
                  <Pie
                    data={this.state.chart4Data}
                    options={{
                      title: {
                        display: true,
                        text: 'Charging program used',
                        fontSize: 20,
                        fontFamily: "'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif"
                      },
                      legend: { display: true, position: "right" },

                      datalabels: {
                        display: true,
                        color: "white",
                      },
                      tooltips: {
                        backgroundColor: "#5a6e7f"
                      }
                    }}
                  />
                </div>
              </div>
              : <div className="error">
                <p>No sessions in requested year!</p>
              </div>
            }
          </div>
          <Footer />
        </div>
      );
    else {
      return (
        <Redirect to="/analytics" />
      )
    }
  }
}
 /*
           <div className="chart">
            <Bar
              data={this.state.chart3Data}
              options={{
                title: {
                  display: true,
                  text: 'Earnings per Charging Point',
                  fontSize: 20,
                  fontFamily:"'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif"
                },
                scales: {
                  yAxes: [{
                    ticks: {
                      beginAtZero: true
                    }
                  }]
                },
                legend: {
                  display: true,
                  position: 'right'
                }
              }}
            />
          </div>
          */