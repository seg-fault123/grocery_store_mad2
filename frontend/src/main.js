import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import router from "./router"

const store = createStore({
    state(){
        return {
            id: null,
            first_name: null,
            last_name: null,
            email_id: null,
            user_name: null,
            access_token: null,
            role_id: null,
            role_name: null
        }
    },
    mutations: {
        set_data(state, payload){
            state.id=payload.id
            state.email_id=payload.email_id
            state.user_name=payload.user_name
            state.access_token=payload.access_token
            state.role_id=payload.role_id
            state.role_name=payload.role_name
            if (payload.role_name==='admin')
            {return}
            state.first_name=payload.first_name
            state.last_name=payload.last_name
        }
    }
})

createApp(App).use(store).use(router).mount('#app')
