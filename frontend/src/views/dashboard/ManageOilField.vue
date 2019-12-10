<template>
    <div>
        <div class="row">
            <div class="col-sm">
                <table class="table table-striped table-dark table-bordered" style="width:100%">
                    <tbody>
                    <tr>
                        <td>Name</td>
                        <td v-if="isNameEditable">
                            <input type="text" class="form-control" v-model="oil_field.name"/>
                        </td>
                        <td v-if="!isNameEditable">{{oil_field.name}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" v-if="isNameEditable" @click="saveName">Save</button>
                            <button class="btn btn-primary btn-sm" v-if="!isNameEditable" @click="editName">Edit
                            </button>
                        </td>
                    </tr>
                    <tr>
                        <td>Pipes amount</td>
                        <td>{{oil_field.amount_pipes}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="showSuppliersList('pipes')">Buy</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Pumps amount</td>
                        <td>{{oil_field.amount_pumps}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="showSuppliersList('pumps')">Buy</button>
                        </td>
                    </tr>

                    <tr>
                        <td>Wagons amount</td>
                        <td>{{oil_field.amount_wagons}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="showSuppliersList('wagons')">Buy</button>
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
                        <td>Drills amount</td>
                        <td>{{oil_field.amount_drills}}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="showSuppliersList('drills')">Buy</button>
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
        <div class="row" style="padding-top: 15px; padding-bottom: 15px">
            <div class="col-2" v-if="(oil_field.status.name == 'IDLE') && (oil_field.amount_drills > 0)">
                <button class="btn btn-success">Start drilling</button>
            </div>
            <div class="col-2" v-if="oil_field.status.name == 'DRILLING'">
                <button class="btn btn-danger">Stop drilling</button>
            </div>
            <div class="col-2" v-if="oil_field.status.name == 'FLOWING'">
                <button class="btn btn-success">Start pumping</button>
            </div>
            <div class="col-2" v-if="oil_field.status.name == 'PUMPING'">
                <button class="btn btn-danger">Stop pumping</button>
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
                        <td v-if="!isForSaleEditable">{{oil_field.is_for_sale}}</td>
                        <td v-if="isForSaleEditable">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox"
                                       v-model="oil_field.is_for_sale" id="is_for_sale_checkbox"/>
                                <label class="form-check-label" for="is_for_sale_checkbox">
                                    {{oil_field.is_for_sale}}
                                </label>
                            </div>
                        </td>
                        <td>
                            <button class="btn btn-primary btn-sm" v-if="!isForSaleEditable" @click="editForSale">
                                Change
                            </button>
                            <button class="btn btn-primary btn-sm" v-if="isForSaleEditable" @click="saveIsForSale">
                                Save
                            </button>
                        </td>
                    </tr>
                    <tr>
                        <td>Selling price</td>
                        <td v-if="!isPriceEditable">{{oil_field.selling_price| formatToCurrency }}</td>
                        <td v-if="isPriceEditable"><input type="text" class="form-control"
                                                          v-model="oil_field.selling_price"/></td>
                        <td>
                            <button v-if="!isPriceEditable" class="btn btn-primary btn-sm" @click="editPrice">Change
                            </button>
                            <button v-if="isPriceEditable" class="btn btn-primary btn-sm" @click="savePrice">Save
                            </button>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="modal fade" id="buyModal" tabindex="-1" role="dialog" aria-labelledby="buyModalLabel"
             aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content dark-modal">
                    <div class="modal-header">
                        <h5 class="modal-title">Modal title</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <table class="table table-hover table-dark">
                                <thead>
                                <tr>
                                    <th scope="col">Name</th>
                                    <th scope="col">Units in store</th>
                                    <th scope="col">Price per unit</th>
                                    <th scope="col"></th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="factory in product_suppliers_list">
                                    <td style="min-width: 200px">{{factory.name}}</td>
                                    <td>{{factory.units_stored}}</td>
                                    <td>{{factory.price_per_unit | formatToCurrency}}</td>
                                    <td>
                                        <button type="button" class="btn btn-primary"
                                                @click="specifyAmount(factory.id, factory.price_per_unit, factory.units_stored, factory.name)">
                                            Select
                                        </button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="row" v-if="specify_amount_box_visible">
                            <div class="col-12">
                                <form>
                                    <div class="form-control">
                                        <label>Enter amount:</label>
                                        <input type="number" v-model.number="buy_list.order[0].amount"
                                               :min="spinner_min"
                                               :max="spinner_max"/>
                                        <span>Total:</span> {{totalSupplierOrder | formatToCurrency}}
                                        <button type="button" class="btn btn-success" @click="buyFromSupplier">Buy
                                        </button>
                                        from {{factory_name}}
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>

    </div>

</template>

<script>
    import {
        FETCH_OIL_FIELD,
        CHANGE_OIL_FIELD_NAME,
        CHANGE_OIL_FIELD_SELLING_PRICE,
        CHANGE_OIL_FIELD_IS_FOR_SALE, FETCH_PRODUCT_SUPPLIERS_LIST, BUY_PRODUCTS_FROM_SUPPLIERS
    } from "../../store/actions";

    import JQuery from 'jquery'

    let $ = JQuery

    export default {
        name: "ManageOilField",
        data() {
            return {
                oil_field: {'status': {'name': ''}, 'selling_price': ''},
                is_name_being_edited: false,
                is_price_being_edited: false,
                is_for_sale_being_edited: false,
                product_suppliers_list: {},
                buy_list: {
                    oil_field_id: 0,
                    order: [{
                        factory_id: 0,
                        amount: 0,
                        price: 0
                    }]
                },
                spinner_min: 1,
                spinner_max: 1,
                specify_amount_box_visible: false,
                factory_name: ''
            }
        },
        mounted() {
            this.$store.dispatch(FETCH_OIL_FIELD, {'id': this.$route.params.id}).then(
                response => {
                    this.oil_field = response.data;
                    this.buy_list.oil_field_id = this.oil_field.id;
                }
            );
        },
        computed: {
            isNameEditable: function () {
                return this.is_name_being_edited;
            },
            isPriceEditable: function () {
                return this.is_price_being_edited;
            },
            isForSaleEditable: function () {
                return this.is_for_sale_being_edited;
            },
            totalSupplierOrder: function () {
                return this.buy_list.order[0].amount * this.buy_list.order[0].price;
            }
        },
        methods: {
            editName: function () {
                this.is_name_being_edited = true;
            },
            editPrice: function () {
                this.is_price_being_edited = true;
            },
            editForSale: function () {
                this.is_for_sale_being_edited = true;
            },
            saveName: function () {
                this.$store.dispatch(CHANGE_OIL_FIELD_NAME, {
                    'id': this.oil_field.id,
                    'name': this.oil_field.name
                }).then(
                    this.is_name_being_edited = false
                );
            },
            savePrice: function () {
                this.$store.dispatch(CHANGE_OIL_FIELD_SELLING_PRICE, {
                    'id': this.oil_field.id,
                    'selling_price': this.oil_field.selling_price
                }).then(
                    this.is_price_being_edited = false,
                ).catch(({response}) => {
                    alert(response.data.selling_price);
                });
            },
            saveIsForSale: function () {
                this.$store.dispatch(CHANGE_OIL_FIELD_IS_FOR_SALE, {
                    'id': this.oil_field.id,
                    'is_for_sale': this.oil_field.is_for_sale
                }).then(
                    this.is_for_sale_being_edited = false,
                ).catch(({response}) => {
                    alert(response.data.is_for_sale);
                });
            },
            showSuppliersList: function (type) {
                this.specify_amount_box_visible = false;
                this.$store.dispatch(FETCH_PRODUCT_SUPPLIERS_LIST, {'product_type': type}).then(
                    response => {
                        this.product_suppliers_list = response.data;
                        $('#buyModal').modal('show');
                    }
                ).catch(error => {
                    alert(error.data);
                });
            },
            specifyAmount: function (factory_id, price, max_amount, name) {
                this.buy_list.order[0].factory_id = factory_id;
                this.buy_list.order[0].amount = 1;
                this.buy_list.order[0].price = price;
                this.spinner_max = max_amount;
                this.factory_name = name;
                this.specify_amount_box_visible = true;
            },
            buyFromSupplier: function () {
                this.$store.dispatch(BUY_PRODUCTS_FROM_SUPPLIERS, this.buy_list).then(
                    response => {
                        console.log('bought')
                    }
                ).catch(error => {
                    alert(error.data)
                })
            }
        }
    }
</script>

<style scoped>
    .dark-modal {
        color: #333333;
    }

</style>