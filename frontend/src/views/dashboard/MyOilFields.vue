<template>
    <div class="row">
        <table class="table table-hover table-dark">
            <thead>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Amount drills</th>
                <th scope="col">Amount pipes</th>
                <th scope="col">Amount pumps</th>
                <th scope="col">Amount storage tanks</th>
                <th scope="col">Amount wagons</th>
                <th scope="col">Current drilling depth</th>
                <th scope="col">Storage tank consumed</th>
                <th scope="col">Storage tank max.</th>
                <th scope="col">For sale</th>
                <th scope="col">Status</th>
                <th scope="col"></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="oil_field in myOilFields">
                <td style="min-width: 200px">{{oil_field.name}}</td>
                <td>{{oil_field.amount_drills}}</td>
                <td>{{oil_field.amount_pipes}}</td>
                <td>{{oil_field.amount_pumps}}</td>
                <td>{{oil_field.amount_storage_tanks}}</td>
                <td>{{oil_field.amount_wagons}}</td>
                <td>{{oil_field.current_drilling_depth}}</td>
                <td>{{oil_field.storage_tank_consumed_capacity}}</td>
                <td>{{oil_field.storage_tank_max_capacity}}</td>
                <td>{{oil_field.is_for_sale}}</td>
                <td>{{oil_field.status.name}}</td>
                <td>
                    <router-link class="btn btn-primary btn-sm" href="#"
                                 :to="{name:'dashboard-oil-fields-manage-view', params:{id:oil_field.id}}">Manage
                    </router-link>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';
    import {FETCH_MY_OIL_FIELDS} from "../../store/actions";

    export default {
        name: "MyOilFields",
        computed: {
            ...mapGetters(['myOilFields']),
        },
        mounted() {
            this.$store.dispatch(FETCH_MY_OIL_FIELDS);
        }
    }
</script>

<style scoped>

</style>