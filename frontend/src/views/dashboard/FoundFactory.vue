<template>
    <div>
        <h2>Found a factory</h2>
        <h3>Please select type</h3>
        <div class="row">
            <div class="col-4">
                <div class="list-group" id="factory-types-list" role="tablist">
                    <a v-for="factory_type in factory_types" class="list-group-item list-group-item-action"
                       id="list-home-list" data-toggle="list"
                       href="#list-home" role="tab" aria-controls="home"
                       @click="selectFactoryType(factory_type)">{{factory_type.human_name}}</a>
                </div>
            </div>
            <div class="col-8">
                <div class="tab-content" id="nav-tabContent">
                    <div class="tab-pane fade show active" role="tabpanel"
                         aria-labelledby="list-home-list">
                        <div class="row">
                            <p>
                                {{selected_factory_type.description}}
                            </p>
                        </div>
                        <div class="row">
                            Build cost: {{selected_factory_type.build_cost | formatToCurrency}}
                        </div>
                        <div class="row">
                            Upkeep cost: {{selected_factory_type.base_upkeep_cost | formatToCurrency}}
                        </div>
                        <div class="row">
                            Base production on Level 1: {{selected_factory_type.base_production_rate}}
                        </div>
                    </div>

                </div>
            </div>
        </div>
        <div class="row" style="padding-top: 20px">
            <div class="col-12">
                Factory name: <input type="text" v-model="factory_form.name"/>
            </div>
            <div class="col-12">
                Setup price per unit: <input type="text" v-model="factory_form.unit_price"/>$
            </div>
            <div class="col-12">
                Start production when build:
                <div class="form-check">
                    <input class="form-check-input" type="checkbox"
                           v-model="factory_form.start_production_when_build" id="start_production_checkbox"/>
                    <label class="form-check-label" for="start_production_checkbox">
                        {{factory_form.start_production_when_build}}
                    </label>
                </div>
            </div>
        </div>
        <div class="row">
            <button class="btn btn-secondary btn-success" @click="build">Build</button>
        </div>
    </div>

</template>

<script>
    import {FETCH_FACTORY_TYPES, BUILD_FACTORY, FETCH_ACCOUNT_DATA} from "../../store/actions";

    export default {
        name: "FoundFactory",
        mounted() {
            this.$store.dispatch(FETCH_FACTORY_TYPES).then(response => {
                this.factory_types = response.data;
                this.selected_factory_type = this.factory_types[0];
            });
        },
        data() {
            return {
                selected_factory_type: '',
                factory_form: {
                    unit_price: '',
                    start_production_when_build: true,
                    name: ''
                },
                factory_types: ''
            }
        },
        methods: {
            selectFactoryType: function (factory_type) {
                this.selected_factory_type = factory_type;
            },
            build: function () {
                this.factory_form.factory_type_id = this.selected_factory_type.id;
                this.$store.dispatch(BUILD_FACTORY,this.factory_form).then(response => {
                    this.$store.dispatch(FETCH_ACCOUNT_DATA);
                    alert('Factory has been build.');
                }).catch(error => {alert(error)});
            }
        }
    }
</script>

<style scoped>

</style>