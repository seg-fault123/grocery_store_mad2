<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Store_Manager_Nav @logout="logout()"></Store_Manager_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <div class="row">
                    <h3 class="card-title col">Your Products</h3>
                    <button class="btn btn-outline-success btn-lg col" id="add"
                        @click="$router.push(`/store_manager/add_product`)">Add Product</button>
                    <button v-if="empty===false" class="btn btn-outline-dark btn-lg col"
                        @click="download_report()">Download Report</button>
                    <div class="col-2">
                        <p v-if="waiting" class="badge bg-warning" style="padding=20px">Please Wait!</p>
                    </div>
                </div>
                <div v-if="empty" class="alert alert-secondary" role="alert">
                    You do not have any products!
                </div>
                <div v-else>
                    <table class="table">
                        <tbody>
                            <tr v-for="product in products" :key="product.id">
                                <td>
                                    <button class="btn btn-outline-primary btn-lg"
                                        @click="$router.push(`/store_manager/product/${product.id}`)">
                                            {{ product.name }}
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
        name: "Store_Manager_Products",
        components: {
            Un_Authorized,
            Store_Manager_Nav
        },
        data(){
            return {
                unauthorized: false,
                products: [],
                waiting: false
            }
        },
        computed: {
            empty(){
                if (this.products.length==0)
                {return true}
                return false
            }
        },
        methods: {
            async download_report(){
                this.waiting=true
                let sm_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url1=`http://127.0.0.1:5000/api/store_manager/${sm_id}/create_report`
                let resp1=await fetch(url1, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data1=await resp1.json()
                let task_id=data1['task_id']
                let url2=`http://127.0.0.1:5000/api/store_manager/${sm_id}/download_report/${task_id}`
                let intv=setInterval(async ()=>{
                    let resp2=await fetch(url2, {
                        method: "GET",
                        headers: {
                            "Authorization": `Bearer ${access_token}`,
                        }
                    })
                    if (resp2.status===200)
                    {
                        clearInterval(intv)
                        let blob=await resp2.blob()
                        let filename=`report${sm_id}.csv`
                        const link=document.createElement('a')
                        link.href = window.URL.createObjectURL(blob)
                        link.download = filename
                        link.click()
                        window.URL.revokeObjectURL(link.href)
                        this.waiting=false
                        alert("Report Downloaded Successfully!")
                    }
                }, 1000)
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
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/products`
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
            this.products=data['products']
        }
        
    }
</script>

<style scoped>
    #add {
        margin-right: 10px;
    }
</style>