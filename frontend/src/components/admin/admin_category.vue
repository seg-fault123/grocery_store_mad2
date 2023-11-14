<template>
    <div v-if="home" class="m-4 p-4 bg-dark text-white rounded" :id="cat_id">
        <h4>{{ name }}</h4>
        <p>{{ description }}</p>
        <hr class="my-4">
        <div v-if="not_empty">
            <div v-for="product in products" :key="product.id">
                <Admin_Product :p_id="product.id"></Admin_Product>
            </div>
        </div>
        <p v-else>No products in this Category</p>
    </div>
    <div v-else>
        <Un_Authorized v-if="unauthorized"></Un_Authorized>
        <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
        <div v-else>
            <Admin_Nav @logout="logout()"></Admin_Nav>
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
                            @click="$router.push(`/admin/edit_category/${cat_id}`)">Edit</button>
                        <button class="btn btn-outline-danger" id="delete"
                            @click="remove()">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div> 




</template>

<script>
    import Admin_Nav from "./admin_nav"
    import Admin_Product from "./admin_product.vue"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"
    
    export default {
        name: "Admin_Category",
        props: {
            cat_id: Number
        },
        components: {
            Admin_Product,
            Un_Authorized,
            Page_Not_Found,
            Admin_Nav
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
                if (this.$route.path==='/admin_home')
                {return true}
                return false
            }
        },
        methods: {
            logout(){
                this.$store.commit('reset_data')
                this.$router.push('/admin_login')
            },
            async remove(){
                let message="Are you sure you want to Delete this category?"
                if (!confirm(message))
                {return}
                let a_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/admin/${a_id}/category/${this.cat_id}`
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
                this.$router.push('/admin/categories')
            }
        },  
        async mounted(){
            let a_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!a_id)
            {
                this.not_found=false
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/admin/${a_id}/category/${this.cat_id}`
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
</style>