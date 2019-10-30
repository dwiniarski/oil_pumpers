import axios from 'axios'
import {
    SET_ACCESS_TOKEN,
    SET_REFRESH_TOKEN,
    DELETE_REFRESH_TOKEN,
    DELETE_ACCESS_TOKEN,
    UPDATE_SECONDS_TO_EXPIRE,
    SET_LOGGED_IN, SET_ACCOUNT_DATA
} from '../mutations'

import {
    HANDLE_LOGIN, HANDLE_LOGOUT, CHECK_TOKEN_AFTER_RELOAD, HANDLE_REFRESH_TOKEN, FETCH_ACCOUNT_DATA, HANDLE_REGISTER
} from '../actions'
import {AuthService} from "../../common/api.service";
import router from "../../routes";

const state = {
    logged_in: false,
    seconds_to_expire: '',
    account_data: ''
}
const getters = {
    userId(state) {
        if (localStorage.getItem('access_token')) {
            let info = JSON.parse(atob(localStorage.getItem('access_token').split('.')[1]));
            return info.user_id;
        }
        return {};
    },
    expireTime(state) {
        if (localStorage.getItem('access_token')) {
            var info = JSON.parse(atob(localStorage.getItem('access_token').split('.')[1]));
            return info.exp;
        }
        return {};
    },
    secondsToExpire(state) {
        return state.seconds_to_expire;
    },
    isLoggedIn(state) {
        return state.logged_in
    },
    accountData(state) {
        return state.account_data;
    }
}
const actions = {
    [HANDLE_REGISTER](context, payload) {
        return AuthService.register(payload);
    },
    [HANDLE_LOGIN](context, payload) {
        return AuthService.login(payload).then(
            function (response) {
                context.commit(SET_ACCESS_TOKEN, response.data.access);
                context.commit(SET_REFRESH_TOKEN, response.data.refresh);
                context.commit(SET_LOGGED_IN, true);
                context.commit(UPDATE_SECONDS_TO_EXPIRE);
            })
    },
    [HANDLE_LOGOUT](context, payload) {
        let access_token = localStorage.getItem('access_token');
        let refresh_token = localStorage.getItem('refresh_token');
        context.commit(DELETE_REFRESH_TOKEN, '');
        context.commit(DELETE_ACCESS_TOKEN, '');
        context.commit(SET_LOGGED_IN, false);
        return AuthService.logout(access_token, refresh_token).then(
            function (response) {

            }).catch(function (response) {
        })
    },
    [CHECK_TOKEN_AFTER_RELOAD](context) {
        if (localStorage.getItem('access_token') && localStorage.getItem('refresh_token')) {
            context.commit(SET_LOGGED_IN, true);
        }
    },
    [HANDLE_REFRESH_TOKEN](context, payload) {
        const {refresh_token} = payload;
        return AuthService.refresh(refresh_token);
    },
    [FETCH_ACCOUNT_DATA](context) {
        return AuthService.getAccountData().then(
            function (response) {
                context.commit(SET_ACCOUNT_DATA, response.data);
            });
    }


}
const mutations = {
    [SET_ACCESS_TOKEN]: (state, payload) => {
        localStorage.setItem('access_token', payload)
    },
    [SET_REFRESH_TOKEN]: (state, payload) => {
        localStorage.setItem('refresh_token', payload)
    },
    [UPDATE_SECONDS_TO_EXPIRE]: state => {
        if (state.access_token) {
            var info = JSON.parse(atob(state.access_token.split('.')[1]));
            state.seconds_to_expire = info.exp - (new Date().getTime()) / 1000;
        }
    },
    [SET_LOGGED_IN]: (state, payload) => {
        state.logged_in = payload;
    },
    [DELETE_ACCESS_TOKEN]: (state, payload) => {
        localStorage.removeItem('access_token');
    },
    [DELETE_REFRESH_TOKEN]: (state, payload) => {
        localStorage.removeItem('refresh_token');
    },
    [SET_ACCOUNT_DATA]: (state, payload) => {
        state.account_data = payload;
    }
}

export default {
    state,
    actions,
    mutations,
    getters
}
