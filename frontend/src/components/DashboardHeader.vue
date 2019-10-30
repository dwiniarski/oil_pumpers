<template>
    <header>
        <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
            <a class="navbar-brand" href="#">---</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault"
                    aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item dropdown active">
                        <a class="nav-link dropdown-toggle" href="#" id="manage_dropdown"
                           data-toggle="dropdown"
                           aria-haspopup="true" aria-expanded="false">Manage</a>
                        <div class="dropdown-menu" aria-labelledby="manage_dropdown">
                            <router-link :to="{name:'dashboard-oil-fields-view'}" class="dropdown-item">Oil fields
                            </router-link>
                            <router-link :to="{name:'dashboard-factories-view'}" class="dropdown-item">Factories
                            </router-link>
                        </div>
                    </li>
                    <li class="nav-item dropdown active">
                        <a class="nav-link dropdown-toggle" href="#" id="buy_dropdown"
                           data-toggle="dropdown"
                           aria-haspopup="true" aria-expanded="false">Buy</a>
                        <div class="dropdown-menu" aria-labelledby="buy_dropdown">
                            <router-link :to="{name:'dashboard-buy-oil-field-view'}" class="dropdown-item">Oil field
                            </router-link>
                            <router-link :to="{name:'dashboard-buy-factory-view'}" class="dropdown-item">Factory
                            </router-link>
                        </div>
                    </li>
                    <li class="nav-item active">
                        <router-link :to="{name:'dashboard-rank-view'}" class="nav-link">Ranks</router-link>
                    </li>
                    <li class="nav-item active">
                        <router-link :to="{name:'dashboard-sabotage-view'}" class="nav-link">Sabotage</router-link>
                    </li>
                </ul>
                <div class="my-2 my-lg-0">
                    <span>Logged in as: {{accountData.email}}</span>
                    <span>Money: {{accountData.cash_total | formatToCurrency}}$</span>
                    <span>Date: 2000-01-01</span>
                    <a href="#" @click="logout">Logout</a>
                </div>
            </div>
        </nav>
    </header>

</template>

<script>
    import {mapGetters} from 'vuex';
    import {HANDLE_LOGOUT} from "../store/actions";

    export default {
        name: "DashboardHeader",
        computed: {
            ...mapGetters(['accountData']),
        },
        methods: {
            logout: function () {
                this.$store.dispatch(HANDLE_LOGOUT).then(() => {
                    this.$router.push({name: 'home-view'});
                }).catch(({response}) => {
                    console.log(response);
                })
            }
        }
    }
</script>

<style scoped>

</style>