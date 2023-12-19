function load_app () {
  var locations = JSON.parse(document.getElementById('locations').textContent);
  locations = Vue.ref(locations);
  var poll_url;
  var config = {headers: {'Content-Type': 'application/x-www-form-urlencoded'}};

  var current_location = Vue.ref(null);
  var details = Vue.ref(null);
  var weather = Vue.ref(null);

  var details = Vue.computed(() => {
    if (weather.value) {
      var details = WEATHER_CODES[weather.value.weather_code];
      if (weather.is_day) {
        return {icon: details['day'], label: details['label']};
      }

      return {icon: details['night'], label: details['label']};
    }
  });

  function switch_locations (index) {
    var l = locations.value[index];
    current_location.value = l;
    weather.value = null;

    // Start Polling
    poll_url = `${location.origin}/weather/${l.location[0]},${l.location[1]}/`;
    axios.post(poll_url, {}, config)
      .then(receive_data)
      .catch((e) => {
        alert("Error retrieving weather");
        console.error(e);
      });
  }

  function receive_data (response) {
    if (response.config.url == poll_url) {
      console.log("Received:", Date.now(), response.data);
      weather.value = response.data.weather;

      axios.post(poll_url, {last_id: response.data.id}, config)
        .then(receive_data)
        .catch((e) => {
          alert("Error retrieving weather");
          console.error(e);
        });
    }
  }

  Vue.createApp({
    setup() {
      return {locations, switch_locations, current_location, details, weather};
    }
  }).mount('#app');
}

load_app();
