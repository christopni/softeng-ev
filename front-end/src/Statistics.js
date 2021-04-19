import React from 'react';
import { energysessions, stationsprovide } from './api';
import { Bar, Line, Pie } from 'react-chartjs-2';
import example from './example';
import { Header, Footer } from './HeaderFooter';
import { UserContext } from './UserContext';



export default class Statistics extends React.Component {

  static contextType = UserContext;

  constructor(props) {
    super(props);
    this.state = {
      chart1Data: {},
      chart2Data: {},
      chart3Data: {},
      chart4Data: {},
      chart5Data: {},
      chart6Data: {},
      chart7Data: {},
      thereare: true,
      year: 2021
    }
    this.changeyear = this.changeyear.bind(this);
    this.getChartData = this.getChartData.bind(this);
  }

  componentDidMount() {
    //   this.state.year = 2021;
    console.log("what im doin");
    this.getChartData(this.state.year);
  }

  changeyear(event) {
    this.setState({ year: event.target.value });
    this.getChartData(event.target.value);
  }


  getChartData(myyear) {
    console.log("getting new data");
    let ch1labels = [];
    let ch2labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    let ch3labels = ["Slow", "Fast"];
    let ch1data = [];
    let ch3data = [];
    let ch7data = [];
    let ch2data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let ch4data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let ch6data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    let ch5data = [0, 0];
    //    var i;
    //        for(i=0; i < 11; i++){ //
    //          var s = new Date(this.year, i, 1);
    //          var e = new Date(this.year, i + 1, 0);
    //    var s = new Date(2018, 4, 3);
    stationsprovide(this.context.token)
      .then(json1 => {
        console.log(json1.data);
        energysessions(myyear + "0101", myyear + "1231", this.context.token, json1.data.EnergyProviderID)  //
          .then(json => { //   

            console.log(json);  //

            const sessionlist = json.data.ProviderChargingSessionsList; //json αντί για example
            //        let ch1labels = [];
            //        let ch1data = [];
            sessionlist.forEach(element => {
              if (ch1labels.indexOf(element.StationID) == -1) {
                ch1labels.push(element.StationID);
                ch1data.push(1);
                ch3data.push(element.TotalCost);
                ch7data.push(element.EnergyDelivered);
              }
              else {
                ch1data[ch1labels.indexOf(element.StationID)]++;
                ch3data[ch1labels.indexOf(element.StationID)] += element.TotalCost;
                ch7data[ch1labels.indexOf(element.StationID)] += element.EnergyDelivered;
                console.log(ch1data[ch1labels.indexOf(element.StationID)]);
              }
              let m = new Date(element.FinishedOn);
              ch2data[m.getMonth()]++;
              ch4data[m.getMonth()] += element.TotalCost;
              ch6data[m.getMonth()] += element.EnergyDelivered;
              element.PricePolicyRef == "fast" ?
                ch5data[1]++ :
                ch5data[0]++;

              //                ch2data[i]++;
              //                ch4data[i]+=element.TotalCost;
            })  //
            //        } //    
            this.setState({
              chart1Data: {
                labels: ch1labels,
                datasets: [
                  {
                    label: 'Sessions',
                    fill: false,
                    lineTension: 0,
                    backgroundColor: 'rgb(86, 179, 255)',
                    borderColor: 'rgba(0,0,0,1)',
                    borderWidth: 2,
                    data: ch1data
                  }
                ]
              },
              chart3Data: {
                labels: ch1labels,
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
              chart2Data: {
                labels: ch2labels,
                datasets: [
                  {
                    label: 'Sessions',
                    fill: false,
                    lineTension: 0,
                    backgroundColor: 'rgba(75,192,192,1)',
                    borderColor: 'rgba(0,0,0,1)',
                    borderWidth: 2,
                    data: ch2data
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
              },
              chart5Data: {
                labels: ch3labels,
                datasets: [
                  {
                    label: 'Earnings',
                    fill: false,
                    lineTension: 0,
                    backgroundColor: ['rgb(86, 179, 255)', 'rgb(250, 129, 130)'],
                    borderColor: 'rgba(0,0,0,1)',
                    borderWidth: 2,
                    data: ch5data
                  }
                ]
              },
              chart6Data: {
                labels: ch2labels,
                datasets: [
                  {
                    label: 'Energy Delivered',
                    fill: false,
                    lineTension: 0,
                    backgroundColor: 'rgba(75,192,192,1)',
                    borderColor: 'rgba(0,0,0,1)',
                    borderWidth: 2,
                    data: ch6data
                  }
                ]
              },
              chart7Data: {
                labels: ch1labels,
                datasets: [
                  {
                    label: 'Energy Delivered',
                    fill: false,
                    lineTension: 0,
                    backgroundColor: 'rgba(75,192,192,1)',
                    borderColor: 'rgba(0,0,0,1)',
                    borderWidth: 2,
                    data: ch7data
                  }
                ]
              },
              thereare: true
            })
          })
          .catch(err => {
            if (err.response.status == 402) {
              this.setState({ thereare: false });
            }
          });
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
                      text: 'Earnings per charging point',
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
                      text: 'Earnings per month',
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
                  data={this.state.chart7Data}
                  options={{
                    title: {
                      display: true,
                      text: 'Energy delivered per charging point',
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
                  data={this.state.chart6Data}
                  options={{
                    title: {
                      display: true,
                      text: 'Energy delivered per month',
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
                  data={this.state.chart5Data}
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
  }
}
