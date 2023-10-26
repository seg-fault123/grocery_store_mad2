<template>

    <nav class="navbar navbar-expand-lg bg-dark" 
        data-bs-theme="dark">
        <div class="navbar-nav">
            <RouterLink class="nav-link" to="/customer_home">Home</RouterLink>
            <RouterLink class="nav-link" to="/customer_search">Search</RouterLink>
            <RouterLink class="nav-link" to="/customer_cart">Cart</RouterLink>
            <RouterLink class="nav-link" to="/customer_orders">Previous Orders</RouterLink>
            <button class="nav-link" @click="$emit('logout')">Logout</button>
        </div>
    </nav>

</template>

<script>
    export default {
        name: "Customer_Nav",
    }
</script>

