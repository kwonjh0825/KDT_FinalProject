var planetName = document
  .getElementById('post-form')
  .getAttribute('data-planet-name');
var page = 1;

// 스크롤시 post 비동기
$(window).scroll(function () {
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
      page: page,
      csrfmiddlewaretoken: csrftoken,
    },
    dataType: 'json',

    success: function (data) {
      for (var i = 0; i < data.length; i++) {
        var post = data[i];

        if (post === null) {
          $(window).off('scroll');
          return;
        }

        $('#post-list').append(
          createpostContainer(
            post.profile_image_url,
            post.nickname,
            post.created_time,
            post.content,
            post.tags,
            post.pk,
            post.image_url,
            post.user,
            post.votetopics,
            post.post_emote_heart,
            post.post_emote_thumbsup,
            post.post_emote_thumbsdown,
            post.vote_count,
            post.voted
          )
        );
      }
    },
  });
}

// 스크롤 첫번째 실행
$(document).ready(function () {
  loadPosts(page);
});