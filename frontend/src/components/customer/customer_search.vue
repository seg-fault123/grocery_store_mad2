<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Customer_Nav @logout="logout()"></Customer_Nav>
        <h1 style="margin-top: 20px;">Search</h1>
        <div id="options" style="background-color: white; border-radius: 10px;">
            <div id="p_name" style="margin: 10px; padding: 10px;">
                <button type="button" class="btn btn-outline-dark btn-lg" 
                    data-bs-toggle="collapse" data-bs-target="#by_pname" 
                    aria-expanded="false" aria-controls="by_pname">
                        Search By Product Name
                </button>
                <div class="collapse" id="by_pname" style="margin: 20px;">
                    <form>
                        <div class="row">
                            <input v-model="p_name" type="text" style="margin-left: 10px;"
                                class="form-control mb-2 col" placeholder="Enter Product Name"/>
                            <div class="col"></div>
                        </div>
                            <button @click="by_pname($event)"
                            class="btn btn-outline-primary btn-sm">Search</button>                                   
                    </form>
                </div>
            </div>
            <div id="c_name" style="margin: 10px; padding: 10px;">
                <button type="button" class="btn btn-outline-dark btn-lg" 
                    data-bs-toggle="collapse" data-bs-target="#by_cname" 
                    aria-expanded="false" aria-controls="by_cname">
                        Search By Category Name
                </button>
                <div class="collapse" id="by_cname" style="margin: 20px;">
                    <form>
                        <div class="row">
                            <input v-model="c_name" type="text" style="margin-left: 10px;"
                                class="form-control mb-2 col" placeholder="Enter Category Name"/>
                            <div class="col"></div>
                        </div>
                        <button @click="by_cname($event)"
                            class="btn btn-outline-primary btn-sm">Search</button>                                   
                    </form>
                </div>
            </div>
            <div id="price" style="margin: 10px; padding: 10px;">
                <button type="button" class="btn btn-outline-dark btn-lg" 
                    data-bs-toggle="collapse" data-bs-target="#by_price" 
                    aria-expanded="false" aria-controls="by_price">
                        Search By Price
                </button>
                <div class="collapse" id="by_price" style="margin: 20px;">
                    <form>
                        <div class="row">
                            <input v-model="price" type="number" style="margin-left: 10px;" step="1" min="0"
                                class="form-control mb-2 col" placeholder="Enter Price"/>
                            <div class="col-10"></div>
                        </div>
                        <button @click="by_price($event)"
                            class="btn btn-outline-primary btn-sm">Search</button>                                   
                    </form>
                </div>
            </div>
            <div id="mfg_date" style="margin: 10px; padding: 10px;">
                <button type="button" class="btn btn-outline-dark btn-lg" 
                    data-bs-toggle="collapse" data-bs-target="#by_mfg_date" 
                    aria-expanded="false" aria-controls="by_mfg_date">
                        Search By Mfg Date
                </button>
                <div class="collapse" id="by_mfg_date" style="margin: 20px;">
                    <form>
                        <div class="row">
                            <input v-model="mfg_date" type="date" style="margin-left: 10px;"
                                class="form-control mb-2 col"/>
                            <div class="col-10"></div>
                        </div>
                        <button @click="by_mfg_date($event)"
                            class="btn btn-outline-primary btn-sm">Search</button>                                   
                    </form>
                </div>
            </div>
        </div>
        <div v-if="show_results" id="results">
            <h2 style="text-align: center; margin: 20px;">Results</h2>
            <div v-if="no_results" class="alert alert-secondary" role="alert">
                Nothing matches! Try searching something different.
            </div>
            <div v-else-if="show_products" class="m-4 p-4 bg-dark rounded">
                <div v-for="product in products" :key="product">
                    <Customer_Product :p_id="product"></Customer_Product>
                </div>
            </div>
            <div v-else-if="show_categories">
                <div v-for="category in categories" :key="category">
                    <Customer_Category :cat_id="category"></Customer_Category>
                </div>
            </div>
        </div>        

        
    </div> 
</template>

<script>
    import Customer_Category from "./customer_category"
    import Customer_Nav from "./customer_nav"
    import Customer_Product from "./customer_product"
    import Un_Authorized from "../un_authorized"

    export default {
        name: "Customer_Search",
        components: {
            Customer_Category,
            Customer_Nav,
            Customer_Product,
            Un_Authorized
        },
        data(){
            return {
                p_name: "",
                c_name: "",
                price: 0,
                mfg_date: "",
                products: [],
                categories: [],
                show_products: false,
                show_categories: false,
                show_results: false,
                no_results: true,
                unauthorized: false
            }
        },
        methods: {
            async by_pname(e){
                e.preventDefault()
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/search?option=p_name&p_name=${this.p_name}`
                let resp=await fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                this.products=data['results']
                this.show_categories=false
                this.unauthorized=false
                if (this.products.length==0)
                {this.no_results=true}
                else
                {this.no_results=false}
                this.show_products=true
                this.show_results=true
            },
            async by_cname(e){
                e.preventDefault()
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/search?option=c_name&c_name=${this.c_name}`
                let resp=await fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                this.categories=data['results']
                this.show_products=false
                this.unauthorized=false
                if (this.categories.length==0)
                {this.no_results=true}
                else
                {this.no_results=false}
                this.show_categories=true
                this.show_results=true
            },
            async by_price(e){
                e.preventDefault()
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/search?option=price&price=${this.price}`
                let resp=await fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                this.products=data['results']
                this.show_categories=false
                this.unauthorized=false
                if (this.products.length==0)
                {this.no_results=true}
                else
                {this.no_results=false}
                this.show_products=true
                this.show_results=true
            }, 
            async by_mfg_date(e){
                e.preventDefault()
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/search?option=mfg_date&mfg_date=${this.mfg_date}`
                let resp=await fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                this.products=data['results']
                this.show_categories=false
                this.unauthorized=false
                if (this.products.length==0)
                {this.no_results=true}
                else
                {this.no_results=false}
                this.show_products=true
                this.show_results=true
            },          
            logout(){
                this.$store.commit('reset_data')
                this.$router.push('/customer_login')
            }
        },
        mounted(){
            let role_name=this.$store.state.role_name
            if (!role_name || role_name!=='customer')
            {
                this.show_products=false
                this.show_categories=false
                this.show_results=false
                this.unauthorized=true
                return
            }
            this.show_products=false
            this.show_categories=false
            this.show_results=false
            this.unauthorized=false
        }
    }
</script>