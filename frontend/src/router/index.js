import { createRouter, createWebHistory } from "vue-router";
import Customer_Login from "../components/customer/customer_login"

const routes=[
    {
        path: "/customer_login",
        name: "customer_login",
        component: Customer_Login
    },
    {
        path: "/",
        redirect: {
            path: "/customer_login"
        }
    }
]
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
  })

export default router