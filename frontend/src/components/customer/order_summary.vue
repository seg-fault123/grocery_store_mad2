<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
    <div v-else>
        <Customer_Nav @logout="logout()"></Customer_Nav> 
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <h3 class="card-title">Order Summary</h3>
                <p class="card-text"><b>Order Id : </b>{{ o_id }}</p>
                <p class="card-text"><b>Order Date : </b>{{ date }}</p>
                <table class="table table-bordered table-dark">
                    <thead>
                        <tr>
                            <th>Product Id</th>
                            <th>Product Name</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="product in products" :key="product.id">
                            <td>{{ product.id }}</td>
                            <td>{{ product.name }}</td>
                            <td>{{ product.price }}</td>
                            <td>{{ product.quantity }}</td>
                            <td>{{ product.price*product.quantity }}</td>
                        </tr>
                        <tr>
                            <th colspan="4" style="text-align: right;">Grand Total</th>
                            <td>{{ total }}</td>
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
    import Page_Not_Found from "../page_not_found"

    export default {
        name: "Order_Summary",
        props: {
            o_id: String
        },
        components: {
            Customer_Nav,
            Page_Not_Found,
            Un_Authorized
        },
        data(){
            return {
                date: "",
                products: [],
                unauthorized: false,
                not_found: false
            }
        },
        computed: {
            total(){
                let sum=0
                for (let i=0; i<this.products.length; i++)
                {
                    sum+=this.products[i]['price']*this.products[i]['quantity']
                }
                return sum
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
                this.not_found=false
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/order/${this.o_id}`
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
            this.date=data['date']
            this.products=data['products']
        }
    }
</script>
