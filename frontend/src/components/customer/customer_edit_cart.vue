<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
    <div v-else>
        <Customer_Nav @logout="logout()"></Customer_Nav>
        <form>
            <div class="card" :id="p_id" style="margin-top: 20px;">
                <div class="card-body">
                    <div v-if="show_error" class="alert alert-danger" role="alert">
                        {{ msg }}
                    </div>
                    <div v-if="show_success" class="alert alert-success" role="alert">
                        {{ msg }}
                    </div>
                    <h5 class="card-title"><b>{{ name }}</b></h5>
                    <p class="card-text"><b>Description : </b>{{ description }}</p>
                    <p class="card-text"><b>Rate : </b>{{ price }} {{ unit_measure }}</p>
                    <p class="card-text" v-if="mfg_date"><b>Mfg Date : </b>{{ mfg_date }}</p>
                    <p class="card-text" v-if="exp_date"><b>Exp Date : </b>{{ exp_date }}</p>
                    <div class="form-group row">
                        <label for="quantity" class="col-2"><b>Quantity</b></label>
                        <input v-model="quantity" type="number" min="1" :max="max_available"
                            class="form-control col" id="quantity" step="1"/>
                        <div class="col-8"></div>
                    </div>
                    <p><b>Total : </b>{{ total }}</p>
                    <div style="margin-top: 10px;">
                        <button @click="save($event)" id="save"
                            class="btn btn-outline-primary">Save</button>
                        <button class="btn btn-outline-secondary"
                            @click="$router.push(`/customer_cart`)">Cancel</button>
            </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import Customer_Nav from "./customer_nav"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"

    export default {
        name: "Customer_Edit_Cart",
        props: {
            p_id: String
        },
        components: {
            Customer_Nav,
            Page_Not_Found,
            Un_Authorized
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
                quantity: 0,
                msg: "",
                unauthorized: false,
                not_found: false,
                show_error: false,
                show_success: false
            }
        },
        computed: {
            total(){
                return this.quantity * this.price
            },
            max_available(){
                return Math.min(this.stock, 10)
            }
        },
        methods: {
            async save(e){
                e.preventDefault()
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/cart/${this.p_id}`
                let resp=await fetch(url, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        "quantity": this.quantity
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
                this.$router.push('/customer_login')
            }
        },
        async mounted(){
            let c_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!c_id)
            {
                this.show_error=false
                this.show_success=false
                this.not_found=false
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/cart_product/${this.p_id}`
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
            else if (resp.status===404)
            {
                this.show_error=false
                this.show_success=false
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
            this.mfg_date=data['mfg_date']
            this.exp_date=data['exp_date']
            this.quantity=data['quantity']
            return

        }

    }
</script>

<style scoped>
    #save{
        margin-right: 10px;
    }
</style>