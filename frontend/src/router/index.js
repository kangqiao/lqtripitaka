import Vue from 'vue'
import Router from 'vue-router'
import Tripitaka from '@/views/Tripitaka'
import DictSearch from '@/views/tripitaka/DictSearch'
import TripitakaSearch from '@/views/tripitaka/Search'
import TripitakaRead from '@/views/tripitaka/Read'

Vue.use(Router)

export default new Router({
  mode:'history', //hash => #
  routes: [
    {
      path: '/tripitaka',
      name: 'Tripitaka',
      component: Tripitaka,
      children:[
        {
          path: '', //默认打开的
          redirect: 'dict'
        },
        {
          path: 'dict',
          name: 'DictSearch',
          component: DictSearch
        },
        {
          path: 'search',
          name: 'TripitakaSearch',
          component: TripitakaSearch,
        },
        {
          path: 'read',
          name: 'TripitakaRead',
          component: TripitakaRead,
        },
      ]
    },
    {
      path: '/',
      redirect: '/tripitaka'
    }
  ]
})
