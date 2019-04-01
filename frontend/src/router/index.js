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
      path: '/panel.html',
      name: 'Panel',
      component: Panel
    },
    {
      path: '/broadcaster.html',
      name: 'Broadcaster',
      component: Broadcaster
    },
  ],
  mode: 'history'
})
