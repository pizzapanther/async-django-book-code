function load_app () {
  var locations = JSON.parse(document.getElementById('locations').textContent);
  locations = Vue.ref(locations);

  var current_location = Vue.ref(null);
  var details = Vue.ref(null);
  var weather = Vue.ref(null);
  var client = null;
  var unsubscribe = null;

  var details = Vue.computed(() => {
    if (weather.value) {
      var details = WEATHER_CODES[weather.value.weather_code];
      if (weather.is_day) {
        return {icon: details['day'], label: details['label']};
      }

      return {icon: details['night'], label: details['label']};
    }
  });

  function on_next (msg) {
    console.log(msg.data.track_location);
    weather.value = msg.data.track_location;
  }

  function on_error (error) {
    console.error(error);

    if (unsubscribe) {
      unsubscribe();
      weather.value = null;
      current_location.value = null;
    }
  }

  function on_complete () {
    console.log('Completed');
  }

  function switch_locations (index) {
    var l = locations.value[index];
    current_location.value = l;
    weather.value = null;

    if (unsubscribe) {
      unsubscribe();
    }

    var url = location.origin.replace("http", "ws") + "/graphql";
    client = graphqlWs.createClient({url});
    var query = `subscription track {track_location(location: "${l.location[0]},${l.location[1]}")}`;
    unsubscribe = client.subscribe(
      {query},
      {next: on_next, error: on_error, complete: on_complete}
    );
  }

  Vue.createApp({
    setup() {
      return {locations, switch_locations, current_location, details, weather};
    }
  }).mount('#app');
}

load_app();
