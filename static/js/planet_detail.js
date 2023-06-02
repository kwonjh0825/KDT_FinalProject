// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// comment container 생성
function createcommentContainer(profile_image_url, nickname, created_time, content, comment_pk, user) {
  var newCommentContainer = document.getElementById('comment-container').cloneNode(true);
  newCommentContainer.style.display = "";
  newCommentContainer.querySelector('#comment-img img').src = profile_image_url ? profile_image_url : "/static/img/no_profile_img.png";
  newCommentContainer.querySelector('#comment-nickname').textContent = nickname;
  newCommentContainer.querySelector('#comment-createdtime p').textContent = created_time;
  newCommentContainer.querySelector('#comment-content').textContent = content;
  newCommentContainer.querySelector('#delete-comment-form').setAttribute("data-post-pk", comment_pk);
  newCommentContainer.querySelector('#comment-detail').href = "/planets/" + planetName + "/" + comment_pk + "/";
  if (user == requestuser) {
    newCommentContainer.querySelector('#dropdown-delete').style.display = "block";
  }
  return newCommentContainer;
}

// eventlistener
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    // 댓글 생성
    if (target.matches('#comment-form')) {
      e.preventDefault();

      var form = target;
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
          var commentList = commentContainer.querySelector('#comment-list');

          form.reset();
        } else {
          console.error(response.data.message);
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }

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

