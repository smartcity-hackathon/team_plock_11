<template>
  <div class='about'>
    <div id='map'>
        <div class='leaflet-top leaflet-right'>
        <img id='wind_direction' style='margin-right: 20px; margin-top: 20px; width: 100px; height: 100px; transform: rotate(0deg);' src='wind.png' />
        </div>
    </div>
    <div id='timeline'></div>
  </div>
</template>
<script>
import { mapState } from 'vuex'

export default {
  name: 'map-component',
  mounted () {
      this.initMap()
  },
  computed: {
    ...mapState([
      'airData'
    ])
  },
  methods: {
    initMap () {
      var map = L.map('map')
        var plockMap = new function () {

          map.setView([52.55265635, 19.7065364], 10)
          L.tileLayer.provider('HERE.terrainDay', {
            app_id: 'SB9ji04wqMxRAhlvKmgK',
            app_code: 'Xo2D-bz5LszAkbLOz1qH2w'
          }).addTo(map)

          this.wind_direction = document.getElementById('wind_direction')
          console.log(this.wind_direction)
          var timeline = new vis.Timeline(document.getElementById('timeline'), null, {
            width:  '100%',
            height: '70px',
            zoomMax: 86400000 * 90,
            zoomMin: 3600 * 60000
          })
          timeline.addCustomTime(new Date(), 1)

          var timeline_follow_checkbox = document.getElementById('timeline_follow_checkbox')
          var current_follow_checkbox = document.getElementById('current_follow_checkbox')

          timeline.on('click', function onTimelineClick(event) {
            timeline.setCustomTime(event.time, 1)
            var go_to_time = 0
            for(var time in plockMap.data['air']) {
              if(new Date(time * 1000) < event.time || go_to_time == 0) {
                go_to_time = time
              }
            }
            plockMap.updateHeatmap(go_to_time)
          })

          timeline.on('timechange', function onCustomTimeChange(properties) {
            var go_to_time = 0
            for(var time in plockMap.data['air']) {
              if(new Date(time * 1000) < properties.time || go_to_time == 0) {
                go_to_time = time
              }
            }
            plockMap.updateHeatmap(go_to_time)
          })
          console.log('timeline setupd')

          // heatmap
          var heatmap = L.webGLHeatmap({
            units: 'm',
            size: 3000,
            alphaRange: 0.1,
            opacity: 0.5
          })
          map.addLayer(heatmap)

          console.log('defining setDta')
          this.setData = function (data) {
            console.log('setting data')
            console.log(data)
            plockMap.data = data
            console.log('data set')

            var timeline_data = []
            var prev_time = null
            var first_time = null

            for(var time in plockMap.data['air']) {
              if(!prev_time) {
              console.log('in if time ' + time)
                prev_time = time
                first_time = time
                continue
              }
              console.log('some time ' + time)
              timeline_data.push({className: 'positive', type: 'background', start: new Date(prev_time * 1000), end: new Date(time * 1000)})
              prev_time = time
            }
            console.log('sfter fucking for')
            timeline.setItems(new vis.DataSet(timeline_data))
            timeline.setCustomTime(timeline_data[timeline_data.length - 1].end, 1)
            timeline.moveTo(timeline_data[timeline_data.length - 1].end)
            timeline.setOptions({
              'min': new Date(timeline_data[0].start.getTime() - 86400000),
              'max': new Date(timeline_data[timeline_data.length - 1].end.getTime() + 86400000)
            })
            timeline.fit()

            this.updateHeatmap(first_time)
          }

          this.updateHeatmap = function(time) {
            var heatData = []
            plockMap.data['air'][time].forEach(function(el) {
              heatData.push([plockMap.data['stations'][el[0]][0], plockMap.data['stations'][el[0]][1], 10000, el[1] / 30])
            })
            heatmap.setData(heatData)
            plockMap.wind_direction.style.transform = 'rotate(' + (plockMap.data['wind'][time] -  45) + 'deg)'
          }
        }()
        plockMap.setData(this.airData)
      }
  }
}
</script>
<style scoped>
</style>
