import { createRouter, createWebHistory } from "vue-router";
import Customer_Add_to_Cart from "../components/customer/customer_add_to_cart"
import Customer_Buy_Now from "../components/customer/customer_buy_now"
import Customer_Home from "../components/customer/customer_home"
import Customer_Login from "../components/customer/customer_login"
import Customer_Orders from "../components/customer/customer_orders"
import Page_Not_Found from "../components/page_not_found"
import Order_Summary from "../components/customer/order_summary"

const routes=[
    {
        path: "/",
        redirect: {
            path: "/customer_login"
        }
    },
    {
        path: "/customer/add_to_cart/:p_id(\\d+)",
        component: Customer_Add_to_Cart,
        props: true
    },
    {
        path: "/customer/buy_now/:p_id(\\d+)",
        component: Customer_Buy_Now,
        props: true
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
        path: "/customer_orders",
        name: "previous_orders",
        component: Customer_Orders
    },
    {
        path: "/customer/order_summary/:o_id(\\d+)",
        component: Order_Summary,
        props: true
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