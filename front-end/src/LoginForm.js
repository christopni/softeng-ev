import React from 'react';
import { userlogin } from './api';
import { UserContext } from './UserContext';
import {Header, Footer} from './HeaderFooter';

class LoginPage extends React.Component{

  static contextType = UserContext;

  constructor(props) {
    super(props);
    this.username = React.createRef();
    this.password = React.createRef();
    this.handleSubmit = this.handleSubmit.bind(this);
}

  handleSubmit(event){
    console.log('ref to username: ', this.username.current);
  
    const u = this.username.current.value;
    const p = this.password.current.value;
    console.log('Submitting...', u, p);
 
    let obj = {
      username: u,
      password: p
    };

    userlogin(obj)
    .then(json => {   
        
        console.log(json);
        
        //store the user's data in local storage
        //to make them available for the next
        //user's visit
        localStorage.setItem('token', json.data.token);
        localStorage.setItem('username', u);
        localStorage.setItem('user', json.data.user);
        
        //use the setUserData function available
        //through the UserContext
        console.log(json.data.user);

        this.context.setUserData(json.data.token, u, json.data.user);
        
        //use the history prop available through
        //the Route to programmatically navigate
        //to another route            
        this.props.history.push('/');
    });

    event.preventDefault();

  }

  render(){
    return(
      <div className="loginformdiv">
        <Header />
        <div className="topnavwannabe">
        </div>

        <div className="row">
          <div className="column left">
            <h2>Login</h2>
            <p>Login in order to watch statistics, find charging station or pay with card!</p>
          </div>
          <div className="column right">
            <form onSubmit={this.handleSubmit}>
              <div className="rowform">
                <input id="username" type="text" ref={this.username} placeholder="Username" required/>
              </div>
              <div className="rowform">
                <input id="password" type="password" ref={this.password} placeholder="Password" required/>
              </div>
              <div className="rowform">
                <button className="" type="submit"> Login </button>
              </div>
            </form>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
}

//                <p>USERNAME</p>
 
export default LoginPage;
