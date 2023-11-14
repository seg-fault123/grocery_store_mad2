<template>
    <Un_Authorized v-if="unauthorized"></Un_Authorized>
    <div v-else>
        <Admin_Nav @logout="logout()"></Admin_Nav>
        <div class="card" style="margin-top: 20px;">
            <div class="card-body">
                <div class="row">
                    <h3 class="card-title col">New Category Requests</h3>
                    <button class="btn btn-outline-secondary col-1" 
                        @click="$router.push(`/admin/category_requests`)">Back</button>
                    <div class="col-7"></div>
                </div>
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
                                <th>Request ID</th>
                                <th>Category Name</th>
                                <th>Category Description</th>
                                <th>Reason</th>
                                <th>Store Manager ID</th>
                                <th>Store Manager Name</th>
                                <th>Options</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="request in requests" :key="request.id">
                                <td>{{ request.id }}</td>
                                <td>{{ request.name }}</td>
                                <td>{{ request.description }}</td>
                                <td>{{ request.reason }}</td>
                                <td>{{ request.sm_id }}</td>
                                <td>{{ request.sm_name }}</td>
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
        name: "Admin_New_Category_Requests",
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
                let message="Are you sure you want to Accept this Request?"
                if (!confirm(message))
                {return}
                let a_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let r_id=e.target.classList[3]
                let request={}
                let i=0
                for(i=0; i<this.requests.length; i++)
                {
                    if (this.requests[i].id==r_id)
                    {
                        request=this.requests[i]
                        break
                    }
                }
                let url1=`http://127.0.0.1:5000/api/admin/${a_id}/category`
                let resp1=await fetch(url1, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        "name": request.name,
                        "description": request.description
                    })
                })
                let data1=await resp1.json()
                if (resp1.status===406)
                {
                    this.unauthorized=false
                    this.show_success=false
                    this.msg=data1['msg'].concat(` Please Decline Request ${r_id}`)
                    this.show_error=true
                    return
                }
                let url2=`http://127.0.0.1:5000/api/admin/${a_id}/new_category_request/${r_id}`
                let resp2=await fetch(url2, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`
                    }
                })
                if (resp2.status!==200)
                {
                    this.unauthorized=false
                    this.show_success=false
                    this.msg=data1['msg'].concat(` Please Decline Request ${r_id}`)
                    this.show_error=true
                    return
                }
                this.requests.splice(i, 1)
                this.unauthorized=false
                this.show_error=false
                this.msg="Request Accepted! Category Created Successfully!"
                this.show_success=true
            },
            async decline(e){
                let message="Are you sure you want to Decline this Request?"
                if (!confirm(message))
                {return}
                let a_id=this.$store.state.id
                let access_token=this.$store.state.access_token
                let r_id=e.target.classList[3]
                let url=`http://127.0.0.1:5000/api/admin/${a_id}/new_category_request/${r_id}`
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
                    if (this.requests[i].id==r_id)
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
            let url=`http://127.0.0.1:5000/api/admin/${a_id}/new_category_requests`
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
