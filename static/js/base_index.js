function scrollTopFixed() {
  window.scrollTo(0, 0);
}

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

navigator.geolocation.getCurrentPosition(success);

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('click', function (e) {
    var target = e.target;

    // 즐겨찾기
    if (target.matches('#star')) {
      e.preventDefault();

      var starButton = target;
      var planetName = starButton.dataset.planetName;
      var value = starButton.value;

      axios({
        url: "/planets/" + planetName + "/star/",
        method: 'POST',
        data: value,
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          if (response.data.star) {
            target.classList.remove('fa-regular')
            target.classList.add('fa-solid')
            document.querySelector('#star-content').textContent = "행성 즐겨찾기에서 제거"
          }
          else {
            target.classList.remove('fa-solid')
            target.classList.add('fa-regular')
            document.querySelector('#star-content').textContent = "행성 즐겨찾기에 추가"
          }
        } else {
          console.error('Star failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

  });
  
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    // 메모 생성
    if (target.matches('#create-memo-form')) {
      e.preventDefault();

      var createForm = target;
      var updateButton = createForm.querySelector('#update-memo-button');
      var indexmemoDiv = createForm.closest('#index-memo');
      var planetName = createForm.dataset.planetName;
      var formData = new FormData(createForm);

      axios({
        url: "/planets/" + planetName + "/memo/",
        method: 'POST',
        data: formData,
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          var memo = response.data.memo;
          var memoDiv = document.createElement('div');
          memoDiv.id = "memo";
          var memocontentDiv = document.createElement('div');
          memocontentDiv.id = "memo-content";
          memocontentDiv.textContent = memo;
          var formElement = document.createElement('form');
          formElement.id = "update-memo-form";
          formElement.setAttribute("data-planet-name", planetName);
          memoDiv.append(formElement);
          var button = document.createElement('button');
          button.id = "update-memo-button";
          button.textContent = "메모 편집"
          button.setAttribute("data-planet-name", planetName);
          formElement.append(button)
          memoDiv.append(memocontentDiv);
          memoDiv.append(formElement);
          indexmemoDiv.querySelector('#create-memo-form').remove();
          indexmemoDiv.append(memoDiv);
        } else {
          console.error('Memo failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

    // 메모 수정 form
    else if (target.matches('#update-memo-form')) {
      e.preventDefault();

      var updateForm = target;
      var updatebutton = target;
      var indexmemoDiv = updateForm.closest('#index-memo');
      var planetName = updatebutton.dataset.planetName;
      var formData = new FormData(updateForm);

      axios({
        url: "/planets/" + planetName + "/memo/",
        method: 'POST',
        data: formData,
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          indexmemoDiv.querySelector('#memo').style.display = "none";
          var memoform = response.data.memoform;
          var formContainer = document.createElement('div');
          formContainer.innerHTML = memoform;
          var formElement = document.createElement('form');
          formElement.id = "edit-memo-form";
          formElement.setAttribute("data-planet-name", planetName);
          formElement.appendChild(formContainer);
          var submitButton = document.createElement('button');
          submitButton.id = "edit-post-button";
          submitButton.textContent = '메모 수정';
          submitButton.type = 'submit';
          formElement.append(submitButton);
          indexmemoDiv.append(formElement);
        } else {
          console.error('Memo failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

    // 메모 수정 처리
    else if (target.matches('#edit-memo-form')) {
      e.preventDefault();

      var updateForm = target;
      var updatebutton = target;
      var indexmemoDiv = updateForm.closest('#index-memo');
      var planetName = updatebutton.dataset.planetName;
      var formData = new FormData(updateForm);

      axios({
        url: "/planets/" + planetName + "/memo/",
        method: 'POST',
        data: formData,
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          var memoDiv = indexmemoDiv.querySelector('#memo')
          memoDiv.style.display = "block";
          document.querySelectorAll('#memo-content').forEach(e => e.textContent = response.data.memo);
          document.querySelectorAll('#edit-memo-form').forEach(e => e.remove());
          document.querySelectorAll('#edit-memo-button').forEach(e => e.remove());
        } else {
          console.error('Memo failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

  });
});

