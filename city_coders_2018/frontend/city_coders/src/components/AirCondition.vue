<template>
  <div id="air-panel">
    <div class="air-header text-xs-center">
      <v-icon color="white" large>label_important</v-icon>
      STAN POWIETRZA
    </div>
    <div class="stats">
        <v-layout row wrap align-content-start text-xs-center>
          <v-flex
            v-for="stat_data in statisticsData"
            :key="stat_data.key"
            class="stat"
            xs3
          >
            <div class="circle" :style="getAirColorStyle(airData.air_now[stat_data.key])">
              {{ airData.air_now[stat_data.key] * 100 | fixify }}%
            </div>
            <div class="air-condition-text" v-html="stat_data.name">
            </div>
          </v-flex>
          <v-flex xs3>
            <v-btn
              fab
              flat
              color="#cc324c"
              size="100px"
              class="map-button"
              to="/map"
            >
            <v-icon
              color="white"
              size="75px"
            >
              map
            </v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AirCondition',
  data () {
    return {
      statisticsData: [
        {'key': 'PM10', 'name': 'PM10'},
        {'key': 'PM2', 'name': 'PM2.5'},
        {'key': 'SO2', 'name': 'SO<sub>2</sub>'},
        {'key': 'C6H6', 'name': 'C<sub>6</sub>H<sub>6</sub>'},
        {'key': 'NO2', 'name': 'NO<sub>2</sub>'},
        {'key': 'O3', 'name': 'O<sub>3</sub>'},
        {'key': 'CO', 'name': 'CO'}
      ]
    }
  },
  computed: {
    ...mapState([
      'airData'
    ])
  },
  methods: {
    getAirColorStyle (airConditionLevel) {
      console.log(airConditionLevel)
      if (airConditionLevel < 0.51) {
        return {'backgroundColor': '#71D161'}
      } else if (airConditionLevel < 0.76) {
        return {'backgroundColor': '#006400'}
      } else if (airConditionLevel < 1.01) {
        return {'backgroundColor': '#ff7400'}
      } else if (airConditionLevel < 1.26) {
        return {'backgroundColor': '#ffc100'}
      } else {
        return {'backgroundColor': '#cc324c'}
      }
    }
  },
  filters: {
    fixify: function (value) {
      if (!value) return '0.00'
      return value.toFixed(2)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#air-panel {
  background-color: #e44a64;
  color: #ffffff;
  padding-bottom: 20px;
}
.air-header {
  font-size: 2em;
  background-color: #cc324c;
  padding: 30px 5px;
}

.stats {
  padding: 20px 0;
}

.stat {
  padding-top: 15px;
}

.circle {
  height: 70px;
  width: 70px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  text-align: center;
  vertical-align: middle;
  line-height: 70px;
  font-size: 1.2em;
  font-weight: bold;
}

.air-condition-text {
  margin-top: 15px;
  font-size: 1.25em;
  font-weight: bold;
}

.map-button {
  margin-top: 25px;
  text-align: center;
  vertical-align: middle;
}
</style>
