<template>
    <main role="main" class="inner cover">
        <h1 class="cover-heading">LOGO</h1>
        <p class="lead">Game where you can build oil empire and become rich or bankrupt. Based on C64 game "Oil
            Pumpers" or "Pompiarze".</p>
        <form class="form-signin">
            <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
            <label for="login_email" class="sr-only">Email address</label>
            <input type="email" id="login_email" class="form-control" v-model="email" placeholder="Email address"
                   required autofocus>
            <label for="login_password" class="sr-only">Password</label>
            <input type="password" id="login_password" class="form-control" v-model="password" placeholder="Password"
                   required>
            <button class="btn btn-lg btn-primary btn-block" type="button" @click="login">Sign in</button>
        </form>
    </main>
</template>

<script>
    import {HANDLE_LOGIN, FETCH_ACCOUNT_DATA} from "../store/actions";

    export default {
        name: "Home",
        data() {
            return {
                email: '',
                password: ''
            }
        },
        methods: {
            login: function () {
                this.$store.dispatch(HANDLE_LOGIN, {
                    email: this.email,
                    password: this.password,
                }).then(() => {
                    this.$store.dispatch(FETCH_ACCOUNT_DATA);
                    this.$router.push({name: 'dashboard-view'});
                }).catch(({response}) => {
                    console.log(response);
                })
            }
        }
    }
</script>

<style scoped>

</style>