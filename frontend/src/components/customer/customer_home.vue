<template>
    <div class="container">
        <Un_Authorized v-if="unauthorized" />
        <div v-else>
            <Customer_Nav @logout="logout()"></Customer_Nav>
            <h1 style="margin-top: 20px;">Welcome {{ $store.state.first_name }}</h1>
            <div class="container" id="all_categories">
                <div v-for="category in categories" :key="category">
                    <Customer_Category :cat_id="category"></Customer_Category>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Un_Authorized from "../un_authorized"
    import Customer_Nav from "./customer_nav"
    import Customer_Category from "./customer_category"

    export default {
        name: "Customer_Home",
        components: {
            Un_Authorized,
            Customer_Nav,
            Customer_Category
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
                this.$router.push('/customer_login')
            }
        },  
        async mounted(){
            let c_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!c_id)
            {
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/home`
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