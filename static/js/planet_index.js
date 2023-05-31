// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// eventlistener
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    // 게시글 생성
    if (target.matches('#post-form')) {
      e.preventDefault();

      var form = e.target;
      var planetName = form.dataset.planetName;
      var url = "/planets/" + planetName + "/create/";
      var formData = new FormData(form);
      formData.append('csrfmiddlewaretoken', csrftoken);

      axios({
        method: 'post',
        url: url,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(function(response) {
        if (response.data.success) {
          var post_pk = response.data.post_pk;
          var postList = document.getElementById('post-list');
          var newPostContainer = createpostContainer(response.data.profile_image_url, response.data.nickname, response.data.created_time, response.data.content, response.data.user, post_pk, planetName);
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

    // 게시글 삭제
    else if (target.matches('#delete-post-form')) {
      e.preventDefault();

      var deleteForm = target;
      var deleteButton = deleteForm.querySelector('#delete-post-button');
      var postContainer = deleteButton.closest('#post-container');
      var planetName = deleteForm.dataset.planetName;
      var postPk = deleteForm.dataset.postPk;
      var url = "/planets/" + planetName + "/" + postPk + "/delete/";

      axios({
        url: url,
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        }
      })
      .then(function(response) {
        if (response.data.success) {
          postContainer.remove();
        } else {
          console.error('Post deletion failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

  //   // 댓글 생성
  //   else if (target.matches('#comment-form')) {
  //     e.preventDefault();

  //     var form = target;
  //     var commentContainer = form.closest('#post-container');
  //     var planetName = form.dataset.planetName;
  //     var postPk = form.dataset.postPk;
  //     var url = "/planets/" + planetName + "/" + postPk + "/create/";

  //     axios({
  //       url: url,
  //       method: 'POST',
  //       data: new FormData(form),
  //       headers: {
  //         'X-CSRFToken': csrftoken,
  //       }
  //     })
  //     .then(function(response) {
  //       if (response.data.success) {
  //         var commentList = commentContainer.querySelector('#comment-list');

  //         var newCommentContainer = document.createElement('div');
  //         newCommentContainer.classList.add('comment-container');

  //         var content = document.createElement('div');
  //         content.textContent = response.data.content;
  //         content.id = 'comment-content';

  //         var createdTime = document.createElement('div');
  //         createdTime.textContent = response.data.created_time;

  //         var nickname = document.createElement('div');
  //         nickname.textContent = response.data.nickname;

  //         newCommentContainer.append(content, createdTime, nickname);

  //         var deleteCommentForm = document.createElement('form');
  //         deleteCommentForm.id = 'delete-comment-form';
  //         deleteCommentForm.dataset.planetName = planetName;
  //         deleteCommentForm.dataset.postPk = postPk;
  //         deleteCommentForm.dataset.commentPk = response.data.comment_pk;

  //         var csrfTokenInput = document.createElement('input');
  //         csrfTokenInput.type = 'hidden';
  //         csrfTokenInput.name = 'csrfmiddlewaretoken';
  //         csrfTokenInput.value = csrftoken;

  //         var deleteCommentButton = document.createElement('input');
  //         deleteCommentButton.id = 'delete-comment-button';
  //         deleteCommentButton.type = 'submit';
  //         deleteCommentButton.value = '댓글 삭제';

  //         deleteCommentForm.append(csrfTokenInput, deleteCommentButton);
  //         newCommentContainer.appendChild(deleteCommentForm);

  //         var recommentList = document.createElement('div');
  //         recommentList.id = 'recomment-list';

  //         var recommentcreate = document.createElement('div');
  //         recommentcreate.id = 'recomment-create';

  //         var button = document.createElement('button');
  //         button.id = 'show-recomment-form-button';
  //         button.textContent = '대댓글 작성';

  //         var recommentForm = document.createElement('form');
  //         recommentForm.id = 'recomment-form';
  //         recommentForm.style.display = 'none';
  //         recommentForm.dataset.planetName = planetName;
  //         recommentForm.dataset.postPk = postPk;
  //         recommentForm.dataset.commentPk = response.data.comment_pk;

  //         var csrfTokenInput2 = document.createElement('input');
  //         csrfTokenInput2.type = 'hidden';
  //         csrfTokenInput2.name = 'csrfmiddlewaretoken';
  //         csrfTokenInput2.value = csrftoken;

  //         var recommentTextarea = document.createElement('textarea');
  //         recommentTextarea.name = 'content';
  //         recommentTextarea.cols = '40';
  //         recommentTextarea.rows = '10';
  //         recommentTextarea.required = true;
  //         recommentTextarea.id = 'id_content';

  //         var recommentLabel = document.createElement('label');
  //         recommentLabel.textContent = '내용:';
  //         recommentLabel.htmlFor = 'id_content';

  //         var recommentParagraph = document.createElement('p');
  //         recommentParagraph.appendChild(recommentLabel);
  //         recommentParagraph.appendChild(recommentTextarea);

  //         var submitButton = document.createElement('input');
  //         submitButton.type = 'submit';
  //         submitButton.value = '대댓글 작성';

  //         recommentForm.append(csrfTokenInput2, recommentParagraph, submitButton);
  //         recommentcreate.appendChild(button);
  //         recommentcreate.appendChild(recommentForm);
  //         recommentList.appendChild(recommentcreate);
  //         newCommentContainer.appendChild(recommentList);

  //         commentList.insertBefore(newCommentContainer, commentList.firstChild);

  //         target.previousElementSibling.textContent = '댓글 작성';

  //         target.style.display = "none";
  //         form.reset();
  //       } else {
  //         console.error(response.data.message);
  //       }
  //     })
  //     .catch(function(error) {
  //       console.error('AJAX request failed:', error);
  //     });
  //   }

  //   // 댓글 삭제
  //   else if (target.matches('#delete-comment-form')) {
  //     e.preventDefault();

  //     var deleteButton = target.querySelector('#delete-comment-button');
  //     var commentContainer = deleteButton.closest('.comment-container');
  //     var planetName = target.dataset.planetName;
  //     var postPk = target.dataset.postPk;
  //     var commentPk = target.dataset.commentPk;
  //     var url = "/planets/" + planetName + "/" + postPk + "/" + commentPk +"/delete/";

  //     axios({
  //       url: url,
  //       method: 'POST',
  //       headers: {
  //         'X-CSRFToken': csrftoken,
  //       }
  //     })
  //     .then(function(response) {
  //       if (response.data.success == "Change") {
  //         var commentContent = commentContainer.querySelector('#comment-content');
  //         commentContent.innerHTML = response.data.comment_content;
  //       } else if (response.data.success) {
  //         commentContainer.remove();
  //       } else {
  //         console.error('Comment deletion failed.');
  //       }
  //     })
  //     .catch(function(error) {
  //       console.error('AJAX request failed:', error);
  //     });
  //   }

  //   // 대댓글 생성
  //   else if (target.matches('#recomment-form')) {
  //     e.preventDefault();

  //     var form = target;
  //     var recommentContainer = form.closest('.comment-container');
  //     var planetName = form.dataset.planetName;
  //     var postPk = form.dataset.postPk;
  //     var commentPk = form.dataset.commentPk;
  //     var url = "/planets/" + planetName + "/" + postPk + "/" + commentPk +"/create/";

  //     axios({
  //       url: url,
  //       method: 'POST',
  //       data: new FormData(form),
  //       headers: {
  //         'X-CSRFToken': csrftoken,
  //       }
  //     })
  //     .then(function(response) {
  //       if (response.data.success) {
  //         var recommentList = recommentContainer.querySelector('#recomment-list');

  //         var newRecommentContainer = document.createElement('div');
  //         newRecommentContainer.classList.add('recomment-container');

  //         var content = document.createElement('div');
  //         content.textContent = response.data.content;

  //         var createdTime = document.createElement('div');
  //         createdTime.textContent = response.data.created_time;

  //         var nickname = document.createElement('div');
  //         nickname.textContent = response.data.nickname;

  //         newRecommentContainer.append(content, createdTime, nickname);

  //         var deleteRecommentForm = document.createElement('form');
  //         deleteRecommentForm.id = 'delete-recomment-form';
  //         deleteRecommentForm.dataset.planetName = planetName;
  //         deleteRecommentForm.dataset.postPk = postPk;
  //         deleteRecommentForm.dataset.commentPk = commentPk;
  //         deleteRecommentForm.dataset.recommentPk = response.data.recomment_pk;

  //         var csrfTokenInput = document.createElement('input');
  //         csrfTokenInput.type = 'hidden';
  //         csrfTokenInput.name = 'csrfmiddlewaretoken';
  //         csrfTokenInput.value = csrftoken;

  //         var deleteRecommentButton = document.createElement('input');
  //         deleteRecommentButton.id = 'delete-recomment-button';
  //         deleteRecommentButton.type = 'submit';
  //         deleteRecommentButton.value = '대댓글 삭제';

  //         deleteRecommentForm.append(csrfTokenInput, deleteRecommentButton);
  //         newRecommentContainer.appendChild(deleteRecommentForm);

  //         recommentList.insertBefore(newRecommentContainer, recommentList.firstChild);

  //         target.previousElementSibling.textContent = '대댓글 작성';

  //         target.style.display = 'none';
  //         form.reset();
  //       } else {
  //         console.error(response.data.message);
  //       }
  //     })
  //     .catch(function(error) {
  //       console.error('AJAX request failed:', error);
  //     });
  //   }

  //   // 대댓글 삭제
  //   else if (target.matches('#delete-recomment-form')) {
  //     e.preventDefault();

  //     var deleteButton = target.querySelector('#delete-recomment-button');
  //     var recommentContainer = deleteButton.closest('.recomment-container');
  //     var planetName = target.dataset.planetName;
  //     var postPk = target.dataset.postPk;
  //     var commentPk = target.dataset.commentPk;
  //     var recommentPk = target.dataset.recommentPk;
  //     var url = "/planets/" + planetName + "/" + postPk + "/" + commentPk + "/" + recommentPk + "/delete/";

  //     axios({
  //       url: url,
  //       method: 'POST',
  //       headers: {
  //         'X-CSRFToken': csrftoken,
  //       }
  //     })
  //     .then(function(response) {
  //       if (response.data.success) {
  //         recommentContainer.remove();
  //       } else {
  //         console.error('Recomment deletion failed.');
  //       }
  //     })
  //     .catch(function(error) {
  //       console.error('AJAX request failed:', error);
  //     });
  //   }
  // });

  // document.querySelector('body').addEventListener('click', function(e) {
  //   var target = e.target;

  //   // 게시 버튼
  //   if (target.id.startsWith('show-post-form-button')) {
  //     e.preventDefault();

  //     var postForm = document.querySelector('#post-form');

  //     if (postForm.style.display === 'none') {
  //       postForm.style.display = 'block';
  //     } else {
  //       postForm.style.display = 'none';
  //     }
  //   }

  //   // 댓글 버튼
  //   if (target.id.startsWith('show-comment-form-button')) {
  //     e.preventDefault();

  //     var commentForm = target.nextElementSibling;
  //     var button = target;

  //     if (commentForm.style.display === 'none') {
  //       commentForm.style.display = 'block';
  //       button.innerHTML = '댓글 작성 취소';
  //     } else {
  //       commentForm.style.display = 'none';
  //       button.innerHTML = '댓글 작성';
  //     }
  //   }

  //   // 대댓글 버튼
  //   else if (target.id.startsWith('show-recomment-form-button')) {
  //     e.preventDefault();

  //     var recommentForm = target.nextElementSibling;
  //     var button = target;

  //     if (recommentForm.style.display === 'none') {
  //       recommentForm.style.display = 'block';
  //       button.innerHTML = '대댓글 작성 취소';
  //     } else {
  //       recommentForm.style.display = 'none';
  //       button.innerHTML = '대댓글 작성';
  //     }
  //   }
  });
});

// 스크롤 첫번째 실행
$(document).ready(function() {
  var initialPage = 1;
  loadPosts(initialPage);
});

// 스크롤시 post 비동기
$(window).scroll(function() {
  if ($(window).scrollTop() == $(document).height() - $(window).height()) {
      var nextPage = parseInt($('#post-list').val()) + 1;
      loadPosts(nextPage);
  }
});

// posts rendering 비동기 처리
function loadPosts(page) {
  var planetName = document.getElementById('post-form').getAttribute('data-planet-name');

  $.ajax({
    url: '/planets/' + planetName + '/posts/',
    type: 'GET',
    data: {
        'page': page
    },
    dataType: 'json',
    success: function(data) {
      for (var i = 0; i < data.length; i++) {
        var post = data[i];
        if (post === null) {
          $(window).off('scroll');
          return;
        }
        $('#post-list').append(createpostContainer(post.profile_image_url, post.nickname, post.created_time, post.content, post.user, post.pk, planetName));
      }
      $('#post-list').val(page);
    }
  });
}

// post container 생성
function createpostContainer(profile_image_url, nickname, created_time, content, user, post_pk, planetName) {
  var newPostContainer = document.getElementById('post-container').cloneNode(true);
  newPostContainer.style.display = "";
  newPostContainer.querySelector('#post-img img').src = profile_image_url ? profile_image_url : "/static/img/no_profile_img.png";
  newPostContainer.querySelector('#post-nickname').textContent = nickname;
  newPostContainer.querySelector('#post-createdtime p').textContent = created_time;
  newPostContainer.querySelector('#post-content').textContent = content;
  return newPostContainer;
}
