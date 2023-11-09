<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Store_Manager_Nav @logout="logout()"></Store_Manager_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <div class="row">
                    <h3 class="card-title col">Categories</h3>
                    <button class="btn btn-outline-success btn-lg col-4"
                        @click="$router.push(`/store_manager/add_category`)">Add Category</button>
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
                                        @click="$router.push(`/store_manager/category/${category.id}`)">
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
    import Store_Manager_Nav from "./store_manager_nav"

    export default {
        name: "Store_Manager_Categories",
        components: {
            Un_Authorized,
            Store_Manager_Nav
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
                this.$router.push('/store_manager_login')
            }
        },
        async mounted(){
            let sm_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!sm_id)
            {
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/categories`
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