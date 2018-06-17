<template>
  <v-layout column v-if="componentLoaded">
    <v-flex xs12>
      <AirCondition />
    </v-flex>

    <v-flex xs12>
      <Alerts />
    </v-flex>

    <v-flex xs12>
    </v-flex>
      <v-fab-transition>
        <v-btn
          color="#ff0000"
          dark
          fab
          fixed
          bottom
          right
          to="/proposal"
        >
          <v-icon>speaker_notes</v-icon>
        </v-btn>
      </v-fab-transition>
  </v-layout>
  <v-layout column v-else>
    <v-spacer></v-spacer>
    <v-flex xs12 text-xs-center align-center justify-center>
      <v-progress-circular
        :size="120"
        :width="10"
        indeterminate
        color="pink"
      >
      </v-progress-circular>
    </v-flex>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
// @ is an alias to /src
import { mapMutations, mapState } from 'vuex'
import axios from 'axios'

import AirCondition from '@/components/AirCondition.vue'
import Alerts from '@/components/Alerts.vue'

export default {
  name: 'home',
  mounted () {
    console.log('created home')
    if (this.airData === null || this.alerts === null) {
      axios.get('/api/status').then(response => {
        console.log('Success')
        console.log(response)
        this.setAirData(response.data)
        this.setAlerts(response.data['info'])
        this.componentLoaded = true
      }).catch(error => {
        console.log('Error')
        console.log(error)
      })
    } else {
      console.log('Data already in use')
      this.componentLoaded = true
    }
  },
  components: {
    AirCondition,
    Alerts
  },
  data () {
    return {
      componentLoaded: false
    }
  },
  computed: {
    ...mapState([
      'airData',
      'alerts'
    ])
  },
  methods: {
    ...mapMutations([
      'setAirData',
      'setAlerts'
    ])
  }
}
</script>

<style>
</style>
