import {
    SET_OIL_FIELDS_FOR_SALE,
    SET_MY_OIL_FIELDS
} from '../mutations'

import {
    FETCH_OIL_FIELDS_FOR_SALE,
    BUY_OIL_FIELD,
    FETCH_MY_OIL_FIELDS,
    FETCH_OIL_FIELD,
    CHANGE_OIL_FIELD_NAME
} from '../actions'
import {OilFieldsService} from "../../common/api.service";

const state = {
    oil_fields_for_sale: '',
    my_oil_fields: ''
}
const getters = {
    oilFieldsForSale(state) {
        return state.oil_fields_for_sale;
    },
    myOilFields(state) {
        return state.my_oil_fields;
    }
}
const actions = {
    [FETCH_OIL_FIELDS_FOR_SALE](context) {
        return OilFieldsService.fetchForSale().then(
            function (response) {
                context.commit(SET_OIL_FIELDS_FOR_SALE, response.data);
            });
    },
    [BUY_OIL_FIELD](context, payload) {
        return OilFieldsService.buy(payload.id);
    },
    [FETCH_MY_OIL_FIELDS](context) {
        return OilFieldsService.fetchMyOilFields().then(
            function (response) {
                context.commit(SET_MY_OIL_FIELDS, response.data);
            }
        );
    },
    [FETCH_OIL_FIELD](context, payload) {
        return OilFieldsService.fetchOilField(payload.id);
    },
    [CHANGE_OIL_FIELD_NAME](context, payload) {
        return OilFieldsService.changeName(payload);
    }
}
const mutations = {
    [SET_OIL_FIELDS_FOR_SALE]: (state, payload) => {
        state.oil_fields_for_sale = payload;
    },
    [SET_MY_OIL_FIELDS]: (state, payload) => {
        state.my_oil_fields = payload;
    }
}

export default {
    state,
    actions,
    mutations,
    getters
}
