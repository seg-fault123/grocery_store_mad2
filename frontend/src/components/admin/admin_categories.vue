<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Admin_Nav @logout="logout()"></Admin_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <div class="row">
                    <h3 class="card-title col">Categories</h3>
                    <button class="btn btn-outline-success btn-lg col" id="add_category"
                        @click="$router.push(`/admin/add_category`)">Add Category</button>
                    <button class="btn btn-outline-info btn-lg col"
                        @click="$router.push(`/admin/category_requests`)">Category Requests</button>
                    <div class="col-1"></div>
                </div>
                <div v-if="empty" class="alert alert-secondary" role="alert">
                    There are no Categories!
                </div>
                <div v-else>
                    <table class="table">
                        <tbody>
                            <tr v-for="category in categories" :key="category.id">
                                <td>
                                    <button class="btn btn-outline-primary btn-lg"
                                        @click="$router.push(`/admin/category/${category.id}`)">
                                            {{ category.name }}
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import Un_Authorized from "../un_authorized"
    import Admin_Nav from "./admin_nav"

    export default {
        name: "Admin_Categories",
        components: {
            Un_Authorized,
            Admin_Nav
        },
        data(){
            return {
                unauthorized: false,
                categories: []
            }
        },
        computed: {
            empty(){
                if (this.categories.length==0)
                {return true}
                return false
            }
        },
        methods: {
            logout(){
                this.$store.commit('reset_data')
                this.$router.push('/admin_login')
            }
        },
        async mounted(){
            let a_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!a_id)
            {
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/admin/${a_id}/categories`
            let resp=await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`
                }
            })
            if (resp.status===401)
            {
                this.unauthorized=true
                return
            }
            let data=await resp.json()
            this.categories=data['categories']
        }
        
    }
</script>

<style scoped>
    #add_category {
        margin-right: 10px;
    }
</style>