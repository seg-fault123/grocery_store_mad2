<template>
    <div class="container">
        <h2 style="padding: 10px">Welcome to the Customer Login Page</h2>
        <div v-if="show_error" class="alert alert-danger" role="alert">
            {{ msg }}
        </div>
        <form id="customer_login">
            <div class="form-group">
                <label for="user_name">UserName</label>
                <input v-model="user_name" type="text" class="form-control" 
                    id="user_name" name="user_name"/>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input v-model="password" type="password" class="form-control"
                    id="password" name="password">
            </div>
            <div style="margin-top: 10px;">
                <button @click="send_credentials($event)" 
                    class="btn btn-outline-primary">Login</button>
            </div>
        </form>
    </div>
</template>

<script>
    export default{
        name:'Customer_Login',
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
                let resp=await fetch("http://127.0.0.1:5000/api/customer_login", {
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
                

            },
            handle_error(){
                this.msg="Some Error Occurred!"
                this.show_error=true
            }
        }
    }

</script>

