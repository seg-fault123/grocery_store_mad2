<template>
    <div class="card" :id="p_id">
        <div class="card-body">
            <h5 class="card-title"><b>{{ name }}</b></h5>
            <p class="card-text"><b>Description : </b>{{ description }}</p>
            <p class="card-text"><b>Rate : </b>{{ price }} {{ unit_measure }}</p>
            <p class="card-text" v-if="mfg_date"><b>Mfg Date : </b>{{ mfg_date }}</p>
            <p class="card-text" v-if="exp_date"><b>Exp Date : </b>{{ exp_date }}</p>
            <p class="card-text"><b>Category : </b>{{ category }}</p>
            <p class="card-text"><b>Stock : </b>{{ stock }}</p>
            <p class="card-text"><b>Units Sold : </b>{{ units_sold }}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Admin_Product',
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
                units_sold: 0,
                mfg_date: null,
                exp_date: null,
                category: ""
            }
        },
        async mounted(){
            let a_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            let url=`http://127.0.0.1:5000/api/admin/${a_id}/product/${this.p_id}`
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
            this.units_sold=data['units_sold']
            this.mfg_date=data['mfg_date']
            this.exp_date=data['exp_date']
            this.category=data['category_name']
        }
    }
</script>

<style scoped>
 .card{
    border-color: black;
    border-width: 5px;
    margin-bottom: 10px;
}  
 </style>