<template>
    <div class="container" style="background-color: wheat; padding: 10px; margin-top: 20px; border-radius: 10px;">
        <h2 style="padding: 10px;">Welcome to the Customer SignUp Page</h2>
        <br>
        <div v-if="show_error" class="alert alert-danger" role="alert">
            {{ msg }}
        </div>
        <div v-if="show_success" class="alert alert-success" role="alert">
            {{ msg }}
        </div>
        <form id="customer_signup">
            <div class="form-group row">
                <label for="f_name">First Name</label>
                <input v-model="first_name" type="text" class="form-control col" 
                   style="margin-left: 10px;" id="f_name" name="f_name"/>
                <div class="col"></div>
            </div>
            <div class="form-group row">
                <label for="l_name">Last Name</label>
                <input v-model="last_name" type="text" class="form-control col" 
                   style="margin-left: 10px;" id="l_name" name="l_name"/>
                <div class="col"></div>
            </div>
            <div class="form-group row">
                <label for="email">Email Id</label>
                <input v-model="email_id" type="text" class="form-control col" 
                   style="margin-left: 10px;" id="email" name="email"/>
                <div class="col"></div>
            </div>
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
                <button @click="create_account($event)" 
                    class="btn btn-outline-primary">SignUp</button>
            </div>
        </form>
        <div class="container" id="links" style="margin-top: 60px;">
            <div class="row">
                <div class="col">
                    <div class="badge bg-dark">
                        <h5>Registered Customer?</h5>
                        <p><RouterLink to="/customer_login">Click Here to Login</RouterLink></p>
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
                        <h5>Are you a Store Manager?</h5>
                        <p><RouterLink to="/store_manager_login">Click Here to Login</RouterLink></p>
                        <p><RouterLink to="/store_manager_signup">Click Here to Register</RouterLink></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
    export default{
        name:'Customer_Signup',
        data(){
            return {
                show_error: false,
                show_success: false,
                msg: "",
                email_id: "",
                first_name: "",
                last_name: "",
                user_name: "",
                password: ""
            }
        },
        methods: {
            async create_account(e){
                e.preventDefault()
                if (this.first_name==="")
                {
                    this.msg='First Name cannot Empty!'
                    this.show_success=false
                    this.show_error=true
                    return 
                }
                else if (this.email_id==="")
                {
                    this.msg='Email Id cannot be empty!'
                    this.show_success=false
                    this.show_error=true
                    return
                }
                else if (this.user_name==="")
                {
                    this.msg='UserName cannot be empty!'
                    this.show_success=false
                    this.show_error=true
                    return
                }
                else if (this.password==="")
                {
                    this.msg='Password cannot be empty!'
                    this.show_success=false
                    this.show_error=true
                    return
                }
                let resp=await fetch("http://127.0.0.1:5000/api/customer", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "first_name": this.first_name,
                        "last_name": this.last_name,
                        "email_id": this.email_id,
                        "user_name": this.user_name,
                        "password": this.password
                    })
                }).catch(this.handle_error)
                if (!resp)
                {return}
                let data=await resp.json()
                if (!resp.ok)
                {
                    this.show_success=false
                    this.msg=data['msg']
                    this.show_error=true
                    return
                }
                this.show_error=false
                this.msg=data['msg']
                this.show_success=true
                

            },
            handle_error(){
                this.show_success=false
                this.msg="Some Error Occurred!"
                this.show_error=true
            }
        }
    }

</script>
