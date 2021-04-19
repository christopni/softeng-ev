import React from 'react';
import { energysessions } from './api';
import { Bar, Line, Pie } from 'react-chartjs-2';
import example from './example';
import { Header, Footer } from './HeaderFooter';
import { Redirect } from 'react-router';
import { stationsessions } from './api';
import moment from 'moment';


export default class SpecificStatsOp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      chart1Data: {},
      chart2Data: {},
      chart3Data: {},
      chart4Data: {},
      year: 2021,
      thereare: true,
      location_id: ""
    }
    this.changeyear = this.changeyear.bind(this);
    this.getChartData = this.getChartData.bind(this);
  }

  componentDidMount() {
    if (this.props.location.state) {
      this.setState({ location_id: this.props.location.state.location_id })
      this.getChartData(this.state.year, this.props.location.state.location_id);
    }
    else {
      this.setState({ location_id: "redirect" });
    }
  }

  changeyear(event) {
    this.setState({ year: event.target.value });
    this.getChartData(event.target.value, this.state.location_id);
  }

  getChartData(myyear, myid) {
    let ch1data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let ch2data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let ch3data = [];
    let ch4data = [];
    let ch1labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    let ch2labels = [];
    let token = localStorage.getItem('token');
    var i;
    let times = 0;
    console.log("about to get data");
    for (i = 0; i < 12; i++) { //
      var s = new Date(myyear, i, 1);
      var e = new Date(myyear, i + 1, 0);
      var formattedDates = moment(s).format('YYYYMMDD');
      var formattedDatee = moment(e).format('YYYYMMDD');
      stationsessions(formattedDates, formattedDatee, token, myid)  //
        .then(json => { //   
          console.log(json.data);  //
          const sessionlist = json.data.SessionsSummaryList; //json.data αντί για example
          sessionlist.forEach(element => {
            if (ch2labels.indexOf(element.PointID) == -1) {
              ch2labels.push(element.PointID);
              ch3data.push(element.PointSessions);
              ch4data.push(element.EnergyDelivered);
            }
            else {
              ch3data[ch2labels.indexOf(element.PointID)] += element.PointSessions;
              ch4data[ch2labels.indexOf(element.PointID)] += element.EnergyDelivered;
            }
          })  //
          var s = new Date(json.data.PeriodFrom);
          var ind = s.getMonth();
          ch1data[ind] = json.data.NumberOfChargingSessions;
          ch2data[ind] = json.data.TotalEnergyDelivered;
          times++;
          console.log(ch2data);
          if (times == 12) {
            console.log(ch2labels);
            if (ch2labels.length != 0) {
              console.log("setting this state");
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
                thereare: true,
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
                chart3Data: {
                  labels: ch2labels,
                  datasets: [
                    {
                      label: 'Earnings',
                      fill: false,
                      lineTension: 0,
                      backgroundColor: 'rgba(75,192,192,1)',
                      borderColor: 'rgba(0,0,0,1)',
                      borderWidth: 2,
                      data: ch3data
                    }
                  ]
                },
                chart4Data: {
                  labels: ch2labels,
                  datasets: [
                    {
                      label: 'Earnings',
                      fill: false,
                      lineTension: 0,
                      backgroundColor: 'rgba(75,192,192,1)',
                      borderColor: 'rgba(0,0,0,1)',
                      borderWidth: 2,
                      data: ch4data
                    }
                  ]
                }
              })
            }
            else {
              this.setState({ thereare: false });
            }
          }
        })//
        .catch(err => {
          if (err.response.status == 402) {
            const sessionlist = err.response.data.SessionsSummaryList; //json.data αντί για example
            sessionlist.forEach(element => {
              if (ch2labels.indexOf(element.PointID) == -1) {
                ch2labels.push(element.PointID);
                ch3data.push(element.PointSessions);
                ch4data.push(element.EnergyDelivered);
              }
              else {
                ch3data[ch2labels.indexOf(element.PointID)] += element.PointSessions;
                ch4data[ch2labels.indexOf(element.PointID)] += element.EnergyDelivered;
              }
            })  //
            var s = new Date(err.response.data.PeriodFrom);
            var ind = s.getMonth();
            ch1data[ind] = err.response.data.NumberOfChargingSessions;
            ch2data[ind] = err.response.data.TotalEnergyDelivered;
            times++;
            console.log(err.response.data);
            console.log(times);
            if (times == 12) {
              console.log(ch2labels);
              if (ch2labels.length != 0) {
                console.log("setting this state");
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
                  chart3Data: {
                    labels: ch2labels,
                    datasets: [
                      {
                        label: 'Earnings',
                        fill: false,
                        lineTension: 0,
                        backgroundColor: 'rgba(75,192,192,1)',
                        borderColor: 'rgba(0,0,0,1)',
                        borderWidth: 2,
                        data: ch3data
                      }
                    ]
                  },
                  chart4Data: {
                    labels: ch2labels,
                    datasets: [
                      {
                        label: 'Earnings',
                        fill: false,
                        lineTension: 0,
                        backgroundColor: 'rgba(75,192,192,1)',
                        borderColor: 'rgba(0,0,0,1)',
                        borderWidth: 2,
                        data: ch4data
                      }
                    ]
                  }
                })
              }
              else {
                this.setState({ thereare: false });

              }
            }
          }
        });
    }
  }

  render() {
    if (this.state.location_id !== "redirect")
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
              <h1>Charts and statistics for charging station {this.state.location_id}</h1>
              <p>
                You have the opportunity to see statistics for the charging sessions done in the charging stations you operate.{this.state.year}
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
                  <Bar
                    data={this.state.chart3Data}
                    options={{
                      title: {
                        display: true,
                        text: 'Sessions per charging point',
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
                  <Bar
                    data={this.state.chart4Data}
                    options={{
                      title: {
                        display: true,
                        text: 'Energy provided per charging point',
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
        <Redirect to="/statistics" />
      );
    }
  }
}
