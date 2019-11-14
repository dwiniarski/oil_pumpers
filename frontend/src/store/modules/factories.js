import {} from '../mutations'

import {
    FETCH_FACTORY_TYPES,
    BUILD_FACTORY
} from '../actions'
import {FactoriesService} from "../../common/api.service";

const state = {
    factory_types: ''
}
const getters = {}
const actions = {
    [FETCH_FACTORY_TYPES](context, payload) {
        return FactoriesService.fetchFactoryTypes();
    },
    [BUILD_FACTORY](context, payload) {
        return FactoriesService.buildFactory(payload);
    }
}
const mutations = {}

export default {
    state,
    actions,
    mutations,
    getters
}
