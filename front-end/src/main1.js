import React from 'react';

class Be extends React.Component{
  constructor(props){
    super(props);
  } 

  render(){
    return(
      <div className="loginformdiv">
        <div className="main1row">
          <div className="buttoncolumn">
            <input type="checkbox" name="Φόρτισε το όχημά σου!"/>
          </div>
          <div className="buttoncolumn">
            <div className="card">
              <h4>Πλήρωσε τον μηνιαίο λογαριασμό!</h4>
            </div>
          </div>
          <div className="buttoncolumn">
            <div className="card">
              <h4>Βρες κοντινούς σταθμούς!</h4>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Be;
