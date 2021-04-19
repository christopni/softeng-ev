import React, { Component } from 'react';
import LoginPage from './LoginForm';
import Logout from './Logout';
import './App.css';
import { BrowserRouter, Redirect, Switch, Route } from 'react-router-dom';
import Statistics from './Statistics';
import AnalyticStatistics from './AnalyticStatistics';
import SpecificStats from './SpecificStats';
import SpecificStatsOp from './SpecificStatsOp';
import StatisticsMain from './StatisticsMain';
import StatisticsMainOp from './StatisticsMainOp';
//import {Header, Footer} from './HeaderFooter';
import { UserProvider } from './UserContext';
import UserMain from './UserMain';
//import ProviderMain from './ProviderMain';
import OperatorMain from './OperatorMain';
import MonthlyBill from './MonthlyBill';
import PaymentResult from './PaymentResult';
import Error from './Error';
import Error2 from './Error2';
import Error3 from './Error3';
import ChargeFirst from './ChargeFirst';
import ChargeSecond from './ChargeSecond';
import ChargeThird from './ChargeThird';
import ProgramSelect from './ProgramSelect';
import PriceSelect from './PriceSelect';
import Pay from './Pay';
import ManageStations from './ManageStations';

import AddLocationOfStations from './AddLocationOfStations';
import ChooseLocation from './ChooseLocation';
import UpdateLocationOfStations from './UpdateLocationOfStations';
import AddPointChooseProvider from './AddPointChooseProvider';
import ManagePoints from './ManagePoints';
import AddPoint from './AddPoint';
import UpdatePoint from './UpdatePoint';
import UpdatePointChooseProvider from './UpdatePointChooseProvider';
import UpdatePointChoosePoint from './UpdatePointChoosePoint';
import ShowMap from './ShowMap';
import DeletePoint from './DeletePoint';
import DeletePointChoosePoint from './DeletePointChoosePoint';
import SuccessManageStation from './SuccessManageStation';
import FailManageStation from './FailManageStation';
import SuccessManageLocation from './SuccessManageLocation';
import FailManageLocation from './FailManageLocation';
import ProfileOp from './ProfileOp';
import ProfileCarO from './ProfileCarO';
import ProfileEP from './ProfileEP';
import MapChooseRegion from './MapChooseRegion';



class App extends React.Component{
  constructor(props) {
    super(props)
    this.state = {
      token: props.userData.token,
      username: props.userData.username,
      user: props.userData.user,
      setUserData: (token, username, user) => this.setState({
        token: token,
        username: username,
        user: user
      }),
    };
  }
  
  changestate = (event) => {
    this.setState({username: event.target.value});
  }

  renderProtectedComponent(ProtectedComponent) {
    if (this.state.username !== null) {
      return  (props) => <ProtectedComponent {...props} />;
    }
    else {
      return (props) => <Redirect to='/' />;
    }
  }

  render(){
    return(
      <UserProvider value={this.state}>
        <BrowserRouter>
            {this.state.token ? (
              this.state.user == 'CarOwner' ? 
                <>
                <Switch>
                  <Route exact path="/" component={UserMain}/>
                  <Route exact path="/charge" component={ChargeFirst}/>
                  <Route exact path="/monthlybill" component={MonthlyBill}/>
                  <Route exact path="/logout" component={Logout}/>
                  <Route exact path="/paymentresult" component={PaymentResult}/>  
                  <Route exact path="/chargesecond" render={(props) => <ChargeSecond {...props}/>}/> 
                  <Route exact path="/chargethird" render={(props) => <ChargeThird {...props}/>}/> 
                  <Route exact path="/programselect" render={(props) => <ProgramSelect {...props}/>}/> 
                  <Route exact path="/priceselect" render={(props) => <PriceSelect {...props}/>}/> 
                  <Route exact path="/pay" render={(props) => <Pay {...props}/>}/> 

                  <Route exact path="/mapchooseregion" component={MapChooseRegion}/>
                  <Route exact path="/showmap" render={(props) => <ShowMap {...props}/>}/>
                  <Route exact path="/profile" component={ProfileCarO}/>
                  <Route path="*" component={Error}/> 

                  </Switch>             
                </>
                :(this.state.user == 'EnergyProviders' ?
                    <>
                    <Switch>
                      <Route exact path="/" component={StatisticsMain}/>
                      <Route exact path="/statistics" component={Statistics}/>
                      <Route exact path="/specificpoint" component={AnalyticStatistics}/>
                      <Route exact path="/specificstats" render={(props) => <SpecificStats {...props}/>}/>
                      <Route exact path="/logout" component={Logout}/>

                      <Route exact path="/profile" component={ProfileEP}/>
                      <Route path="*" component={Error2} />  
         
                      </Switch>      
                    </> :
                    <>
                    <Switch>
                      <Route exact path="/" component={OperatorMain}/>
                      <Route exact path="/statistics" component={StatisticsMainOp}/>
                      <Route exact path="/logout" component={Logout}/>
                      <Route exact path="/specificstats" render={(props) => <SpecificStatsOp {...props}/>}/>
                      <Route exact path="/managestations" component={ManageStations}/>

                      <Route exact path="/profile" component={ProfileOp}/>
                      <Route exact path="/successmanagestation" component={SuccessManageStation}/>
                      <Route exact path="/failmanagestation" component={FailManageStation}/>
                      <Route exact path="/successmanagelocation" component={SuccessManageLocation}/>
                      <Route exact path="/failmanagelocation" component={FailManageLocation}/>
                      <Route exact path="/addlocationofstations" component={AddLocationOfStations}/>
                      <Route exact path="/updatelocationofstations" render={(props) => <UpdateLocationOfStations {...props}/>}/>
                      <Route exact path="/chooselocation" component={ChooseLocation}/>
                      <Route exact path="/managepoints" component={ManagePoints}/>
                      <Route exact path="/addpoint" component={AddPoint}/>
                      <Route exact path="/addpointchooseprovider" render={(props) => <AddPointChooseProvider {...props}/>}/>
                      <Route exact path="/updatepoint" component={UpdatePoint}/>
                      <Route exact path="/updatepointchoosepoint" render={(props) => <UpdatePointChoosePoint {...props}/>}/>
                      <Route exact path="/updatepointchooseprovider" render={(props) => <UpdatePointChooseProvider {...props}/>}/>
                      <Route exact path="/deletepoint" component={DeletePoint}/>
                      <Route exact path="/deletepointchoosepoint" render={(props) => <DeletePointChoosePoint {...props}/>}/>
                      <Route path="*" component={Error3} />    
                      </Switch>           
                    </> 
              )):
              <>
              <Switch>
                <Route path="/" component={LoginPage}/>
                </Switch>
              </>
            }
        </BrowserRouter>
      </UserProvider>
    );
  }
}
/*
        <Switch>
          <Route path = "/" exact component = {LoginPage} />
          <Route path="/main" render = {this.renderProtectedComponent(Be)} />   




    <BrowserRouter>
      <Switch>
        <Route path="/" exact>
          <App userData={userData}/>
        </Route>
        <Route path="/ok">
          <Be />
        </Route>
      </Switch>
    </BrowserRouter>
*/

export default App;

//                      <Route exact path= "/monthlybill" component={MonthlyBill}/>
