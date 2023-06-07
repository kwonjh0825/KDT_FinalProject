// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

var planetName = document.getElementById('comment-create-form').getAttribute('data-planet-name');
var postPk = document.getElementById('comment-create-form').getAttribute('data-post-pk');

if (requestuser_nickname != document.getElementById('post-nickname').textContent) {
  document.getElementById('dropdown-menu').querySelector('li#dropdown-delete').style.display = 'none';
}

// comments, recomments rendering 비동기 처리
function loadComments(page) {
  $.ajax({
    url: '/planets/' + planetName + '/' + postPk + '/comments/',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      for (var i = 0; i < data.length; i++) {
        var comment = data[i];
        if (comment === null) {
          $(window).off('scroll');
          return;
        }
        createcommentContainer(comment.profile_image_url, comment.nickname, comment.created_time, comment.content, comment.pk, comment.user, comment.recomments);
      }
    }
  });
}

// 스크롤 첫번째 실행
$(document).ready(function() {
  loadComments(page);
});

// 댓글 생성 container
function createcommentContainer(profile_image_url, nickname, created_time, content, comment_pk, user, recomments) {
  var newCommentContainer = document.getElementById('container').cloneNode(true);
  var commentSection = newCommentContainer.querySelector('#section')
  commentSection.style.display = 'flex';
  var newDiv = document.createElement('div');
  newDiv.innerHTML = `<svg width="30px" height="30px" id="Capa_1" style="enable-background:new 0 0 74.5 60;" version="1.1" viewBox="0 0 74.5 60" width="74.5px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g><path d="M10,45h40.5v15l24-22l-24-22v15H14V0H0v35C0,40.523,4.477,45,10,45z" fill="#ffffff"/></g></svg>`;
  newCommentContainer.classList = 'bg-[#282c37]';
  commentSection.insertBefore(newDiv, commentSection.children[0]);
  newCommentContainer.querySelector('#comment-create-form').id = "recomment-create-form";
  newCommentContainer.querySelector('#recomment-create-form').setAttribute("data-comment-pk", comment_pk);
  newCommentContainer.querySelector('#create-button').textContent = "대댓글 작성";
  var textarea = newCommentContainer.querySelector('textarea[name="content"]');
  textarea.value = '';
  newCommentContainer.querySelector('#post-img img').src = profile_image_url ? profile_image_url : "/static/img/no_profile_img.png";
  newCommentContainer.querySelector('#post-nickname').textContent = nickname;
  newCommentContainer.querySelector('#post-nickname').href = "/planets/" + planetName + "/profile/" + nickname + "/";
  newCommentContainer.querySelector('#post-createdtime p').textContent = created_time;
  newCommentContainer.querySelector('#post-content').textContent = content;
  newCommentContainer.querySelector('#post-tags').remove();
  newCommentContainer.querySelector('#post-image').remove();
  newCommentContainer.querySelector('#delete-post-button').id = "delete-comment-button";
  newCommentContainer.querySelector('#delete-comment-button').textContent = "댓글 삭제";
  newCommentContainer.querySelector('#delete-post-form').id = "delete-comment-form";
  newCommentContainer.querySelector('#delete-comment-form').setAttribute("data-comment-pk", comment_pk);
  if (requestuser_nickname == user) {
    newCommentContainer.querySelector('#dropdown-delete').style.display = 'block';
  } else {
    newCommentContainer.querySelector('#dropdown-delete').remove();
  }
  newCommentContainer.querySelector('#comment_form').id = "recomment_form";
  document.getElementById('comment-list').append(newCommentContainer);

  // 대댓글 있을 경우
  if (recomments) {
    for (var recomment of recomments) {
      var newRecommentContainer = createRecommentContainer(recomment.profile_image_url, recomment.nickname, recomment.created_time, recomment.content, recomment.pk, comment_pk);
      newCommentContainer.append(newRecommentContainer);
    }
  }

  return newCommentContainer;
}

