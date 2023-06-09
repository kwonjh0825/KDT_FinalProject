var weatherIcon = {
  '01': 'fas fa-sun',
  '02': 'fas fa-cloud-sun',
  '03': 'fas fa-cloud',
  '04': 'fas fa-cloud-meatball',
  '09': 'fas fa-cloud-sun-rain',
  '10': 'fas fa-cloud-showers-heavy',
  '11': 'fas fa-poo-storm',
  '13': 'far fa-snowflake',
  '50': 'fas fa-smog'
};

function getWeatherData(lat, lon) {
  var apiURI = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=b601f3a3c62f1f902a1a11a92d60a81d&lang=kr&units=metric`;

  $.ajax({
    url: apiURI,
    dataType: "json",
    type: "GET",
    async: "false",
    success: function (resp) {
      var $Icon = (resp.weather[0].icon).substr(0, 2);
      var $weather_description = resp.weather[0].main;
      var $Temp = Math.floor(resp.main.temp) + '°C';
      // var $humidity = '습도&nbsp;&nbsp;' + resp.main.humidity + ' %';
      // var $wind = '바람&nbsp;&nbsp;' + resp.wind.speed + ' m/s';
      // var $cloud = '구름&nbsp;&nbsp;' + resp.clouds.all + "%";
      var $temp_min = '최저&nbsp;&nbsp;' + Math.floor(resp.main.temp_min) + '°C';
      var $temp_max = '최고&nbsp;&nbsp;' + Math.floor(resp.main.temp_max) + '°C';

      $('.weather_icon').empty();
      $('.weather_description').empty();
      $('.current_temp').empty();
      // $('.humidity').empty();
      // $('.wind').empty();
      // $('.cloud').empty();
      $('.temp_min').empty();
      $('.temp_max').empty();

      $('.weather_icon').append('<i class="' + weatherIcon[$Icon] + ' fa-2x"></i>');
      $('.weather_description').prepend($weather_description);
      $('.current_temp').prepend($Temp);
      // $('.humidity').prepend($humidity);
      // $('.wind').prepend($wind);
      // $('.cloud').append($cloud);
      $('.temp_min').append($temp_min);
      $('.temp_max').append($temp_max);
    }
  });
}

var lat = 37.532600;
var lon = 127.024612;
getWeatherData(lat, lon);

function success(position) {
  var lat = position.coords.latitude;
  var lon = position.coords.longitude;
  getWeatherData(lat, lon);
}

function error(error) {
  console.log('weather error')
}

navigator.geolocation.getCurrentPosition(success, error);
