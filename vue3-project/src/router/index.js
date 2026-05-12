import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Profile from '../views/Profile.vue'
import Icons from '../views/Icons.vue'
import Tables from '../views/Tables.vue'
import Maps from '../views/Maps.vue'
import Part3 from '../views/Part3.vue'
import Part4 from '../views/Part4.vue'
import Part5 from '../views/Part5.vue'
import Part6 from '../views/Part6.vue'
import Part7 from '../views/Part7.vue'
import DashboardScreen from '../views/DashboardScreen.vue'
import Chat from '../views/Chat.vue'
import ProductDetail from '../views/ProductDetail.vue'
import PredictView from '../views/PredictView.vue'
import ClusteringView from '../views/ClusteringView.vue'

const routes = [
  {
    path: '/',
    redirect: '/Login'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
 {
    path:'/profile',
    name:'Profile',
    component:Profile
 },
 {
    path:'/tables',
    name:'Tables',
    component:Tables
 },
 {
    path:'/icons',
    name:'Icons',
    component:Icons
 },
 {
    path:'/maps',
    name:'Maps',
    component:Maps
 },
 {
    path:'/part3',
    name:'Part3',
    component:Part3
 },
 {
    path:'/part4',
    name:'Part4',
    component:Part4
 },
 {
    path:'/part5',
    name:'Part5',
    component:Part5
 },
 {
    path:'/part6',
    name:'Part6',
    component:Part6
 },
 {
    path:'/part7',
    name:'Part7',
    component:Part7
 },
 {
    path:'/dashboard-screen',
    name:'DashboardScreen',
    component:DashboardScreen
 },
 {
    path:'/chat',
    name:'Chat',
    component:Chat
 },
 {
    path:'/product/:id',
    name:'ProductDetail',
    component:ProductDetail
 },
 {
    path:'/predict',
    name:'PredictView',
    component:PredictView
 },
 {
    path:'/clustering',
    name:'ClusteringView',
    component:ClusteringView
 },

]

const router = createRouter({
    history:createWebHistory(),
    routes
})

export default router