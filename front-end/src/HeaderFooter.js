import React from 'react';
import green_leaf from './green_leaf.ico'

export class Header extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="header">
        <a href='/'>
          <h1>
            <img src={green_leaf} style={{ width: '40px', height: '40px' }} />
EcoCharge
</h1>
        </a>
      </div>
    );
  }
}

export default Header;

export class Footer extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="footer">
        <div className="info">
          <p>Contact us: Team 50</p>
        </div>
      </div>
    );
  }
}
