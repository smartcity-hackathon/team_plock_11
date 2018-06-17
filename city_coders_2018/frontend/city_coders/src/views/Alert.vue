<template>
  <v-layout row wrap text-xs-center>
      <v-container
        fluid
        style="min-height: 0;"
        v-if="alert != undefined"
        grid-list-lg
      >
        <v-layout row wrap>
          <v-flex xs12>
            <v-card >
              <v-card-title class="dark-background" primary-title>
                <div class="headline white--text">
                  <v-icon
                    large
                    color="#e44a64"
                    class="warning-icon"
                    :style="getIconColor(alert)"
                  >
                    report_problem
                  </v-icon>
                    {{ alert.title }}
                </div>
              </v-card-title>
              <v-card-actions class="warning-message">
                {{ alert.text }}
              </v-card-actions>
            </v-card>
          </v-flex>
          <v-fab-transition>
            <v-btn
              color="#ff0000"
              style="background-color: #cc324c;"
              dark
              fab
              fixed
              top
              left
              to="/"
            >
              <v-icon>keyboard_arrow_left</v-icon>
            </v-btn>
          </v-fab-transition>
        </v-layout>
      </v-container>
    <v-flex xs12 v-else>
      Przeprzaszamy, podany alert nie istnieje lub wygasł..
    </v-flex>
  </v-layout>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'alert',
  data () {
    return {
    }
  },
  computed: {
    ...mapState([
      'alerts'
    ]),
    alert () {
      console.log('alertID = ' + this.$route.params.alertId)
      var alert = this.getAlertByID(this.$route.params.alertId)
      console.log(alert)
      return alert
    }
  },
  methods: {
    getAlertByID (id) {
      return this.alerts.filter(item => item.id == id)[0]
    },
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
.container {
  padding: 10px 10px;
}
.dark-background {
  background-color: #e44a64;
}

.warning-icon {
  margin: 0 15px;
}

.warning-message {
  padding: 30px 20px !important;
  font-size: 1.25em;
}
</style>
