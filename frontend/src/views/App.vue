<template>
    <div>
        <div v-if="!isLoggedIn" class="cover-container d-flex h-100 p-3 mx-auto flex-column" style="text-align: center">
            <main-header></main-header>
            <router-view></router-view>
            <main-footer></main-footer>
        </div>
        <div v-if="isLoggedIn">
            <dashboard-header></dashboard-header>
            <main role="main" class="container">
                <router-view></router-view>
            </main>
            <dashboard-footer></dashboard-footer>
        </div>
    </div>

</template>

<script>
    import MainHeader from "../components/MainHeader";
    import MainFooter from "../components/MainFooter";
    import DashboardHeader from '../components/DashboardHeader';
    import DashboardFooter from '../components/DashboardFooter';
    import {CHECK_TOKEN_AFTER_RELOAD, FETCH_ACCOUNT_DATA} from '../store/actions'
    import router from '../routes'
    import {mapGetters} from 'vuex';

    export default {
        name: 'app',
        components: {MainHeader, MainFooter, DashboardHeader, DashboardFooter},
        computed: {
            ...mapGetters(['isLoggedIn']),
        },
        mounted() {
            this.$store.dispatch(CHECK_TOKEN_AFTER_RELOAD);
            if (this.isLoggedIn) {
                this.$store.dispatch(FETCH_ACCOUNT_DATA);
                router.push({name: 'dashboard-view'});
            }
        }
    }
</script>

<style src="../assets/css/main.css"></style>
