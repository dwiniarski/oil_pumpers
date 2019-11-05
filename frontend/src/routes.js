import VueRouter from 'vue-router';
import store from "./store";

let routes = [
    {
        path: '/',
        name: 'home-view',
        meta: {
            guest: true
        },
        component: require('./views/Home.vue').default
    },
    {
        path: '/register',
        name: 'register-view',
        meta: {
            guest: true
        },
        component: require('./views/Register.vue').default
    },
    {
        path: '/contact',
        name: 'contact-view',
        meta: {
            guest: true
        },
        component: require('./views/Contact.vue').default
    },
    {
        path: '/dashboard',
        name: 'dashboard-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/Main.vue').default
    },
    {
        path: '/dashboard/buy/factory',
        name: 'dashboard-buy-factory-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/BuyFactory.vue').default
    },
    {
        path: '/dashboard/buy/oil-field',
        name: 'dashboard-buy-oil-field-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/BuyOilField.vue').default
    },
    {
        path: '/dashboard/factories',
        name: 'dashboard-factories-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/MyFactories.vue').default
    },
    {
        path: '/dashboard/oil-fields',
        name: 'dashboard-oil-fields-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/MyOilFields.vue').default
    },
    {
        path: '/dashboard/oil-fields/:id/manage',
        name: 'dashboard-oil-fields-manage-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/ManageOilField').default
    },
    {
        path: '/dashboard/factories/found',
        name: 'dashboard-found-factory-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/FoundFactory.vue').default
    },
    {
        path: '/dashboard/rank',
        name: 'dashboard-rank-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/Rank.vue').default
    },
    {
        path: '/dashboard/sabotage',
        name: 'dashboard-sabotage-view',
        meta: {
            requiresAuth: true
        },
        component: require('./views/dashboard/Sabotage.vue').default
    },
]

const router = new VueRouter({
    routes
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.getters.isLoggedIn) {
            next({
                path: '/',
                params: {nextUrl: to.fullPath}
            })
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router;