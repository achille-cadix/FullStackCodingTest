<template>
  <div>
    <b-table striped hover :items="items" :fields="fields" :sort-by="sortBy"></b-table>
  </div>
</template>

<script>
export default {
  props: { weeks: String }, // a prop is coming from App : the week I need to get data from
  data () {
    return {
      items: [],
      sortBy: 'name', // by default, the data will be sorted by name
      fields: [
        // I need to fill the fields with the names of the data in order to use b-table
        {
          key: 'name',
          label: 'Name',
          sortable: true,
          sortDirection: 'desc'
        },
        {
          key: 'quantity',
          label: 'volume',
          sortable: true,
          sortDirection: 'desc'
        },
        {
          key: 'sku',
          label: 'SKU number',
          sortable: true,
          sortDirection: 'desc'
        }
      ]
    }
  },
  mounted () {
    fetch('http://127.0.0.1:5000/api/Volume/2018-W29', {
      // by default, the query is '2018-W29'
      method: 'get'
    })
      .then(response => {
        response.clone()
        return response.json()
      })
      .then(jsonData => {
        this.items = jsonData
      })
  },
  watch: {
    // watch means that the functions will be activated when a value changes
    weeks: {
      // in our case, the value I am watching for is weeks, since   it's what's changing from app
      immediate: true,
      handler () {
        // the handler is the function ran when the value of weeks changes
        fetch('http://127.0.0.1:5000/api/Volume/' + this.weeks, {
          // I happend the name of the week into the url of the query, so I get the good data coming from the backend
          method: 'get'
        })
          .then(response => {
            response.clone()
            return response.json()
          })
          .then(jsonData => {
            this.items = jsonData
          })
      }
    }
  }
}
</script>
