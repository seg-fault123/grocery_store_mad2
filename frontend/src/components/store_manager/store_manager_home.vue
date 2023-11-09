<template>
    <div class="container">
        <Un_Authorized v-if="unauthorized" />
        <div v-else>
            <Store_Manager_Nav @logout="logout()"></Store_Manager_Nav>
            <h1 style="margin-top: 20px;">Welcome {{ $store.state.first_name }}</h1>
            <div class="container" id="all_categories">
                <div v-for="category in categories" :key="category.id">
                    <Store_Manager_Category :cat_id="category.id"></Store_Manager_Category>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Un_Authorized from "../un_authorized"
    import Store_Manager_Nav from "./store_manager_nav"
    import Store_Manager_Category from "./store_manager_category"

    export default {
        name: "Store_Manager_Home",
        components: {
            Un_Authorized,
            Store_Manager_Nav,
            Store_Manager_Category
        },
        data(){
            return {
                categories: [],
                unauthorized: false
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
            this.unauthorized=false
        }
    }
</script>