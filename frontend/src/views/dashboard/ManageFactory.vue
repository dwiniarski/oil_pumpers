<template>
    <div>
        <div class="row">
            <div class="col-sm">Factory management</div>
        </div>
        <div class="row">
            <div class="col-2">Name</div>
            <div class="col-sm">{{factory.name}}</div>
        </div>
        <div class="row">
            <div class="col-2">Type</div>
            <div class="col-sm">{{factory.type.human_name}}</div>
        </div>
        <div class="row">
            <div class="col-2">Level</div>
            <div class="col-sm">{{factory.level}}
                <button class="btn btn-sm btn-primary" @click="upgradeLevel">Upgrade</button>
            </div>
        </div>
        <div class="row">
            <div class="col-2">Production rate</div>
            <div class="col-sm">{{factory.production_rate}}</div>
        </div>
        <div class="row">
            <div class="col-2">Units stored</div>
            <div class="col-sm">{{factory.units_stored}}</div>
        </div>
        <div class="row">
            <div class="col-2">Is selling</div>
            <div class="col-sm">{{factory.is_selling}}</div>
        </div>
        <div class="row">
            <div class="col-2">Price per unit</div>
            <div class="col-sm">{{factory.price_per_unit | formatToCurrency}}</div>
        </div>
        <div class="row">
            <div class="col-2">Upkeep cost</div>
            <div class="col-sm">{{factory.upkeep_cost | formatToCurrency}}</div>
        </div>
        <div class="row">
            <div class="col-2">State</div>
            <div class="col-sm">{{factory.state.human_name}}</div>
        </div>
        <div class="row">
            <div class="col-2">Is for sale</div>
            <div class="col-sm">{{factory.is_for_sale}}</div>
        </div>
        <div class="row">
            <div class="col-2">Selling price</div>
            <div class="col-sm">{{factory.selling_price | formatToCurrency}}</div>
        </div>
    </div>

</template>

<script>
    import {FETCH_FACTORY} from "../../store/actions";

    export default {
        name: "ManageFactory",
        data() {
            return {
                factory: {},
            }
        },
        mounted() {
            this.$store.dispatch(FETCH_FACTORY, {'id': this.$route.params.id}).then(
                response => {
                    this.factory = response.data;
                }
            );
        },
        methods: {
            upgradeLevel: function () {
                alert("Updating level");
            }
        }
    }
</script>

<style scoped>

</style>