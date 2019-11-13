import axios from 'axios'
import {API_URL, DEBUG} from "./config";
import store from "../store";
import router from '../routes'
import {HANDLE_REFRESH_TOKEN, HANDLE_LOGOUT} from "../store/actions"

const ApiService = {
    init() {
        let url = window.location.host;
        let refreshing_token_in_progress = false;
        if (url == 'localhost:8008') {
            axios.defaults.baseURL = API_URL;
        } else {
            axios.defaults.baseURL = "http://" + url + "/api";
        }

        axios.interceptors.request.use(function (config) {
            const token = localStorage.getItem('access_token');
            const refresh_token = localStorage.getItem('refresh_token');
            let is_token_valid = false;
            if (token) {
                let info = JSON.parse(atob(localStorage.getItem('access_token').split('.')[1]));
                let timestamp_now = Date.now() / 1000;
                if (info.exp > timestamp_now) {
                    is_token_valid = true;
                } else {
                    is_token_valid = false;
                }
            } else {
                if (DEBUG) {
                    console.log("There is no token.");
                }
            }

            if (is_token_valid) {
                if (DEBUG) {
                    console.log("Token is valid, adding to header.");
                }
                config.headers.Authorization = `Bearer ${token}`;
            } else if (!is_token_valid && token) {
                if (DEBUG) {
                    console.log("Token is invalid, trying refreshing.");
                }
                if (!refreshing_token_in_progress) {
                    if (DEBUG) {
                        console.log('Refreshing in progress...');
                    }
                    refreshing_token_in_progress = true;
                    store.dispatch(HANDLE_REFRESH_TOKEN, {'refresh_token': refresh_token}).then(
                        function (response) {
                            localStorage.setItem('access_token', response.data.access);
                            if (DEBUG) {
                                console.log('Access token has been refreshed');
                            }
                            refreshing_token_in_progress = false;
                        }).catch(({response}) => {
                        if (DEBUG) {
                            console.log('Error refreshing token...');
                        }
                        if (response.status === 401 && response.data.code == 'token_not_valid' && response.request.responseURL.includes('token/refresh')) {
                            store.dispatch(HANDLE_LOGOUT);
                            if (DEBUG) {
                                console.log('Redirect to login page');
                            }
                            router.push('login-view');
                        }
                        console.log(response);
                    });
                } else {
                    if (DEBUG) {
                        console.log('In the middle of refreshing...');
                    }
                }
            }

            return config;
        }, function (error) {
            return Promise.reject(err);
        });

    }
}

export default ApiService;


export const AuthService = {
    register(payload) {
        return axios.post('/core/register', payload)
    },
    login(payload) {
        return axios.post('/token/', payload)
    },
    refresh(refresh_token) {
        return axios.post('/token/refresh/', {
            refresh: refresh_token,
        })
    },
    logout() {
        return axios.post('/logout')
    },
    getAccountData() {
        return axios.get('/core/account/data');
    }
}

export const OilFieldsService = {
    fetchForSale(payload) {
        return axios.get('/core/oil-fields/for-sale')
    },
    buy(id) {
        return axios.post('/core/oil-fields/' + id + '/buy')
    },
    fetchMyOilFields() {
        return axios.get('/core/account/oil-fields')
    },
    fetchOilField(id) {
        return axios.get('/core/oil-fields/' + id)
    },
    partialUpdate(payload) {
        return axios.patch('/core/oil-fields/' + payload.id, payload)
    }
}

export const FactoriesService = {
    fetchFactoryTypes() {
        return axios.get('/factories/factory-types')
    },
}