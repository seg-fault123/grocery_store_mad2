<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Admin_Nav @logout="logout()"></Admin_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <h3 class="card-title">New Store Managers</h3>
                <hr class="my-4">
                <div v-if="empty" class="alert alert-secondary" role="alert">
                    No Requests as of Now!
                </div>
                <div v-else>
                    <div v-if="show_error" class="alert alert-danger" role="alert">
                        {{ msg }}
                    </div>
                    <div v-if="show_success" class="alert alert-success" role="alert">
                        {{ msg }}
                    </div>
                    <table class="table table-bordered table-dark">
                        <thead>
                            <tr>
                                <th>Store Manager ID</th>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Email ID</th>
                                <th>UserName</th>
                                <th>Options</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="request in requests" :key="request.id">
                                <td>{{ request.id }}</td>
                                <td>{{ request.first_name }}</td>
                                <td>{{ request.last_name }}</td>
                                <td>{{ request.email_id }}</td>
                                <td>{{ request.user_name }}</td>
                                <td>
                                    <button @click="accept($event)"
                                        :class="`btn btn-outline-success btn-sm ${request.id}`"
                                        id="accept">Accept</button>
                                    <button @click="decline($event)"
                                        :class="`btn btn-outline-danger btn-sm ${request.id}`">Decline</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import Admin_Nav from "./admin_nav"
    import Un_Authorized from "../un_authorized"

    export default {
        name: "Admin_New_Store_Managers",
        components: {
            Un_Authorized,
            Admin_Nav
        },
        data(){
            return {
                requests: [],
                msg: "",
                unauthorized: false,
                show_error: false,
                show_success: false
            }
        },
        computed: {
            empty(){
                if (this.requests.length===0)
                {return true}
                return false
            }
        },
        methods: {
            async accept(e){
                let message=`Are you sure you want to Accept this Request?`
                if (!confirm(message))
                {return}
                let a_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let sm_id=e.target.classList[3]
                let url1=`http://127.0.0.1:5000/api/admin/${a_id}/new_store_manager/${sm_id}`
                let resp1=await fetch(url1, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                })
                let data1=await resp1.json()
                if (resp1.status!==200)
                {
                    this.unauthorized=false
                    this.show_success=false
                    this.msg=data1['msg'].concat(` Please Decline Request ${sm_id}`)
                    this.show_error=true
                    return
                }
                let i=0
                for(i=0; i<this.requests.length; i++)
                {
                    if (this.requests[i].id==sm_id)
                    {
                        this.requests.splice(i, 1)
                        break
                    }
                }
                this.unauthorized=false
                this.show_error=false
                this.msg="Request Accepted! Store Manager Approved Successfully!"
                this.show_success=true
            },
            async decline(e){
                let message="Are you sure you want to Decline this Request?"
                if (!confirm(message))
                {return}
                let a_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let sm_id=e.target.classList[3]
                let url=`http://127.0.0.1:5000/api/admin/${a_id}/new_store_manager/${sm_id}`
                let resp=await fetch(url, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                let data=await resp.json()
                if (resp.status!==200)
                {
                    this.unauthorized=false
                    this.show_success=false
                    this.msg=data['msg']
                    this.show_error=true
                    return
                }
                let i=0
                for (i=0; i<this.requests.length; i++)
                {
                    if (this.requests[i].id==sm_id)
                    {
                        this.requests.splice(i, 1)
                        break
                    }
                }
                this.unauthorized=false
                this.show_error=false
                this.msg=data['msg']
                this.show_success=true
            },
            logout(){
                this.$store.commit('reset_data')
                this.$router.push('/admin_login')
            }
        },
        async mounted(){
            let a_id=this.$store.state.id
            let access_token=this.$store.state.access_token
            if (!a_id)
            {
                this.show_error=false
                this.show_success=false
                this.unauthorized=true
                return
            }
            let url=`http://127.0.0.1:5000/api/admin/${a_id}/new_store_managers`
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
                this.unauthorized=true
                return
            }
            this.show_error=false
            this.show_success=false
            this.unauthorized=false
            let data=await resp.json()
            this.requests=data['requests']
        }
    }
</script>

<style scoped>
    #accept {
        margin-right: 10px;
    }
</style>
