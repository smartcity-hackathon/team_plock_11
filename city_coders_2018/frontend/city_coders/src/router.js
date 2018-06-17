import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Proposal from './views/Proposal.vue'
import Map from './views/Map.vue'
import Alert from './views/Alert.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/map',
      name: 'map',
      component: Map
    },
    {
      path: '/proposal',
      name: 'proposal',
      component: Proposal
    },
    {
      path: '/alert/:alertId',
      name: 'alert',
      component: Alert
    }
  ]
})
