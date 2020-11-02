<template>
  <div>
    <div id="app">
      <b-navbar type="light" variant="light" class="header" fixed="top"> <!-- the beginning is a navbar, in this case only for the look -->
        <b-navbar-brand>
          <a href="https://www.hellofresh.com.au/">
            <img src="../HelloFresh_Logo_Horizontal_V2.svg" alt="HelloFresh" height="42" />
          </a>
        </b-navbar-brand>
      </b-navbar>
    </div>
    <b-form-select v-model="selected" :options="items" value-field="text"></b-form-select> <!-- Here I create a form selector, thats permits to choose between weeks -->
    <div class="mt-3">
      Week selected :
      <strong>{{ selected }}</strong>
      <p></p>
    </div>
    <tableau v-bind:weeks="selected" /> <!-- Here I call the app "table", and give it the info "selected", that is what week I want to see the data of-->
  </div>
</template>

<script>
import tableau from './components/tableau.vue' // importing my compenent tableau
export default {
  data () {
    return {
      selected: '2018-W29', // by default, the week selected is the first one
      items: [] // I need to create the object items, Vue wouldn't let me create it in the mounted()
    }
  },
  components: {
    tableau // I have to tell Vue that I use tableau as a compenent
  },
  mounted () {
    fetch('http://127.0.0.1:5000/api/weeks', { // here I fetch the weeks I can choose from, directly from the api, this helps me avoid selecting weeks without data
      method: 'get' // I use the get method to do the query, although it was recommended, I didn't need axios
    })
      .then(response => {
        response.clone()
        return response.json()
      })
      .then(jsonData => {
        this.items = jsonData // the data I extracted will be registered in items
      })
  }
}
</script>

<style lang="scss">
#app {
  padding: 50px; // I added a padding, so that the navbar wouldn't hide the form selector
}
</style>
