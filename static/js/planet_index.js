// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

var planetName = document.getElementById('post-form').getAttribute('data-planet-name');
var page = 1;

// 스크롤시 post 비동기
$(window).scroll(function() {
  if ($(window).scrollTop() == $(document).height() - $(window).height()) {
    page++;
    loadPosts(page);
  }
});

// posts rendering 비동기 처리
function loadPosts(page) {

  $.ajax({
    url: '/planets/' + planetName + '/posts/',
    type: 'POST',
    data: {
        'page': page,
        'csrfmiddlewaretoken': csrftoken,
    },
    dataType: 'json',
    success: function(data) {
      for (var i = 0; i < data.length; i++) {
        var post = data[i];
        if (post === null) {
          $(window).off('scroll');
          return;
        }
        $('#post-list').append(createpostContainer(post.profile_image_url, post.nickname, post.created_time, post.content, post.tags, post.pk, post.image_url, post.user));
      }
    }
  });
}

// 스크롤 첫번째 실행
$(document).ready(function() {
  loadPosts(page);
});

// eventlistener
document.addEventListener('DOMContentLoaded', function() {
  // submit event
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    // 게시글 생성
    if (target.matches('#post-form')) {
      e.preventDefault();

      var form = e.target;
      var planetName = form.dataset.planetName;
      var formData = new FormData(form);
      formData.append('csrfmiddlewaretoken', csrftoken);

      axios({
        method: 'post',
        url: "/planets/" + planetName + "/create/",
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(function(response) {
        if (response.data.success) {
          var post_pk = response.data.post_pk;
          var postList = document.getElementById('post-list');
          var newPostContainer = createpostContainer(response.data.profile_image_url, response.data.nickname, response.data.created_time, response.data.content, response.data.tags, post_pk, response.data.image_url, response.data.user);
          postList.insertBefore(newPostContainer, postList.children[1]);
          form.reset();
        } else {
          var divIdContent = form.querySelector("#div_id_content");
          var newP = document.createElement("p");
          newP.id = "error_1_id_content";
          newP.className = "text-red-500 text-xs italic";

          var strongElement = document.createElement("strong");
          strongElement.textContent = JSON.parse(response.data.errors).content[0].message;
          newP.appendChild(strongElement);
          divIdContent.appendChild(newP);
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

  });

});


