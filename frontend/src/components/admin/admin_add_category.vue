<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
    <div v-else>
        <Admin_Nav @logout="logout()"></Admin_Nav>
        <form>
            <div class="card" style="margin-top: 20px;">
                <div class="card-body rounded" style="background-color: wheat;">
                    <div v-if="show_error" class="alert alert-danger" role="alert">
                        {{ msg }}
                    </div>
                    <div v-if="show_success" class="alert alert-success" role="alert">
                        {{ msg }}
                    </div>
                    <h3 class="card-title"><b>Add Category</b></h3>
                    <div class="form-group row mb-2">
                        <label for="name"><b>Name</b></label>
                        <input v-model="name" type="text" class="form-control col" 
                        style="margin-left: 10px;" id="name" name="name"/>
                        <div class="col"></div>
                    </div>
                    <div class="form-group row mb-2">
                        <label for="description"><b>Description</b></label>
                        <input v-model="description" type="text" class="form-control col" 
                        style="margin-left: 10px;" id="description" name="description"/>
                        <div class="col"></div>
                    </div>                                             
                    <div style="margin-top: 30px;">
                        <button @click="add($event)" id="add"
                            class="btn btn-outline-success">Add</button>
                        <button class="btn btn-outline-secondary"
                            @click="$router.push(`/admin/categories`)">Cancel</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import Admin_Nav from "./admin_nav"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"

    export default {
        name: "Admin_Add_Category",
        components: {
            Admin_Nav,
            Un_Authorized,
            Page_Not_Found
        },
        data(){
            return {
                name: "",
                description: "",
                unauthorized: false,
                not_found: false,
                show_error: false,
                show_success: false,
                msg: ""
            }
        },
        methods: {
            async add(e){
                e.preventDefault()
                let a_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/admin/${a_id}/category`
                let resp=await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        "name": this.name,
                        "description": this.description,                       
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
                this.$router.push('/admin_login')
            }
        },
        mounted(){
            let role_name=this.$store.state.role_name
            if (role_name!=='admin')
            {
                this.show_error=false
                this.show_success=false
                this.not_found=false
                this.unauthorized=true
                return
            }
            return       
        }
        

    }
</script>

<style>
    #add {
        margin-right: 10px;
    }
</style>