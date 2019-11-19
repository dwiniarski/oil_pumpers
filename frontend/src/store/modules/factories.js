import {
    SET_MY_FACTORIES
} from '../mutations'

import {
    FETCH_FACTORY_TYPES,
    BUILD_FACTORY,
    FETCH_MY_FACTORIES,
    FETCH_FACTORY,
    UPGRADE_FACTORY
} from '../actions'
import {FactoriesService} from "../../common/api.service";

const state = {
    factory_types: '',
    my_factories: ''
}
const getters = {
    myFactories(state) {
        return state.my_factories;
    }
}
const actions = {
    [FETCH_FACTORY_TYPES](context, payload) {
        return FactoriesService.fetchFactoryTypes();
    },
    [BUILD_FACTORY](context, payload) {
        return FactoriesService.buildFactory(payload);
    },
    [FETCH_MY_FACTORIES](context, payload) {
        return FactoriesService.fetchMyFactories().then(
            function (response) {
                context.commit(SET_MY_FACTORIES, response.data);
            });
        ;
    },
    [FETCH_FACTORY](context, payload) {
        return FactoriesService.fetchFactory(payload.id);
    },
    [UPGRADE_FACTORY](context, payload) {
        return FactoriesService.upgradeFactory(payload.id);
    }
}
const mutations = {
    [SET_MY_FACTORIES]: (state, payload) => {
        state.my_factories = payload;
    },
}

export default {
    state,
    actions,
    mutations,
    getters
}
