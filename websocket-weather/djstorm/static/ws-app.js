function load_app () {
  var locations = JSON.parse(document.getElementById('locations').textContent);
  locations = Vue.ref(locations);

  var ws_url = location.origin.replace("http", "ws") + "/ws";
  var ws = new WebSocket(ws_url);

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
    ws.send(JSON.stringify({"location": l.location}));
  }

  ws.onopen = () => {
    console.log("WebSocket opened");
  }

  ws.onmessage = (msg) => {
    var data = JSON.parse(msg.data);
    if (data.weather) {
      weather.value = data.weather;
      console.log('Loaded Weather:', data.weather);
    } else {
      console.log('Unhandled Message:', data);
    }
  }

  ws.onclose = () => {
    console.log("WebSocket closed");
  }

  Vue.createApp({
    setup() {
      return {locations, switch_locations, current_location, details, weather};
    }
  }).mount('#app');
}

load_app();
