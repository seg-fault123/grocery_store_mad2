<template>
    <div class="m-4 p-4 bg-dark text-white rounded" :id="cat_id">
        <h4>{{ name }}</h4>
        <p>{{ description }}</p>
        <hr class="my-4">
        <div v-for="product in products" :key="product.id">
            <Customer_Product :p_id="product.id"></Customer_Product>
        </div>
    </div>

</template>

<script>
    import Customer_Product from "./customer_product"
    
    export default {
        name: "Customer_Category",
        props: {
            cat_id: Number
        },
        components: {
            Customer_Product
        },  
        data(){
            return{
                name: "",
                description: "",
                products: []
            }
        },
        async mounted(){
            let c_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            let url=`http://127.0.0.1:5000/api/customer/${c_id}/category/${this.cat_id}`
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
            this.products=data['products']
        }
    }
</script>