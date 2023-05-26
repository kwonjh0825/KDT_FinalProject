// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// 게시글 생성
document.addEventListener('DOMContentLoaded', function() {
  var postForm = document.getElementById('post-form');

  postForm.addEventListener('submit', function(e) {
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
        var postPk = response.data.post_pk;
        var newPostContainer = document.createElement('div');
        newPostContainer.classList.add('post-container');
        newPostContainer.setAttribute('data-post-pk', postPk);

        var content = document.createElement('div');
        content.textContent = response.data.content;

        var createdTime = document.createElement('div');
        createdTime.textContent = response.data.created_time;

        var nickname = document.createElement('div');
        nickname.textContent = response.data.nickname;

        var image = null;
        if (response.data.image_url) {
          image = document.createElement('img');
          image.setAttribute('src', response.data.image_url);
          image.setAttribute('alt', 'Image');
        }

        if (image) {
          newPostContainer.append(content, createdTime, nickname, image);
        } else {
          newPostContainer.append(content, createdTime, nickname);
        }



        var deletePostForm = document.createElement('form');
        deletePostForm.classList.add('delete-post-form');
        deletePostForm.dataset.planetName = planetName;
        deletePostForm.dataset.postPk = postPk;

        var csrfTokenInput = document.createElement('input');
        csrfTokenInput.type = 'hidden';
        csrfTokenInput.name = 'csrfmiddlewaretoken';
        csrfTokenInput.value = csrftoken;

        var deletePostButton = document.createElement('input');
        deletePostButton.type = 'submit';
        deletePostButton.classList.add('delete-post-button');
        deletePostButton.value = '게시글 삭제';

        deletePostForm.append(csrfTokenInput, deletePostButton);
        newPostContainer.appendChild(deletePostForm);

        var commentList = document.createElement('div');
        commentList.id = 'comment-list';

        var commentForm = document.createElement('form');
        commentForm.id = 'comment-form';
        commentForm.dataset.planetName = planetName;
        commentForm.dataset.postPk = postPk;

        var csrfTokenInput2 = document.createElement('input');
        csrfTokenInput2.type = 'hidden';
        csrfTokenInput2.name = 'csrfmiddlewaretoken';
        csrfTokenInput2.value = csrftoken;

        var commentTextarea = document.createElement('textarea');
        commentTextarea.name = 'content';
        commentTextarea.cols = '40';
        commentTextarea.rows = '10';
        commentTextarea.required = true;
        commentTextarea.id = 'id_content';

        var commentLabel = document.createElement('label');
        commentLabel.textContent = '내용:';
        commentLabel.htmlFor = 'id_content';

        var commentParagraph = document.createElement('p');
        commentParagraph.appendChild(commentLabel);
        commentParagraph.appendChild(commentTextarea);

        var submitButton = document.createElement('input');
        submitButton.type = 'submit';
        submitButton.value = '댓글 작성';

        commentForm.append(csrfTokenInput2, commentParagraph, submitButton);
        commentList.appendChild(commentForm);

        newPostContainer.appendChild(commentList);

        var postList = document.getElementById('post-list');
        postList.insertBefore(newPostContainer, postList.firstChild);

        form.reset();
      } else {
        console.error(response.data.message);
      }
    })
    .catch(function(error) {
      console.error('AJAX request failed:', error);
    });
  });
});

// 게시글 삭제
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    if (target.matches('.delete-post-form')) {
      e.preventDefault();

      var deleteForm = target;
      var deleteButton = deleteForm.querySelector('.delete-post-button');
      var postContainer = deleteButton.closest('.post-container');
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
  });
});


