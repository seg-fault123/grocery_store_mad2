<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
    <div v-else>
        <Store_Manager_Nav v-if="home===false" @logout="logout()"></Store_Manager_Nav>
        <div v-if="home===false" style="margin: 20px;"></div>
        <div class="card" :id="p_id">
            <div class="card-body">
                <h5 class="card-title"><b>{{ name }}</b></h5>
                <p class="card-text"><b>Description : </b>{{ description }}</p>
                <p class="card-text"><b>Rate : </b>{{ price }} {{ unit_measure }}</p>
                <p class="card-text" v-if="mfg_date"><b>Mfg Date : </b>{{ mfg_date }}</p>
                <p class="card-text" v-if="exp_date"><b>Exp Date : </b>{{ exp_date }}</p>
                <p class="card-text"><b>Category : </b>{{ category }}</p>
                <div v-if="home===false">
                    <p class="card-text"><b>Stock : </b>{{ stock }}</p>
                    <p class="card-text"><b>Units Sold : </b>{{ units_sold }}</p>
                    <button class="btn btn-outline-primary" id="edit"
                        @click="$router.push(`/store_manager/edit_product/${p_id}`)">Edit</button>
                    <button class="btn btn-outline-danger" id="delete"
                        @click="remove()">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Store_Manager_Nav from "./store_manager_nav"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"

    export default {
        name: 'Store_Manager_Product',
        props: {
            p_id: Number
        },
        components: {
            Un_Authorized,
            Page_Not_Found,
            Store_Manager_Nav
        },
        data(){
            return {
                name: "",
                description: "",
                price: 0,
                unit_measure: "",
                stock: 0,
                units_sold: 0,
                mfg_date: null,
                exp_date: null,
                category: "",
                unauthorized: false,
                not_found: false
            }
        },
        computed: {
            home(){
                if (this.$route.path==='/store_manager_home')
                {return true}
                return false
            }
        },
        methods: {
            logout(){
                this.$store.commit('reset_data')
                this.$router.push('/store_manager_login')
            },
            async remove(){
                let message="Are you sure you want to Delete this product from your store?"
                if (!confirm(message))
                {return}
                let sm_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/product/${this.p_id}`
                let resp=await fetch(url, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                if (resp.status!==200)
                {
                    alert(data['msg'])
                    return
                }
                alert(data['msg'])
                this.$router.push('/store_manager/products')
                
            }
        },  
        async mounted(){
            let sm_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!sm_id)
            {
                this.not_found=false
                this.unauthorized=true
                return
            }
            let url=''
            if (this.home)
            {url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/product_home/${this.p_id}`}
            else
            {url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/product/${this.p_id}`}

            let resp=await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`
                }
            })
            if (resp.status===401)
            {
                this.not_found=false
                this.unauthorized=true
                return
            }
            else if (resp.status===404)
            {
                this.unauthorized=false
                this.not_found=true
                return
            }
            let data=await resp.json()
            this.name=data['name']
            this.description=data['description']
            this.price=data['price']
            this.unit_measure=data['unit_measure']
            this.stock=data['stock']
            this.units_sold=data['units_sold']
            this.mfg_date=data['mfg_date']
            this.exp_date=data['exp_date']
            this.category=data['category_name']
        }
    }
</script>

<style scoped>
 #edit{
    margin-right: 10px;
 }

 .card{
    border-color: black;
    border-width: 5px;
    margin-bottom: 10px;
}  
 
</style>