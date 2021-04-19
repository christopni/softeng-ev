import React, { Component } from 'react';
import { userlogout } from './api';
import { UserContext } from './UserContext';

export default class Logout extends Component {
    
    static contextType = UserContext;
    
    doLogout() {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('user');
                    
        this.context.setUserData(null, null, null);
        
        this.props.history.push('/');
    }
    
    componentDidMount() {
        //perform an ajax call to logout
        //and then clean up local storage and
        //context state.
        console.log("About to log out");
        userlogout()
        .then(() => {
            console.log("logout");
            this.doLogout();

        });
    }
    
    render() {
        return (<h2>Loggin out...</h2>);
    }
}