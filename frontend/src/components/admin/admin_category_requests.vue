<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Admin_Nav @logout="logout()"></Admin_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <h3 class="card-title">Category Requests</h3>
                <table class="table">
                    <tbody>
                        <tr>
                            <td>
                                <button class="btn btn-outline-primary btn-lg"
                                    @click="$router.push(`/admin/new_category_requests`)">
                                        New Category Requests
                                </button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <button class="btn btn-outline-success btn-lg"
                                    @click="$router.push(`/admin/edit_category_requests`)">
                                        Edit Category Requests
                                </button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <button class="btn btn-outline-danger btn-lg"
                                    @click="$router.push(`/admin/delete_category_requests`)">
                                        Delete Category Requests
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    import Admin_Nav from "./admin_nav"
    import Un_Authorized from "../un_authorized"

    export default {
        name: "Admin_Category_Requests",
        components: {
            Un_Authorized,
            Admin_Nav
        },
        data(){
            return {
                unauthorized: false
            }
        },
        methods: {
            logout(){
                this.$store.commit('reset_data')
                this.$router.push('/admin_login')
            }
        }
    }
</script>