import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

function isWarning (alert) {
  return alert['type'] === 0
}

export default new Vuex.Store({
  state: {
    airData: null,
    alerts: null,
    filters: [
      {'name': 'Krytyczne', 'icon': 'warning', 'include': true},
      {'name': 'Policja', 'icon': 'info', 'include': true},
      {'name': 'Urząd Miasta', 'icon': 'stars', 'include': true}
    ]
  },
  getters: {
    getWarningAlerts (state) {
      console.log(state.alerts.filter(isWarning))
      return state.alerts.filter(isWarning)
    },
    getSortedAlerts (state) {
      var alerts = []
      var active = state.alerts.filter(a => a.expiration  === null).sort((a, b) => a.type - b.type)
      var inactive = state.alerts.filter(a => a.expiration  !== null).sort((a, b) => a.type - b.type)
      for (var alert of active) {
        alerts.push(alert)
        console.log(alert.type)
        alerts.push({divider: true, inset: true})
      }
      for (var ialert of inactive) {
        alerts.push(ialert)
        console.log(ialert.type)
        alerts.push({divider: true, inset: true})
      }
      alerts.pop()
      return alerts
    }
  },
  mutations: {
    setAirData (state, airData) {
      console.log('setting air data to ' + airData)
      state.airData = airData
      console.log(state.airData)
    },
    setAlerts (state, alerts) {
      console.log('setting alert to ' + alerts)
      state.alerts = alerts
      console.log(state.alerts)
    }
  },
  actions: {
  }
})
