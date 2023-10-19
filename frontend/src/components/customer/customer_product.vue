<template>
    <div class="card" :id="p_id">
        <div class="card-body">
            <h5 class="card-title"><b>{{ name }}</b></h5>
            <p class="card-text"><b>Description : </b>{{ description }}</p>
            <p class="card-text"><b>Rate : </b>{{ price }} {{ unit_measure }}</p>
            <p class="card-text" v-if="mfg_date"><b>Mfg Date : </b>{{ mfg_date }}</p>
            <p class="card-text" v-if="exp_date"><b>Exp Date : </b>{{ exp_date }}</p>
            <div v-if="instock">
                <button class="btn btn-outline-primary" id="buy_now"
                    @click="$router.push(`/customer/buy_now/${p_id}`)">Buy Now</button>
                <button class="btn btn-outline-success" id="add_to_cart"
                    @click="$router.push(`/customer/add_to_cart/${p_id}`)">Add to Cart</button>
            </div>
            <div v-else>
                <button class="btn btn-secondary" disabled>Out of Stock</button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Customer_Product',
        props: {
            p_id: Number
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
            }
        },
        computed: {
            instock(){
                if (this.stock>0)
                {return true}
                else
                {return false}
            }
        },
        async mounted(){
            let c_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/product/${this.p_id}`
            let resp=await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`
                }
            })
            let data=await resp.json()
            this.name=data['name']
            this.description=data['description']
            this.price=data['price']
            this.unit_measure=data['unit_measure']
            this.stock=data['stock']
            this.mfg_date=data['mfg_date']
            this.exp_date=data['exp_date']
        }
    }
</script>

<style scoped>
 #buy_now{
    margin-right: 10px;
 }
 
</style>