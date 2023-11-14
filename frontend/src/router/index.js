import { createRouter, createWebHistory } from "vue-router";

import Admin_Add_Category from "../components/admin/admin_add_category"
import Admin_Edit_Category from "../components/admin/admin_edit_category"
import Admin_Category from "../components/admin/admin_category"
import Admin_Categories from "../components/admin/admin_categories"
import Admin_Category_Requests from "../components/admin/admin_category_requests"
import Admin_Delete_Category_Requests from "../components/admin/admin_delete_category_requests"
import Admin_Edit_Category_Requests from "../components/admin/admin_edit_category_requests"
import Admin_New_Category_Requests from "../components/admin/admin_new_category_requests"
import Admin_New_Store_Managers from "../components/admin/admin_new_store_managers"
import Admin_Home from "../components/admin/admin_home"
import Admin_Login from "../components/admin/admin_login"

import Customer_Add_to_Cart from "../components/customer/customer_add_to_cart"
import Customer_Buy_Now from "../components/customer/customer_buy_now"
import Customer_Cart from "../components/customer/customer_cart"
import Customer_Edit_Cart from "../components/customer/customer_edit_cart"
import Customer_Home from "../components/customer/customer_home"
import Customer_Login from "../components/customer/customer_login"
import Customer_Orders from "../components/customer/customer_orders"
import Customer_Search from "../components/customer/customer_search"
import Customer_Signup from "../components/customer/customer_signup"
import Page_Not_Found from "../components/page_not_found"
import Order_Summary from "../components/customer/order_summary"

import Store_Manager_Add_Category from "../components/store_manager/store_manager_add_category"
import Store_Manager_Edit_Category from "../components/store_manager/store_manager_edit_category"
import Store_Manager_Category from "../components/store_manager/store_manager_category"
import Store_Manager_Categories from "../components/store_manager/store_manager_categories"
import Store_Manager_Home from "../components/store_manager/store_manager_home"
import Store_Manager_Login from "../components/store_manager/store_manager_login"
import Store_Manager_Add_Product from "../components/store_manager/store_manager_add_product"
import Store_Manager_Edit_Product from "../components/store_manager/store_manager_edit_product"
import Store_Manager_Product from "../components/store_manager/store_manager_product"
import Store_Manager_Products from "../components/store_manager/store_manager_products"
import Store_Manager_Signup from "../components/store_manager/store_manager_signup"


const routes=[
    {
        path: '/admin/add_category',
        component: Admin_Add_Category,
    },
    {
        path: '/admin/edit_category/:cat_id(\\d+)',
        component: Admin_Edit_Category,
        props: true
    },
    {
        path: "/admin/category/:cat_id(\\d+)",
        component: Admin_Category,
        props: true
    },
    {
        path: "/admin/categories",
        component: Admin_Categories
    },
    {
        path: '/admin/category_requests',
        component: Admin_Category_Requests
    },
    {
        path: '/admin/delete_category_requests',
        component: Admin_Delete_Category_Requests
    },
    {
        path: '/admin/edit_category_requests',
        component: Admin_Edit_Category_Requests
    },
    {
        path: '/admin/new_category_requests',
        component: Admin_New_Category_Requests
    },
    {
        path: '/admin/new_store_managers',
        component: Admin_New_Store_Managers
    },
    {
        path: "/admin_home",
        component: Admin_Home
    },
    {
        path: "/admin_login",
        component: Admin_Login
    },
    
    
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
        path: "/customer_cart",
        component: Customer_Cart
    },
    {
        path: "/customer/edit_cart/:p_id(\\d+)",
        component: Customer_Edit_Cart,
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
        path: "/customer_search",
        component: Customer_Search
    },
    {
        path: "/customer_signup",
        component: Customer_Signup
    },


    {
        path: "/store_manager/add_category",
        component: Store_Manager_Add_Category
    },
    {
        path: "/store_manager/edit_category/:cat_id(\\d+)",
        component: Store_Manager_Edit_Category,
        props: true
    },
    {
        path: "/store_manager/category/:cat_id(\\d+)",
        component: Store_Manager_Category,
        props: true
    },
    {
        path: "/store_manager/categories",
        component: Store_Manager_Categories
    },

    {
        path: "/store_manager_home",
        component: Store_Manager_Home
    },

    {
        path: "/store_manager_login",
        component: Store_Manager_Login
    },
    {
        path: "/store_manager/add_product",
        component: Store_Manager_Add_Product
    },
    {
        path: "/store_manager/edit_product/:p_id(\\d+)",
        component: Store_Manager_Edit_Product,
        props: true
    },
    {
        path: "/store_manager/product/:p_id(\\d+)",
        component: Store_Manager_Product,
        props: true
    },
    {
        path: "/store_manager/products",
        component: Store_Manager_Products
    },
    {
        path: "/store_manager_signup",
        component: Store_Manager_Signup
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