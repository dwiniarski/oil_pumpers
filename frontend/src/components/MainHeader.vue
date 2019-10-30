<template>
    <header class="masthead mb-auto">
        <div class="inner">
            <h3 class="masthead-brand">
                <router-link :to="{name:'home-view'}">Oil Pumpers</router-link>
            </h3>
            <nav class="nav nav-masthead justify-content-center">
                <router-link :to="{name:'home-view'}" class="nav-link">Log In
                </router-link>
                <router-link :to="{name:'register-view'}" class="nav-link">Register
                </router-link>
                <router-link :to="{name:'contact-view'}" class="nav-link">Contact
                </router-link>
            </nav>
        </div>
    </header>
</template>

<script>
    export default {
        name: "MainHeader"
    }
</script>

<style scoped>

</style>