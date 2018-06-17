<template>
  <div id="alerts-panel">
    <!-- krytyczne komunikaty -->
    <v-card class="warning-panel" dark color="#394263">
      <v-container
        fluid
        style="min-height: 0;"
        grid-list-lg
      >
        <v-layout row wrap>
          <v-flex xs12>
            <v-card >
              <v-card-title
                class="dark-background"
                primary-title
              >
                <div class="headline white--text">
                  <v-icon
                    large
                    color="#e44a64"
                    class="warning-icon"
                  >
                    report_problem
                  </v-icon>
                  Komunikaty
                </div>
              </v-card-title>
              <v-card-actions
                v-if="warningAlert"
                class="warning-message"
               @click="$router.push('/alert/' + warningAlert.id)"
               >
                {{ warningAlert.title }}
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>

    <v-layout row>
      <v-flex xs12>
        <v-card dark color="#394263">
          <v-list three-line>
            <template v-for="(item, index) in sortedAlerts">
              <v-divider
                v-if="item.divider"
                :inset="item.inset"
                :key="index"
              >
              </v-divider>
                <v-list-tile
                  v-else
                  :key="item.title"
                  :disabled="item.expiration !== null"
                  avatar
                  @click="$router.push('/alert/' + item.id)"
                >
                <v-list-tile-avatar>
                  <!--
                  <img :src="getIconSRC(alert)">
                  -->
                  <v-icon :color="getIconColor(item)">
                    {{getIconSRC(item)}}
                  </v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
            </template>
          </v-list>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>

import { mapState, mapGetters } from 'vuex'

export default {
  name: 'Alerts',
  computed: {
    ...mapState([
      'alerts'
    ]),
    ...mapGetters({
      sortedAlerts: 'getSortedAlerts'
    }),
    warningAlert () {
      let alertId = this.$route.query.alert_id
      console.log('got alert_id = ' + alertId)
      if (alertId) {
        var alert = this.alerts.filter(item => item['id'] == alertId)[0]
        alert.include = true
        return alert
      }
      return null
    }
  },
  methods: {
    getIconColor (alert) {
      let type = alert['type']
      if (type === 3) {
        return 'orange'
      } else if (type === 2) {
        return 'yellow'
      }
      return 'red'
    },
    getIconSRC (alert) {
      let type = alert['type']
      if (type === 3) {
        return 'new_releases'
      } else if (type === 2) {
        return 'priority_high'
      }
      return 'report_problem'
    }
  }
}
</script>
<style scoped>
#alerts-panel {
}

.dark-background {
  background-color: #1d1d1d;
}

.warning-icon {
  color: #e44a64 !important;
  margin: 0 15px;
}

.warning-message {
  padding: 30px 20px !important;
  font-size: 1.25em;
  background-color: #e44a64;
}
</style>
