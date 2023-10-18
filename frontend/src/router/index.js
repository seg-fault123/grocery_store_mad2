import { createRouter, createWebHistory } from "vue-router";
import Customer_Home from "../components/customer/customer_home"
import Customer_Login from "../components/customer/customer_login"
import Page_Not_Found from "../components/page_not_found"

const routes=[
    {
        path: "/",
        redirect: {
            path: "/customer_login"
        }
    },
    {
        path: "/customer_home",
        name: "customer_home",
        component: Customer_Home
    },
    {
        path: "/customer_login",
        name: "customer_login",
        component: Customer_Login
    },
    {
        path: "/:pathMatch(.*)*",
        component: Page_Not_Found
    }
]
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
  })

export default router