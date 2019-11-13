import Vue from "vue";
import Vuex from "vuex";

import auth from "./modules/auth";
import oil_fields from "./modules/oil_fields"
import factories from "./modules/factories"

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        auth: auth,
        oil_fields: oil_fields,
        factories: factories
    }
});
