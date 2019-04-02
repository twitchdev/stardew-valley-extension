import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Panel from '@/components/Panel'
import Broadcaster from '@/components/Broadcaster'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/panel',
      name: 'Panel',
      component: Panel
    },
    {
      path: '/mobile',
      name: 'Mobile',
      component: Panel
    },
    {
      path: '/broadcaster',
      name: 'Broadcaster',
      component: Broadcaster
    }//,
  ]//,
  // mode: 'history'
})
