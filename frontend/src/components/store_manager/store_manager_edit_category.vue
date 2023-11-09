<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <Page_Not_Found v-else-if="not_found"></Page_Not_Found>
    <div v-else>
        <Store_Manager_Nav @logout="logout()"></Store_Manager_Nav>
        <form>
            <div class="card" style="margin-top: 20px;">
                <div class="card-body rounded" style="background-color: wheat;">
                    <div v-if="show_error" class="alert alert-danger" role="alert">
                        {{ msg }}
                    </div>
                    <div v-if="show_success" class="alert alert-success" role="alert">
                        {{ msg }}
                    </div>
                    <h3 class="card-title"><b>Edit Category</b></h3>
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
                    <div class="form-group row mb-2">
                        <label for="reason"><b>Reason</b></label>
                        <input v-model="reason" type="text" class="form-control col" 
                        style="margin-left: 10px;" id="reason" name="reason"/>
                        <div class="col"></div>
                    </div>                       
                    <div style="margin-top: 30px;">
                        <button @click="save($event)" id="save"
                            class="btn btn-outline-success">Make Request</button>
                        <button class="btn btn-outline-secondary"
                            @click="$router.push(`/store_manager/category/${cat_id}`)">Cancel</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import Store_Manager_Nav from "./store_manager_nav"
    import Un_Authorized from "../un_authorized"
    import Page_Not_Found from "../page_not_found"

    export default {
        name: "Store_Manager_Edit_Category",
        props: {
            cat_id: Number
        },
        components: {
            Store_Manager_Nav,
            Un_Authorized,
            Page_Not_Found
        },
        data(){
            return {
                name: "",
                description: "",
                reason: "",
                unauthorized: false,
                not_found: false,
                show_error: false,
                show_success: false,
                msg: ""
            }
        },
        methods: {
            async save(e){
                e.preventDefault()
                let sm_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/category/${this.cat_id}`
                let resp=await fetch(url, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        "name": this.name,
                        "description": this.description,
                        "reason": this.reason                        
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
                this.$router.push('/store_manager_login')
            }
        },
        async mounted(){
            let sm_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!sm_id)
            {
                this.show_error=false
                this.show_success=false
                this.not_found=false
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/store_manager/${sm_id}/category/${this.cat_id}`
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
                this.show_success=false
                this.not_found=false
                this.unauthorized=true
                return
            }
            else if (resp.status===404)
            {
                this.show_error=false
                this.show_success=false
                this.unauthorized=false
                this.not_found=true
                return
            }
            let data=await resp.json()
            this.name=data['name']
            this.description=data['description']
        }
        

    }
</script>

<style>
    #save {
        margin-right: 10px;
    }
</style>