// 대댓글 생성 container
function createRecommentContainer(profile_image_url, nickname, created_time, content, recomment_pk, comment_pk) {
  var newRecommentContainer = document.getElementById('section').cloneNode(true);
  var newDropdownMenu = document.getElementById('dropdown-menu').cloneNode(true);
  var newDiv = document.createElement('div');
  newDiv.innerHTML = `<svg width="30px" height="30px" id="Capa_1" style="enable-background:new 0 0 74.5 60;" version="1.1" viewBox="0 0 74.5 60" width="74.5px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g><path d="M10,45h40.5v15l24-22l-24-22v15H14V0H0v35C0,40.523,4.477,45,10,45z" fill="#ffffff"/></g></svg>`;
  newRecommentContainer.insertBefore(newDiv, newRecommentContainer.children[0]);
  var newDiv2 = document.createElement('div');
  newDiv2.style.width = "130px";
  newRecommentContainer.insertBefore(newDiv2, newRecommentContainer.children[0]);
  newRecommentContainer.querySelector('#post-img img').src = profile_image_url ? profile_image_url : "/static/img/no_profile_img.png";
  newRecommentContainer.querySelector('#post-nickname').textContent = nickname;
  newRecommentContainer.querySelector('#post-nickname').href = "/planets/" + planetName + "/profile/" + nickname + "/";
  newRecommentContainer.querySelector('#post-createdtime p').textContent = created_time;
  newRecommentContainer.querySelector('#post-content').textContent = content;
  newRecommentContainer.querySelector('#delete-post-button').id = "delete-recomment-button";
  newRecommentContainer.querySelector('#delete-recomment-button').textContent = "대댓글 삭제";
  newRecommentContainer.querySelector('#delete-post-form').id = "delete-recomment-form";
  newRecommentContainer.querySelector('#delete-recomment-form').setAttribute("data-comment-pk", comment_pk);
  newRecommentContainer.querySelector('#delete-recomment-form').setAttribute("data-recomment-pk", recomment_pk);
  if (requestuser_nickname == nickname) {
    newRecommentContainer.querySelector('#dropdown-delete').style.display = 'block';
  } else {
    newRecommentContainer.querySelector('#dropdown-delete').remove();
  }
  var svgDiv = newRecommentContainer.querySelector('#comment_form').closest('p').closest('div')
  var newp = document.createElement('p')
  newp.classList.add('w-1/5');
  svgDiv.insertBefore(newp, svgDiv.firstChild);
  newRecommentContainer.querySelector('#comment_form').closest('p').remove();
  newRecommentContainer.append(newDropdownMenu);

  return newRecommentContainer;
}

