<template>
    <div class="container" style="background-color: wheat; padding: 10px; margin-top: 20px; border-radius: 10px;">
        <h2 style="padding: 10px;">Welcome to the Store Manager Login Page</h2>
        <br>
        <div v-if="show_error" class="alert alert-danger" role="alert">
            {{ msg }}
        </div>
        <form id="sm_login">
            <div class="form-group row">
                <label for="user_name">UserName</label>
                <input v-model="user_name" type="text" class="form-control col" 
                   style="margin-left: 10px;" id="user_name" name="user_name"/>
                <div class="col"></div>
            </div>
            <div class="form-group row">
                <label for="password">Password</label>
                <input v-model="password" type="password" class="form-control col"
                    style="margin-left: 10px;" id="password" name="password">
                <div class="col"></div>
            </div>
            <div style="margin-top: 10px;">
                <button @click="send_credentials($event)" 
                    class="btn btn-outline-primary">Login</button>
            </div>
        </form>
        <div class="container" id="links" style="margin-top: 60px;">
            <div class="row">
                <div class="col">
                    <div class="badge bg-dark">
                        <h5>Are you a Customer?</h5>
                        <p><RouterLink to="/customer_login">Click Here to Login</RouterLink></p>
                        <p><RouterLink to="/customer_signup">Click Here to Register</RouterLink></p>
                    </div>   
                </div>
                <div class="col">
                    <div class="badge bg-dark">
                        <h5>Are you an Admin?</h5>
                        <p><RouterLink to="/admin_login">Click Here to Login</RouterLink></p>
                    </div>
                </div>
                <div class="col">
                    <div class="badge bg-dark">
                        <h5>New Store Manager?</h5>
                        <p><RouterLink to="/store_manager_signup">Click Here to Register</RouterLink></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
    export default{
        name:'Store_Manager_Login',
        data(){
            return {
                show_error: false,
                msg: "",
                user_name: "",
                password: ""
            }
        },
        methods: {
            async send_credentials(e){
                e.preventDefault()
                if (this.user_name==="")
                {
                    this.msg='UserName cannot be empty!'
                    this.show_error=true
                    return
                }
                else if (this.password==="")
                {
                    this.msg='Password cannot be empty!'
                    this.show_error=true
                    return
                }
                let resp=await fetch("http://127.0.0.1:5000/api/store_manager_login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "user_name": this.user_name,
                        "password": this.password
                    })
                }).catch(this.handle_error)
                if (!resp)
                {return}
                let data=await resp.json()
                if (!resp.ok)
                {
                    this.msg=data['msg']
                    this.show_error=true
                    return
                }
                this.show_error=false
                this.$store.commit('set_data', data)
                this.$router.push('/store_manager_home')

            },
            handle_error(){
                this.msg="Some Error Occurred!"
                this.show_error=true
            }
        }
    }

</script>
