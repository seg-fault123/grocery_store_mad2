<template>
    <div class="container">
        <Un_Authorized v-if="unauthorized" />
        <div v-else>
            <Admin_Nav @logout="logout()"></Admin_Nav>
            <h1 style="margin-top: 20px;">Welcome Admin</h1>
            <div class="container" id="all_categories">
                <div v-for="category in categories" :key="category.id">
                    <Admin_Category :cat_id="category.id"></Admin_Category>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Un_Authorized from "../un_authorized"
    import Admin_Nav from "./admin_nav"
    import Admin_Category from "./admin_category"

    export default {
        name: "Admin_Home",
        components: {
            Un_Authorized,
            Admin_Nav,
            Admin_Category
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
            this.unauthorized=false
        }
    }
</script>