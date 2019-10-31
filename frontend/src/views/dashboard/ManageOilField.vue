<template>
    <div>
        <div class="row">
            <div class="col-sm">
                <table class="table table-striped table-dark table-bordered" style="width:100%">
                    <tbody>
                    <tr>
                        <td>Name</td>
                        <td>{{oil_field.name}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Edit</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Pipes amount</td>
                        <td>{{oil_field.amount_pipes}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Buy</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Pumps amount</td>
                        <td>{{oil_field.amount_pumps}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Buy</button>
                        </td>
                    </tr>

                    <tr>
                        <td>Wagons amount</td>
                        <td>{{oil_field.amount_wagons}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Buy</button>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-sm">
                <table class="table table-striped table-dark table-bordered" style="width:100%">
                    <tbody>
                    <tr>
                        <td>Drills amount</td>
                        <td>{{oil_field.amount_drills}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Buy</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Current drilling depth</td>
                        <td>{{oil_field.current_drilling_depth}}</td>
                        <td>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-sm">
                <table class="table table-striped table-dark table-bordered" style="width:100%">
                    <tbody>
                    <tr>
                        <td>Storage tanks amount</td>
                        <td>{{oil_field.amount_storage_tanks}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Buy</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Consumed capacity</td>
                        <td>{{oil_field.storage_tank_consumed_capacity}}</td>
                        <td>
                        </td>
                    </tr>
                    <tr>
                        <td>Max capacity</td>
                        <td>{{oil_field.storage_tank_max_capacity}}</td>
                        <td>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="row">
            <div class="col-sm">
                <table class="table table-striped table-dark table-bordered" style="width:100%">
                    <tbody>
                    <tr>
                        <td>Status</td>
                        <td>{{oil_field.status.name}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Change</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Is for sale</td>
                        <td>{{oil_field.is_for_sale}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Change</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Selling price</td>
                        <td>{{oil_field.selling_price | formatToCurrency }}</td>
                        <td>
                            <button class="btn btn-primary btn-sm">Change</button>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</template>

<script>
    import {FETCH_OIL_FIELD} from "../../store/actions";

    export default {
        name: "ManageOilField",
        data() {
            return {
                oil_field: ''
            }
        },
        mounted() {
            this.$store.dispatch(FETCH_OIL_FIELD, {'id': this.$route.params.id}).then(
                response => {
                    this.oil_field = response.data;
                }
            );
        }
    }
</script>

<style scoped>

</style>