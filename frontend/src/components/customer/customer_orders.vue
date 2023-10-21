<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Customer_Nav @logout="logout()"></Customer_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <h3>Previous Orders</h3>
                <table class="table">
                    <tbody>
                        <tr v-for="order in orders" :key="order.id">
                            <td style="border-radius: 10px;">
                                <button class="btn btn-outline-success btn-lg"
                                    @click="$router.push(`/customer/order_summary/${order.id}`)">
                                    Order Id : {{ order.id }} &nbsp; &nbsp; &nbsp; &nbsp; Date : {{ order.date }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div> 
    </div>
</template>

<script>
    import Customer_Nav from "./customer_nav"
    import Un_Authorized from "../un_authorized"

    export default {
        name: "Customer_Orders",
        components: {
            Customer_Nav,
            Un_Authorized
        },
        data(){
            return {
                orders: [],
                unauthorized: false,
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
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/orders`
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
            this.orders=data['orders']
        }

    }
</script>