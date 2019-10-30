<template>
    <div class="row">
        <table class="table table-hover table-dark">
            <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Selling price</th>
                <th scope="col">Owner</th>
                <th scope="col">Amount drills</th>
                <th scope="col">Amount pipes</th>
                <th scope="col">Amount pumps</th>
                <th scope="col">Amount storage tanks</th>
                <th scope="col">Amount wagons</th>
                <th scope="col">Current drilling depth</th>
                <th scope="col">Storage tank consumed</th>
                <th scope="col">Storage tank max.</th>
                <th scope="col">Status</th>
                <th scope="col"></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="oil_field in oilFieldsForSale">
                <th scope="row">{{oil_field.id}}</th>
                <td>{{oil_field.name}}</td>
                <td>{{oil_field.selling_price | formatToCurrency}}</td>
                <td>{{oil_field.owner}}</td>
                <td>{{oil_field.amount_drills}}</td>
                <td>{{oil_field.amount_pipes}}</td>
                <td>{{oil_field.amount_pumps}}</td>
                <td>{{oil_field.amount_storage_tanks}}</td>
                <td>{{oil_field.amount_wagons}}</td>
                <td>{{oil_field.current_drilling_depth}}</td>
                <td>{{oil_field.storage_tank_consumed_capacity}}</td>
                <td>{{oil_field.status.name}}</td>
                <td>
                    <button class="btn btn-primary btn-sm" @click="buy(oil_field.id)">Buy</button>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import {FETCH_OIL_FIELDS_FOR_SALE, BUY_OIL_FIELD, FETCH_ACCOUNT_DATA} from "../../store/actions";
    import {mapGetters} from 'vuex';

    export default {
        name: "BuyOilField",
        computed: {
            ...mapGetters(['oilFieldsForSale']),
        },
        mounted() {
            this.$store.dispatch(FETCH_OIL_FIELDS_FOR_SALE);
        },
        methods: {
            buy: function (id) {
                if (confirm("Are you sure you want to buy this oil field?")) {
                    this.$store.dispatch(BUY_OIL_FIELD, {'id': id}).then(
                        response => {
                            this.$store.dispatch(FETCH_OIL_FIELDS_FOR_SALE);
                            this.$store.dispatch(FETCH_ACCOUNT_DATA);
                            alert("Oil field successfuly bought.")
                        }
                    ).catch(error => {
                        alert(error);
                    });
                }

            }
        }
    }
</script>

<style scoped>

</style>