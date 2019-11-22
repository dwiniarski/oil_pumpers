<template>
    <div class="row">
        <table class="table table-hover table-dark">
            <thead>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Type</th>
                <th scope="col">State</th>
                <th scope="col">Level</th>
                <th scope="col">Price per unit</th>
                <th scope="col">Production rate</th>
                <th scope="col">Is selling</th>
                <th scope="col">Units stored</th>
                <th scope="col">Upkeep cost</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="factory in myFactories">
                <td style="min-width: 200px">{{factory.name}}</td>
                <td>{{factory.type.human_name}}</td>
                <td>{{factory.state.human_name}}</td>
                <td>{{factory.level}}</td>
                <td>{{factory.price_per_unit}}</td>
                <td>{{factory.production_rate}}</td>
                <td>{{factory.is_selling}}</td>
                <td>{{factory.units_stored}}</td>
                <td>{{factory.upkeep_cost | formatToCurrency}}</td>
                <td>
                    <router-link class="btn btn-primary btn-sm" href="#"
                                 :to="{name:'dashboard-factories-manage-view', params:{id:factory.id}}">Manage
                    </router-link>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import {FETCH_MY_FACTORIES} from "../../store/actions";

    export default {
        name: "MyFactories",
        computed: {
            ...mapGetters(['myFactories']),
        },
        mounted() {
            this.$store.dispatch(FETCH_MY_FACTORIES);
        }
    }
</script>

<style scoped>

</style>