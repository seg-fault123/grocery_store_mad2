<template>
    <div v-if="home" class="m-4 p-4 bg-dark text-white rounded" :id="cat_id">
        <h4>{{ name }}</h4>
        <p>{{ description }}</p>
        <hr class="my-4">
        <div v-if="not_empty">
            <div v-for="product in products" :key="product.id">
                <Store_Manager_Product :p_id="product.id"></Store_Manager_Product>
            </div>
        </div>
        <p v-else>No products in this Category</p>
    </div>
    <div v-else>
        <Un_Authorized v-if="unauthorized"></Un_Authorized>
        <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
        <div v-else>
            <Store_Manager_Nav @logout="logout()"></Store_Manager_Nav>
            <div class="card" style="margin-top: 20px;">
                <div class="card-body">
                    <h5 class="card-title"><b>{{ name }}</b></h5>
                    <p class="card-text"><b>Description : </b>{{ description }}</p>
                    <div class="row">
                        <p class="card-text col-1"><b>Products : </b><span v-if="not_empty===false">No Products</span></p> 
                        <ul v-if="not_empty" class="list-group col-2">
                            <li v-for="product in products" class="list-group-item" :key="product.id">
                                {{ product.name }}
                            </li>
                        </ul>
                        <div class="col-9"></div>
                    </div>
                    <div style="margin-top: 30px;">    
                        <button class="btn btn-outline-primary" id="edit"
                            @click="$router.push(`/store_manager/edit_category/${cat_id}`)">Edit</button>
                        <button class="btn btn-outline-danger" id="delete"
                            data-bs-toggle="collapse" data-bs-target="#delete_form" 
                            aria-expanded="false" aria-controls="delete_form">
                                Delete
                        </button>
                        <div class="collapse" id="delete_form" style="margin: 20px;">
                            <form>
                                <div class="row">
                                    <input v-model="reason" type="text" style="margin-left: 10px;"
                                        class="form-control mb-2 col" placeholder="Enter Reason for Deletion"/>
                                    <div class="col"></div>
                                </div>
                                <button @click="remove($event)" id="make_request"
                                    class="btn btn-outline-danger btn-sm">Make Request</button>
                                <button type="button" class="btn btn-outline-secondary btn-sm" id="cancel"
                                    data-bs-toggle="collapse" data-bs-target="#delete_form" 
                                    aria-expanded="false" aria-controls="delete_form">
                                        Cancel
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div> 




</template>

<script>
    import Store_Manager_Nav from "./store_manager_nav"
    import Store_Manager_Product from "./store_manager_product.vue"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"
    
    export default {
        name: "Store_Manager_Category",
        props: {
            cat_id: Number
        },
        components: {
            Store_Manager_Product,
            Un_Authorized,
            Page_Not_Found,
            Store_Manager_Nav
        },  
        data(){
            return{
                name: "",
                description: "",
                products: [],
                reason: "",
                unauthorized: false,
                not_found: false,
                msg: ""
            }
        },
        computed: {
            not_empty(){
                if (this.products.length>0)
                {return true}
                return false
            },
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
            async remove(e){
                e.preventDefault()
                if (this.reason==="")
                {
                    alert("Reason cannot be empty!")
                    return
                }
                let message="Are you sure you want to Delete this category?"
                if (!confirm(message))
                {return}
                let sm_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/category/${this.cat_id}`
                let resp=await fetch(url, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        "reason": this.reason
                    })
                })
                let data=await resp.json()
                if (resp.status!==200)
                {
                    alert(data['msg'])
                    return
                }
                alert(data['msg'])
                return
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
            let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/category/${this.cat_id}`
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
            this.products=data['products']
        }
    }
</script>

<style scoped>
    #edit {
        margin-right: 10px;
    }
    #make_request {
        margin-right: 10px;
    }
</style>