import {} from '../mutations'

import {
    FETCH_FACTORY_TYPES
} from '../actions'
import {FactoriesService} from "../../common/api.service";

const state = {
    factory_types: ''
}
const getters = {}
const actions = {
    [FETCH_FACTORY_TYPES](context, payload) {
        return FactoriesService.fetchFactoryTypes();
    }
}
const mutations = {}

export default {
    state,
    actions,
    mutations,
    getters
}
