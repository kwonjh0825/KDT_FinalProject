var weatherIcon = {
  '01': 'fas fa-sun',
  '02': 'fas fa-cloud-sun',
  '03': 'fas fa-cloud',
  '04': 'fas fa-cloud-meatball',
  '09': 'fas fa-cloud-sun-rain',
  10: 'fas fa-cloud-showers-heavy',
  11: 'fas fa-poo-storm',
  13: 'far fa-snowflake',
  50: 'fas fa-smog',
};

function getWeatherData(lat, lon) {
  var apiURI = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=b601f3a3c62f1f902a1a11a92d60a81d&lang=kr&units=metric`;

  $.ajax({
    url: apiURI,
    dataType: 'json',
    type: 'GET',
    async: 'false',
    success: function (resp) {
      var $Icon = resp.weather[0].icon.substr(0, 2);
      var $weather_description = resp.weather[0].main;
      var $Temp = Math.floor(resp.main.temp) + '°C';
      // var $humidity = '습도&nbsp;&nbsp;' + resp.main.humidity + ' %';
      // var $wind = '바람&nbsp;&nbsp;' + resp.wind.speed + ' m/s';
      // var $cloud = '구름&nbsp;&nbsp;' + resp.clouds.all + "%";
      var $temp_min =
        '최저&nbsp;&nbsp;' + Math.floor(resp.main.temp_min) + '°C';
      var $temp_max =
        '최고&nbsp;&nbsp;' + Math.floor(resp.main.temp_max) + '°C';

      $('.weather_icon').empty();
      $('.weather_description').empty();
      $('.current_temp').empty();
      // $('.humidity').empty();
      // $('.wind').empty();
      // $('.cloud').empty();
      $('.temp_min').empty();
      $('.temp_max').empty();

      $('.weather_icon').append(
        '<i class="' + weatherIcon[$Icon] + ' fa-2x"></i>'
      );
      $('.weather_description').prepend($weather_description);
      $('.current_temp').prepend($Temp);
      // $('.humidity').prepend($humidity);
      // $('.wind').prepend($wind);
      // $('.cloud').append($cloud);
      $('.temp_min').append($temp_min);
      $('.temp_max').append($temp_max);
    },
  });
}

var lat = 37.5326;
var lon = 127.024612;
getWeatherData(lat, lon);

function success(position) {
  var lat = position.coords.latitude;
  var lon = position.coords.longitude;
  getWeatherData(lat, lon);
}

function error(error) {
  console.log('weather error');
}

navigator.geolocation.getCurrentPosition(success, error);

const voteToggle = document.getElementById('vote-toggle');
const voteTopicsContainer = document.getElementById('vote-topics-container');
const voteTopics = document.getElementById('vote-topics');

voteToggle.addEventListener('click', function () {
  const computedStyle = window.getComputedStyle(voteTopicsContainer);
  console.log(computedStyle);
  if (computedStyle.display === 'none') {
    console.log('hi');
    voteTopicsContainer.style.display = 'block';
  } else {
    console.log('bye');
    // 이미지를 클릭하여 폼을 숨기는 경우, 첫 번째 주제를 제외한 나머지 주제를 삭제합니다.
    const topicInputs = voteTopics.querySelectorAll('.vote-topic-input');
    for (let i = topicInputs.length - 1; i > 0; i--) {
      topicInputs[i].remove();
    }

    voteTopicsContainer.style.display = 'none';
    console.log('ㅎㅇㅎㅇ');
  }
});

const plusButton = document.getElementById('plus-button');

plusButton.addEventListener('click', function () {
  console.log('플러스!');
  event.preventDefault(); // 폼 제출 방지
  const newTopicInput = document.createElement('input');
  newTopicInput.type = 'text';
  newTopicInput.name = 'title';
  newTopicInput.classList.add(
    'block',
    'mt-2',
    'w-full',
    'bg-[#101013]',
    'text-white',
    'rounded-lg',
    'py-2',
    'px-3'
  );

  const deleteButton = document.createElement('button');
  deleteButton.textContent = '-';
  deleteButton.setAttribute('class', 'delete-button');
  deleteButton.addEventListener('click', function () {
    voteTopics.removeChild(newTopicInput.parentNode);
  });

  const inputWrapper = document.createElement('div');
  inputWrapper.setAttribute('class', 'vote-topic-input');
  inputWrapper.appendChild(newTopicInput);
  inputWrapper.appendChild(deleteButton);

  voteTopics.appendChild(inputWrapper);
});
