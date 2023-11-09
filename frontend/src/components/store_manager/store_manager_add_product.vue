<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
    <div v-else>
        <Store_Manager_Nav @logout="logout()"></Store_Manager_Nav>
        <form>
            <div class="card" style="margin-top: 20px;">
                <div class="card-body rounded" style="background-color: wheat;">
                    <div v-if="show_error" class="alert alert-danger" role="alert">
                        {{ msg }}
                    </div>
                    <div v-if="show_success" class="alert alert-success" role="alert">
                        {{ msg }}
                    </div>
                    <h3 class="card-title"><b>Add Product</b></h3>
                    <div class="form-group row mb-2">
                        <label for="name"><b>Name</b></label>
                        <input v-model="name" type="text" class="form-control col" 
                        style="margin-left: 10px;" id="name" name="name"/>
                        <div class="col"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="description"><b>Description</b></label>
                        <input v-model="description" type="text" class="form-control col" 
                        style="margin-left: 10px;" id="description" name="description"/>
                        <div class="col"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="price"><b>Price</b></label>
                        <input v-model="price" type="number" class="form-control col" min="1" step="1"
                        style="margin-left: 10px;" id="price" name="price"/>
                        <div class="col-8"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="unit_measure"><b>Unit Measure</b></label>
                        <select v-model="unit_measure" class="form-select col" style="margin-left: 10px;" id="unit_measure">
                            <option value="Rs/packet">Rs/packet</option>
                            <option value="Rs/Litre">Rs/Litre</option>
                            <option value="Rs/Kg">Rs/Kg</option>
                            <option value="Rs/Gram">Rs/Gram</option>
                            <option value="Rs/ml">Rs/ml</option>
                            <option value="Rs/Item">Rs/Item</option>
                        </select>
                        <div class="col"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="stock"><b>Stock</b></label>
                        <input v-model="stock" type="number" class="form-control col" min="0" step="1"
                        style="margin-left: 10px;" id="stock" name="stock"/>
                        <div class="col-8"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="mfg_date"><b>Mfg Date</b></label>
                        <input v-model="mfg_date" type="date" class="form-control col"
                            style="margin-left: 10px;" id="mfg_date" />
                        <div class="col-8"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="exp_date"><b>Exp Date</b></label>
                        <input v-model="exp_date" type="date" class="form-control col"
                            style="margin-left: 10px;" id="exp_date" />
                        <div class="col-8"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="category"><b>Category</b></label>
                        <select  v-model="category" class="form-select col" style="margin-left: 10px;" id="category">
                            <option v-for="cat in categories" :key="cat.id" :value="cat.name">
                                {{ cat.name }}
                            </option>
                        </select>
                        <div class="col"></div>
                    </div>
                    <div style="margin-top: 30px;">
                        <button @click="add($event)" id="add"
                            class="btn btn-outline-success">Add</button>
                        <button class="btn btn-outline-secondary"
                            @click="$router.push(`/store_manager/products`)">Cancel</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import Store_Manager_Nav from "./store_manager_nav"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"

    export default {
        name: "Store_Manager_Add_Product",
        components: {
            Store_Manager_Nav,
            Un_Authorized,
            Page_Not_Found
        },
        data(){
            return {
                name: "",
                description: "",
                price: 0,
                unit_measure: "",
                stock: 0,
                mfg_date: null,
                exp_date: null,
                category: "",
                categories: [],
                unauthorized: false,
                not_found: false,
                show_error: false,
                show_success: false,
                msg: ""
            }
        },
        methods: {
            async add(e){
                e.preventDefault()
                let sm_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/product`
                let resp=await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        "name": this.name,
                        "description": this.description,
                        "price": this.price,
                        "unit_measure": this.unit_measure,
                        "stock": this.stock,
                        "mfg_date": this.mfg_date,
                        "exp_date": this.exp_date,
                        "category_name": this.category
                    })
                })
                let data=await resp.json()
                if (resp.status===406)
                {
                    this.unauthorized=false
                    this.not_found=false
                    this.show_success=false
                    this.msg=data['msg']
                    this.show_error=true
                    return
                }
                this.msg=data['msg']
                this.unauthorized=false
                this.not_found=false
                this.show_error=false
                this.show_success=true
            },
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
                this.show_error=false
                this.show_success=false
                this.not_found=false
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
                this.show_error=false
                this.show_success=false
                this.not_found=false
                this.unauthorized=true
                return
            }
            let data=await resp.json()
            this.categories=data['categories']
            
        }
        

    }
</script>

<style>
    #add {
        margin-right: 10px;
    }
</style>