// eventlistener
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('click', function(e) {
    var target = e.target;

    // 댓글, 대댓글 작성 svg 클릭
    if (target.tagName == 'svg' && target.id == 'comment_form') {
      var commentForm = document.querySelector('#comment-create-form');

      if (commentForm.style.display == 'none') {
        commentForm.style.display = 'block';
      } else {
        commentForm.style.display = 'none';
      }
    } else if (target.tagName == 'svg' && target.id == 'recomment_form') {
      var parentDiv = target.closest('#container');
      var recommentForm = parentDiv.querySelector('#recomment-create-form');

      if (recommentForm.style.display == 'none') {
        recommentForm.style.display = 'block';
      } else {
        recommentForm.style.display = 'none';
      }
    };
  });

  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    // 댓글 생성
    if (target.matches('#comment-create-form')) {
      e.preventDefault();

      var form = target;
      form.style.display = 'none';
      var planetName = form.dataset.planetName;
      var postPk = form.dataset.postPk;
      var url = "/planets/" + planetName + "/" + postPk + "/create/";

      axios({
        url: url,
        method: 'POST',
        data: new FormData(form),
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          var commentList = document.querySelector('#comment-list');
          var newCommentContainer = createcommentContainer(response.data.profile_image_url, response.data.nickname, response.data.created_time, response.data.content, response.data.comment_pk, response.data.user);
          commentList.append(newCommentContainer);
          form.reset();
        } else {
          console.error(response.data.message);
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

    // 댓글 삭제
    else if (target.matches('#delete-comment-form')) {
      e.preventDefault();

      var deleteButton = target.querySelector('#delete-comment-button');
      var commentContainer = deleteButton.closest('#container');
      var planetName = target.dataset.planetName;
      var postPk = target.dataset.postPk;
      var commentPk = target.dataset.commentPk;
      var url = "/planets/" + planetName + "/" + postPk + "/" + commentPk +"/delete/";

      axios({
        url: url,
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
      .then(function(response) {
        if (response.data.success == "Change") {
          var commentContent = commentContainer.querySelector('#post-content');
          commentContent.innerHTML = response.data.comment_content;
        } else if (response.data.success) {
          commentContainer.remove();
        } else {
          console.error('Comment deletion failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

    // 대댓글 생성
    else if (target.matches('#recomment-create-form')) {
      e.preventDefault();

      var form = target;
      form.style.display = 'none';
      var recommentContainer = form.closest('#container');
      var planetName = form.dataset.planetName;
      var postPk = form.dataset.postPk;
      var commentPk = form.dataset.commentPk;

      axios({
        url: "/planets/" + planetName + "/" + postPk + "/" + commentPk + "/create/",
        method: 'POST',
        data: new FormData(form),
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          recommentContainer.append(createRecommentContainer(response.data.profile_image_url, response.data.nickname, response.data.created_time, response.data.content, response.data.recomment_pk, commentPk));
          form.reset();
        } else {
          console.error(response.data.message);
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

    // 대댓글 삭제
    else if (target.matches('#delete-recomment-form')) {
      e.preventDefault();

      var deleteButton = target.querySelector('#delete-recomment-button');
      var recommentContainer = deleteButton.closest('#section');
      var planetName = target.dataset.planetName;
      var postPk = target.dataset.postPk;
      var commentPk = target.dataset.commentPk;
      var recommentPk = target.dataset.recommentPk;
      var url = "/planets/" + planetName + "/" + postPk + "/" + commentPk + "/" + recommentPk + "/delete/";

      axios({
        url: url,
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          recommentContainer.remove();
        } else {
          console.error('Recomment deletion failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }
  });
});

// post 비동기 emote
const postEmoteForms = document.querySelectorAll('.post-emote-form')
postEmoteForms.forEach((emoteForm) => {
  emoteForm.addEventListener('submit', (e) => {
    e.preventDefault()
    
    const emoteClass = e.target.dataset.emoteClass
    const planetName = e.target.dataset.planetName
    const postPk = e.target.dataset.postPk
    const emotionCount = document.querySelector(`.post-emote-form > p > .emotion-${emoteClass}-count`)

    axios({
      method:'post',
      url:`/planets/${planetName}/posts/${postPk}/emotes/${emoteClass}`,
      headers:{'X-CSRFToken': csrftoken,}
    })
    .then((response) => {
      emotionCount.innerHTML = response.data.emotion_count
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})

// comment 비동기 emote
// const commentEmoteForms = document.querySelectorAll('.comment-emote-form')
// postEmoteForms.forEach((emoteForm) => {
//   emoteForm.addEventListener('submit', (e) => {
//     e.preventDefault()
    
//     const emoteClass = e.target.dataset.emoteClass
//     const planetName = e.target.dataset.planetName
//     const commentPk = e.target.dataset.commentPk
//     const postPk = e.target.dataset.postPk
//     const emotionCount = document.querySelector(`.comment-emote-form > p > .emotion-${emoteClass}-count`)

//     axios({
//       method:'post',
//       url:`/planets/${planetName}/posts/${postPk}/commments/${commentPk}/emotes/${emoteClass}`,
//       headers:{'X-CSRFToken': csrftoken,}
//     })
//     .then((response) => {
//       emotionCount.innerHTML = response.data.emotion_count
//     })
//     .catch((error) => {
//       console.log(error.response)
//     })
//   })
// })