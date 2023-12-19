function load_app () {
  var locations = JSON.parse(document.getElementById('locations').textContent);
  locations = Vue.ref(locations);
  var poll_url;
  var config = {headers: {'Content-Type': 'application/x-www-form-urlencoded'}};

  var event_source = null;
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

  function set_weather(msg) {
    var data = JSON.parse(msg.data);
    weather.value = data.weather;
  }

  function switch_locations (index) {
    var l = locations.value[index];
    current_location.value = l;
    weather.value = null;

    if (event_source) {
      event_source.close();
    }

    // Start Polling
    poll_url = `${location.origin}/weather/${l.location[0]},${l.location[1]}/`;
    axios.post(poll_url, {}, config)
      .then(receive_data)
      .catch((e) => {
        alert("Error retrieving weather");
        console.error(e);
      });
    // event_source = new EventSource(url);
    // event_source.addEventListener("weather", (msg) => {
    //   var data = JSON.parse(msg.data)
    //   console.log("Received:", Date.now(), data);
    //   weather.value = data;
    // });
  }

  function receive_data (response) {
    if (response.config.url == poll_url) {
      console.log("Received:", Date.now(), response.data);
      weather.value = response.data;

      axios.post(poll_url, {wait: 1}, config)
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
