<template>

    <nav class="navbar navbar-expand-lg bg-dark" 
        data-bs-theme="dark">
        <div class="navbar-nav">
            <RouterLink class="nav-link" to="/admin_home">Home</RouterLink>
            <RouterLink class="nav-link" to="/admin/categories">Categories</RouterLink>
            <RouterLink class="nav-link" to="/admin/new_store_managers">New Store Managers</RouterLink>
            <button class="nav-link" @click="$emit('logout')">Logout</button>
        </div>
    </nav>

</template>

<script>
    export default {
        name: "Admin_Nav",
    }
</script>

