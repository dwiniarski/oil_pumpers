<template>
    <div>
        Manage Oil Field
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