<template>
  <div id="app">
    <v-app dark>
      <router-view/>
      <!--
      <v-footer height="auto" class="grey darken-3">
        <v-layout row wrap justify-center>
          <v-btn
            v-for="(filter, index) in filters"
            :key="filter.name"
            color="white"
            @click="toggleFilter(index)"
            icon
            large
            flat
          >
            <v-icon>{{ filter.icon }}</v-icon>
          </v-btn>
        </v-layout>
      </v-footer>
      -->
    </v-app>
  </div>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

export default {
  data () {
    return {
    }
  },
  computed: {
    ...mapState([
      'filters'
    ])
  },
  methods: {
    ...mapMutations([
      'toggleFilter'
    ])
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
