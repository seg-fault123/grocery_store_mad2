<template>

    <nav class="navbar navbar-expand-lg bg-dark" 
        data-bs-theme="dark">
        <div class="navbar-nav">
            <RouterLink class="nav-link" to="/store_manager_home">Home</RouterLink>
            <RouterLink class="nav-link" to="/store_manager/categories">Categories</RouterLink>
            <RouterLink class="nav-link" to="/store_manager/products">Your Products</RouterLink>
            <button class="nav-link" @click="$emit('logout')">Logout</button>
        </div>
    </nav>

</template>

<script>
    export default {
        name: "Store_Manager_Nav",
    }
</script>