// 댓글 생성
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    if (target.matches('#comment-form')) {
      e.preventDefault();

      var form = target;
      var commentContainer = form.closest('.post-container');
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

          var newCommentContainer = document.createElement('div');
          newCommentContainer.classList.add('comment-container');

          var content = document.createElement('div');
          content.textContent = response.data.content;

          var createdTime = document.createElement('div');
          createdTime.textContent = response.data.created_time;

          var nickname = document.createElement('div');
          nickname.textContent = response.data.nickname;

          newCommentContainer.append(content, createdTime, nickname);

          var deleteCommentForm = document.createElement('form');
          deleteCommentForm.classList.add('delete-comment-form');
          deleteCommentForm.dataset.planetName = planetName;
          deleteCommentForm.dataset.postPk = postPk;
          deleteCommentForm.dataset.commentPk = response.data.comment_pk;

          var csrfTokenInput = document.createElement('input');
          csrfTokenInput.type = 'hidden';
          csrfTokenInput.name = 'csrfmiddlewaretoken';
          csrfTokenInput.value = csrftoken;

          var deleteCommentButton = document.createElement('input');
          deleteCommentButton.type = 'submit';
          deleteCommentButton.classList.add('delete-comment-button');
          deleteCommentButton.value = '댓글 삭제';

          deleteCommentForm.append(csrfTokenInput, deleteCommentButton);
          newCommentContainer.appendChild(deleteCommentForm);

          var recommentList = document.createElement('div');
          recommentList.id = 'recomment-list';

          var recommentForm = document.createElement('form');
          recommentForm.id = 'recomment-form';
          recommentForm.dataset.planetName = planetName;
          recommentForm.dataset.postPk = postPk;
          recommentForm.dataset.commentPk = response.data.comment_pk;

          var csrfTokenInput2 = document.createElement('input');
          csrfTokenInput2.type = 'hidden';
          csrfTokenInput2.name = 'csrfmiddlewaretoken';
          csrfTokenInput2.value = csrftoken;

          var recommentTextarea = document.createElement('textarea');
          recommentTextarea.name = 'content';
          recommentTextarea.cols = '40';
          recommentTextarea.rows = '10';
          recommentTextarea.required = true;
          recommentTextarea.id = 'id_content';

          var recommentLabel = document.createElement('label');
          recommentLabel.textContent = '내용:';
          recommentLabel.htmlFor = 'id_content';

          var recommentParagraph = document.createElement('p');
          recommentParagraph.appendChild(recommentLabel);
          recommentParagraph.appendChild(recommentTextarea);

          var submitButton = document.createElement('input');
          submitButton.type = 'submit';
          submitButton.value = '대댓글 작성';

          recommentForm.append(csrfTokenInput2, recommentParagraph, submitButton);
          recommentList.appendChild(recommentForm);

          newCommentContainer.appendChild(recommentList);

          commentList.insertBefore(newCommentContainer, commentList.firstChild);

          form.reset();
        } else {
          console.error(response.data.message);
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }
  });
});

// 댓글 삭제
document.addEventListener('DOMContentLoaded', function() {
  var deleteForms = document.querySelector('body');

  deleteForms.addEventListener('submit', function(e) {
    var target = e.target;

    if (target.matches('.delete-comment-form')) {
      e.preventDefault();

      var deleteButton = target.querySelector('.delete-comment-button');
      var commentContainer = deleteButton.closest('.comment-container');
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
        if (response.data.success) {
          commentContainer.remove();
        } else {
          console.error('Comment deletion failed.');
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }
  });
});

// 대댓글 생성
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;

    if (target.matches('#recomment-form')) {
      e.preventDefault();

      var form = target;
      var recommentContainer = form.closest('.comment-container');
      var planetName = form.dataset.planetName;
      var postPk = form.dataset.postPk;
      var commentPk = form.dataset.commentPk;
      var url = "/planets/" + planetName + "/" + postPk + "/" + commentPk +"/create/";

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
          var recommentList = recommentContainer.querySelector('#recomment-list');

          var newRecommentContainer = document.createElement('div');
          newRecommentContainer.classList.add('recomment-container');

          var content = document.createElement('div');
          content.textContent = response.data.content;

          var createdTime = document.createElement('div');
          createdTime.textContent = response.data.created_time;

          var nickname = document.createElement('div');
          nickname.textContent = response.data.nickname;

          newRecommentContainer.append(content, createdTime, nickname);

          var deleteRecommentForm = document.createElement('form');
          deleteRecommentForm.classList.add('delete-recomment-form');
          deleteRecommentForm.dataset.planetName = planetName;
          deleteRecommentForm.dataset.postPk = postPk;
          deleteRecommentForm.dataset.commentPk = commentPk;
          deleteRecommentForm.dataset.recommentPk = response.data.recomment_pk;

          var csrfTokenInput = document.createElement('input');
          csrfTokenInput.type = 'hidden';
          csrfTokenInput.name = 'csrfmiddlewaretoken';
          csrfTokenInput.value = csrftoken;

          var deleteRecommentButton = document.createElement('input');
          deleteRecommentButton.type = 'submit';
          deleteRecommentButton.classList.add('delete-recomment-button');
          deleteRecommentButton.value = '대댓글 삭제';

          deleteRecommentForm.append(csrfTokenInput, deleteRecommentButton);
          newRecommentContainer.appendChild(deleteRecommentForm);

          recommentList.insertBefore(newRecommentContainer, recommentList.firstChild);

          form.reset();
        } else {
          console.error(response.data.message);
        }
      })
      .catch(function(error) {
        console.error('AJAX request failed:', error);
      });
    }
  });
});


// 대댓글 삭제
document.addEventListener('DOMContentLoaded', function() {
  var deleteForms = document.querySelector('body');

  deleteForms.addEventListener('submit', function(e) {
    var target = e.target;

    if (target.matches('.delete-recomment-form')) {
      e.preventDefault();

      var deleteButton = target.querySelector('.delete-recomment-button');
      var recommentContainer = deleteButton.closest('.recomment-container');
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
