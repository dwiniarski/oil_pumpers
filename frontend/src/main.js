import Vue from 'vue'
import App from './views/App.vue'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import VueRouter from 'vue-router'
import router from './routes'
import store from "./store";
import ApiService from './common/api.service'

Vue.use(VueRouter);

ApiService.init();

Vue.filter('formatToCurrency', function (value) {
    if (typeof value !== "number") {
        return value;
    }
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    });
    return formatter.format(value);
});

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})
