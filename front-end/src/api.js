//import qs from "qs";
import axios from "axios";
import config from "./config";
import { UserContext } from './UserContext';

axios.defaults.baseURL = config.apiUrl;

//static contextType = UserContext;

export const userlogin = (obj) => {
    const requestUrl = "login/?username=" + obj.username + "&password=" + obj.password;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
            //            'Access-Control-Allow-Origin': 'http://localhost:3000'
            //            'X-OBSERVATORY-AUTH': token;
        }
    }
    //    return axios.post(requestUrl, JSON.stringify(obj), requestOptions);
    return axios.post(requestUrl, null, requestOptions);
}

export const userlogout = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "logout/";
    const requestHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Token ' + token
    }
    //    return axios.post(requestUrl, qs.stringify(obj), requestOptions);
    return axios({ method: 'post', url: requestUrl, headers: requestHeaders });
}

export const energysessions = (from, to, token, id) => {
    //    let token = localStorage.getItem('token');
    //    console.log(token)
    const requestUrl = "SessionsPerProvider/" + id + "/" + from + "/" + to;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const pointsessions = (from, to, token, id) => {
    //    let token = localStorage.getItem('token');
    //    console.log(token)
    const requestUrl = "SessionsPerPoint/" + id + "/" + from + "/" + to;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const stationsprovide = (token) => {
    //    let token = localStorage.getItem('token');
    //    console.log(token)
    const requestUrl = "statistics/provider/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const locationsoperate = (token) => {
    //    let token = localStorage.getItem('token');
    //    console.log(token)
    const requestUrl = "statistics/operator/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}


export const stationsessions = (from, to, token, id) => {
    //    let token = localStorage.getItem('token');
    //    console.log(token)
    const requestUrl = "SessionsPerStation/" + id + "/" + from + "/" + to;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const unpaidbills = (token) => {
    const requestUrl = "carowner/monthly_charges/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const paymonth = (id, token) => {
    const requestUrl = "carowner/payment_verification/?id=" + id;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    //    return axios.post(requestUrl, JSON.stringify(obj), requestOptions);
    return axios.post(requestUrl, null, requestOptions);
}



export const getregionslist = (token) => {
    const requestUrl = "carowner/all_locations/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}


export const getlocationslist = (region, token) => {
    var d = new Date();
    const requestUrl = "carowner/specificlocations/?address_region=" + region + "&time=" + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const getpointslist = (location, token) => {
    const requestUrl = "carowner/available_points/?location_id=" + location;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const getusertype = (token) => {
    const requestUrl = "carowner/if_monthly_charges/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.get(requestUrl, requestOptions);
}



export const paymentverif = (token, method, protocol, energy_amount, amount, station) => {
    let url = '';
    if (method == "monthly") {
        url = "carowner/chargepayverified/?protocol=" + protocol + "&energy_amount=" + energy_amount + "&amount=" + amount + "&station=" + station;
    }
    else {
        console.log(protocol);
        url = "carowner/chargepayverified/?method=" + method + "&protocol=" + protocol + "&energy_amount=" + energy_amount + "&amount=" + amount + "&station=" + station;
    }
    const requestUrl = url
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token
        }
    }
    return axios.post(requestUrl, null, requestOptions);
}

export const addlocation = (obj) => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/location/insert/?address="+obj.address+"&addresspostalcode="+obj.address_postal_code+"&addressregion="+obj.address_region+"&phone="+obj.phone+"&openhour="+obj.open_hour+"&closehour="+obj.close_hour;
    const requestHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Token ' + token 
    }
    return axios({method: 'post', url: requestUrl, headers: requestHeaders});
}

export const updatelocation = (obj) => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/location/update/?locationid="+obj.location_id+"&phone="+obj.phone+"&openhour="+obj.open_hour+"&closehour="+obj.close_hour;
    const requestHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Token ' + token 
    }
    return axios({method: 'post', url: requestUrl, headers: requestHeaders});
}

export const displaylocations = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/location/details/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const displayproviders = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/station/energyproviders/details/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const addpointt = (locid,idd) => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/station/insert/?locationid="+locid+"&providerid="+idd;
    const requestHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Token ' + token 
    }
    return axios({method: 'post', url: requestUrl, headers: requestHeaders});
}

export const updatepointt = (locid,idd) => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/station/update/?stationid="+locid+"&providerid="+idd;
    const requestHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Token ' + token 
    }
    return axios({method: 'post', url: requestUrl, headers: requestHeaders});
}

export const displayregions = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "carowner/all_locations/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const displaycoordinates = (adrreg) => {
    let token = localStorage.getItem('token');
    const requestUrl = "carowner/specificlocations/?address_region="+adrreg;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const displaypoints = (locid) => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/location_points/?location_id="+locid;
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const deletepointt = (locid,idd) => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/station/delete/?stationid="+locid;
    const requestHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Token ' + token 
    }
    return axios({method: 'post', url: requestUrl, headers: requestHeaders});
}

export const displayinfoop = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "operator/elements/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const displayinfocar = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "carowner/elements/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}

export const displayinfoep = () => {
    let token = localStorage.getItem('token');
    const requestUrl = "energyprovider/elements/";
    const requestOptions = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Token ' + token 
        }
    }
    return axios.get(requestUrl, requestOptions);
}