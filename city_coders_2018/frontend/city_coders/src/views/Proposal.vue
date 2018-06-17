<template>
  <v-layout row wrap text-xs-center>
    <v-flex xs12>
      <div class="proposal-title">
        Zgłoś problem
      </div>
    </v-flex>
    <v-flex xs12>
      <v-text-field
          name="input-7-1"
          placeholder="Opisz zaistniałą sytuację..."
          color="#d1d1d1"
          flat
          dark
          full-width
          multi-line
      ></v-text-field>
    </v-flex>
    <v-flex xs12>
      <v-btn
        block
        dark
      >
      <v-icon style="padding: 7px">camera_alt</v-icon>
      Dodaj Zdjęcie
      </v-btn>
    </v-flex>
    <v-flex xs5>
      <v-btn
        block
        flat
        to="/"
      >
        Powrót
      </v-btn>
    </v-flex>
    <v-flex xs5 offset-xs2>
      <v-btn
        block
        flat
        to="/"
      >
        Wyślij
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'proposal',
  data () {
    return {
    }
  }
}
</script>

<style>
.row {
  margin: 0 20px;
  color: #ffffff;
}

.proposal-title {
  background-color: #1d1d1d;
  padding: 10px 20px;
  margin-top: 20px;
  font-size: 2em;
}
</style>
