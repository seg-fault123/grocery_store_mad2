<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Customer_Nav @logout="logout()"></Customer_Nav> 
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <h3 class="card-title">Cart</h3>
                <div v-if="empty" class="alert alert-secondary" role="alert">
                    Cart is Empty!
                </div>
                <div v-else>
                    <div v-if="show_error" class="alert alert-danger" role="alert">
                        {{ msg }}
                    </div>
                    <table class="table table-bordered table-dark">
                        <thead>
                            <tr>
                                <th>Product Id</th>
                                <th>Product Name</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>Total Price</th>
                                <th>Options</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="product in cart" :key="product.id">
                                <td>{{ product.id }}</td>
                                <td>{{ product.name }}</td>
                                <td>{{ product.price }}</td>
                                <td>{{ product.quantity }}</td>
                                <td>{{ product.price*product.quantity }}</td>
                                <td>
                                    <button @click="$router.push(`/customer/edit_cart/${product.id}`)"
                                        :class="`btn btn-outline-success btn-sm ${product.id}`"
                                        id="edit">Edit</button>
                                    <button @click="remove($event)"
                                        :class="`btn btn-outline-danger btn-sm ${product.id}`">Delete</button>
                                </td>
                            </tr>
                            <tr>
                                <th colspan="4" style="text-align: right;">Grand Total</th>
                                <td>{{ total }}</td>
                                <td></td>
                            </tr>
                        </tbody>
                        <button @click="buy_all()"
                            class="btn btn-outline-success" id="buy_all">Buy All</button>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Customer_Nav from "./customer_nav"
    import Un_Authorized from "../un_authorized"

    export default {
        name: "Customer_Cart",
        components: {
            Customer_Nav,
            Un_Authorized
        },
        data(){
            return {
                cart: [],
                msg: "",
                unauthorized: false,
                show_error: false
            }
        },
        computed: {
            empty(){
                if (this.cart.length===0)
                {return true}
                return false
            },
            total(){
                let sum=0
                for (let i=0; i<this.cart.length; i++)
                {
                    sum+=this.cart[i]['price']*this.cart[i]['quantity']
                }
                return sum
            }
        },
        methods: {
            async buy_all(){
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/order`
                let resp=await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                if (resp.status===406)
                {
                    this.unauthorized=false
                    this.msg=data['msg']
                    this.show_error=true
                    return
                }
                this.$router.push(`/customer/order_summary/${data['order_id']}`)
            },
            async remove(e){
                if (!confirm("Are you sure you want to Delete this product from your Cart?"))
                {return}
                let c_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let p_id=e.target.classList[3]
                let url=`http://127.0.0.1:5000/api/customer/${c_id}/cart/${p_id}`
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
                    this.unauthorized=false
                    this.msg=data['msg']
                    this.show_error=true
                    return
                }
                let i=0
                for (i=0; i<this.cart.length; i++)
                {
                    if (this.cart[i].id==p_id)
                    {
                        this.cart.splice(i, 1)
                        break
                    }
                }
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
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/cart`
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
                this.unauthorized=true
                return
            }
            this.show_error=false
            this.unauthorized=false
            let data=await resp.json()
            this.cart=data['cart']
        }
        

    }
</script>

<style scoped>
    #edit{
        margin-right: 10px;
    }
    #buy_all{
        margin-top: 10px;
    }
</style>