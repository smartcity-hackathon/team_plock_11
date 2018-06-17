import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vuetify from 'vuetify'
import axios from 'axios'

import 'vuetify/dist/vuetify.min.css'
import './registerServiceWorker'

axios.defaults.baseURL = 'https://bc2665c6.ngrok.io'

Vue.use(Vuetify)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
