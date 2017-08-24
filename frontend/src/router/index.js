import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index'

Vue.use(Router)

export default new Router({
  mode:'history', //hash => #
  routes: [
    {
      path: '/index',
      name: 'Index',
      component: Index
    },
    {
      path: '/',
      redirect: '/index'
    },
    {
      path: '*',
      redirect: '/index'
    }
  ]
})
