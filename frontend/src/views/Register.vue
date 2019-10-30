<template>
    <main role="main" class="inner cover">
        <div id="register_screen" v-if="is_register_screen_visible">
            <h1 class="cover-heading">Register</h1>
            <p class="lead">Game where you can build oil empire and become rich or bankrupt. Based on C64 game "Oil
                Pumpers" or "Pompiarze".</p>
            <form class="form-signin">
                <label for="email" class="sr-only">Email address</label>
                <input type="email" id="email" v-model="email" class="form-control" placeholder="Email address" required
                       autofocus>
                <label for="password" class="sr-only">Password</label>
                <input type="password" id="password" v-model="password" class="form-control" placeholder="Password"
                       required>
                <label for="password_confirm" class="sr-only">Password</label>
                <input type="password" id="password_confirm" v-model="password_confirm" class="form-control"
                       placeholder="Password confirmation"
                       required>
                <button class="btn btn-lg btn-primary btn-block" type="button" @click="register">Register</button>
            </form>
        </div>
        <div id="register_success_screen" v-if="is_register_success_screen_visible">
            <h1 class="cover-heading">Your account has been registered!</h1>
            <p class="lead">Please activate your account using instructions we send to your email address.</p>
        </div>
    </main>
</template>

<script>
    import {HANDLE_REGISTER} from "../store/actions";

    export default {
        name: "Register",
        data() {
            return {
                email: '',
                password: '',
                password_confirm: '',
                is_register_screen_visible: true,
                is_register_success_screen_visible: false
            }

        },
        mounted: function () {
            this.is_register_screen_visible = true;
            this.is_register_success_screen_visible = false;
        },
        methods: {
            register: function () {
                this.$store.dispatch(HANDLE_REGISTER, {
                    email: this.email,
                    password: this.password,
                    password_confirm: this.password_confirm
                }).then(() => {
                    this.is_register_screen_visible = false;
                    this.is_register_success_screen_visible = true;
                }).catch(({response}) => {
                    console.log(response.data);
                })
            }
        }
    }
</script>

<style scoped>

</style>