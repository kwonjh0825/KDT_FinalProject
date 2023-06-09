// post container 생성
function createpostContainer(
  profile_image_url,
  nickname,
  created_time,
  content,
  tags,
  post_pk,
  image_url,
  user,
  votetopics
) {
  var newPostContainer = document.getElementById('container').cloneNode(true);
  newPostContainer.querySelector('#section').style.display = 'flex';
  newPostContainer.querySelector('#post-img img').src = profile_image_url
    ? profile_image_url
    : '/static/img/no_profile_img.png';
  newPostContainer.querySelector('#post-nickname').textContent = nickname;

  // if (votetopic) {
  //   console.log('--------------------------------------ssssssssssss');
  //   console.log(votetopic);
  //   var votetopicContainer = newPostContainer.querySelector('#post-votetopic');
  //   if (votetopicContainer) {
  //     votetopic.forEach(function (topic) {
  //       var newTopic = document.createElement('span');
  //       newTopic.classList.add('text-[#bcbdbf]');
  //       newTopic.id = 'votetopic';
  //       newTopic.textContent = '#' + topic.title;
  //       votetopicContainer.appendChild(newTopic);
  //     });
  //   } else {
  //     console.log('#post-votetopic element not found');
  //     return; // 동작을 건너뛰고 함수 종료
  //   }
  // }
  if (votetopics && votetopics.length > 0) {
    votetopics.forEach(function (votetopic) {
      if (votetopic.title.trim() !== '') {
        var voteTopicContainer =
          newPostContainer.querySelector('#post-votetopics');
        var newVotetopic = document.createElement('div'); // 변경된 부분: <span> 대신 <div> 사용
        newVotetopic.classList.add(
          'text-[#bcbdbf]',
          'my-1',
          'rounded-md',
          'p-2',
          'border'
        );
        newVotetopic.id = 'votetopic';
        newVotetopic.textContent = votetopic.title;
        voteTopicContainer.appendChild(newVotetopic);
      } else {
        var voteTopicContainer =
          newPostContainer.querySelector('#post-votetopics');
        voteTopicContainer.style.display = 'none';
      }
    });
  }

  newPostContainer.querySelector('#post-nickname').href = "/planets/" + planetName + "/profile/" + nickname + "/";
  newPostContainer.querySelector('#post-createdtime p').textContent = created_time;
  newPostContainer.querySelector('#post-content').textContent = content;
  newPostContainer.querySelector('#delete-post-form').setAttribute("data-post-pk", post_pk);
  newPostContainer.querySelector('#update-post-form').setAttribute("data-post-pk", post_pk);
  newPostContainer.querySelector('#post-report').href = "/planets/" + planetName + "/report/post/" + post_pk + "/";
  newPostContainer.querySelector('#post-detailpage').href = "/planets/" + planetName + "/" + post_pk + "/";

  if (tags) {
    tags.forEach(function (tag) {
      var tagContainer = newPostContainer.querySelector('#post-tags');
      var newTag = document.createElement('span');

      newTag.classList.add("text-[#bcbdbf]");
      newTag.id = "tag";
      var newA = document.createElement('a');
      newA.href = "/planets/" + planetName + "/tags/" + tag + "/";
      newA.textContent = "#" + tag;
      newTag.appendChild(newA);
      tagContainer.appendChild(newTag);
    });
  }
  if (image_url) {
    var imageContainer = newPostContainer.querySelector('#post-image');
    var newImage = document.createElement('img');
    newImage.src = image_url;
    newImage.alt = 'image';
    newImage.classList.add('rounded-lg');
    imageContainer.append(newImage);
  }
  if (nickname == requestuser) {
    newPostContainer.querySelector('#dropdown-delete').style.display = 'block';
    newPostContainer.querySelector('#dropdown-update').style.display = 'block';
  }
  return newPostContainer;
}

// eventlistener
document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('body').addEventListener('click', function (e) {
    var target = e.target;

    // 더보기 클릭
    if (
      target.tagName == 'circle' ||
      (target.tagName == 'svg' && target.id == 'more')
    ) {
      var parentDiv = target.closest('#section');
      var dropdownMenu = parentDiv.querySelector('#dropdown-menu');
      var buttonRect = target.getBoundingClientRect();

      dropdownMenu.style.top = buttonRect.top + window.scrollY + 'px';
      dropdownMenu.style.left = buttonRect.right + window.scrollX + 'px';

      if (dropdownMenu.style.display == 'none') {
        dropdownMenu.style.display = 'block';
      } else {
        dropdownMenu.style.display = 'none';
      }
    } else {
      var dropdownMenus = document.querySelectorAll('#dropdown-menu');

      dropdownMenus.forEach(function (menu) {
        if (menu.style.display == 'block') {
          menu.style.display = 'none';
        }
      });
    }
  });

  document.querySelector('body').addEventListener('submit', function (e) {
    var target = e.target;

    // 게시글 삭제
    if (target.matches('#delete-post-form')) {
      e.preventDefault();

      var deleteForm = target;
      var deleteButton = deleteForm.querySelector('#delete-post-button');
      var postContainer = deleteButton.closest('#container');
      var planetName = deleteForm.dataset.planetName;
      var postPk = deleteForm.dataset.postPk;

      var url = "/planets/" + planetName + "/post/" + postPk + "/delete/";
      

      axios({
        url: url,
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        },
      })
        .then(function (response) {
          if (response.data.success) {
            postContainer.remove();
          } else {
            console.error('Post deletion failed.');
          }
        })
        .catch(function (error) {
          console.error('AJAX request failed:', error);
        });
    }

    // 게시글 수정 form
    else if (target.matches('#update-post-form')) {
      e.preventDefault();

      var updateForm = target;
      var updateButton = updateForm.querySelector('#update-post-button');
      var postContainer = updateButton.closest('#container');
      var planetName = updateForm.dataset.planetName;
      var postPk = updateForm.dataset.postPk;
      var formData = new FormData(updateForm);

      axios({
        url: '/planets/' + planetName + '/' + postPk + '/update/',
        method: 'POST',
        data: formData,
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'multipart/form-data',
        }
      })
      .then(function(response) {
        if (response.data.success) {
          var formHtml = response.data.form_html;
          var formContainer = document.createElement('div');
          formContainer.innerHTML = formHtml;
          formContainer.querySelector('label[for="id_content"]').innerHTML = '<p class="text-base text-white">내용</p>';
          formContainer.querySelector('label[for="id_image"]').innerHTML = '<p class="text-base text-white">이미지</p>';
          formContainer.querySelector('label[for="id_tags"]').innerHTML = '<p class="text-base text-white">태그</p>';
          var formElement = document.createElement('form');
          formElement.id = "edit-post-form";
          formElement.setAttribute("data-planet-name", planetName);
          formElement.setAttribute("data-post-pk", postPk);
          formElement.appendChild(formContainer);
          var submitButton = document.createElement('button');
          submitButton.id = "edit-post-button";
          submitButton.classList.add('chatting-create-btn', 'bg-[#bcbdbf]', 'mx-auto');
          submitButton.textContent = '게시글 수정';
          submitButton.type = 'submit';
          formContainer.append(submitButton);
          postContainer.querySelector('#section').style.display = 'none';
          postContainer.append(formElement);
        } else {
          console.error('Post deletion failed.');
        }

      })
        // .then(function (response) {
        //   if (response.data.success) {
        //     var formHtml = response.data.form_html;
        //     var formContainer = document.createElement('div');
        //     formContainer.innerHTML = formHtml;
        //     var formElement = document.createElement('form');
        //     formElement.id = 'edit-post-form';
        //     formElement.setAttribute('data-planet-name', planetName);
        //     formElement.setAttribute('data-post-pk', postPk);
        //     formElement.appendChild(formContainer);
        //     var submitButton = document.createElement('button');
        //     submitButton.id = 'edit-post-button';
        //     submitButton.textContent = 'Update';
        //     submitButton.type = 'submit';
        //     formContainer.append(submitButton);
        //     postContainer.querySelector('#section').style.display = 'none';
        //     postContainer.append(formElement);
        //   } else {
        //     console.error('Post deletion failed.');
        //   }
        // })
        // .catch(function (error) {
        //   console.error('AJAX request failed:', error);
        // });
    }

    // 게시글 수정 처리
    else if (target.matches('#edit-post-form')) {
      e.preventDefault();

      var editForm = target;
      var editButton = editForm.querySelector('#edit-post-button');
      var postContainer = editButton.closest('#container');
      var planetName = editForm.dataset.planetName;
      var postPk = editForm.dataset.postPk;
      var formData = new FormData(editForm);

      axios({
        url: '/planets/' + planetName + '/' + postPk + '/update/',
        method: 'POST',
        data: formData,
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'multipart/form-data',
        },
      })
        .then(function (response) {
          if (response.data.success) {
            postContainer.querySelector('#section').style.display = 'block';
            postContainer.querySelector('#post-content').textContent =
              response.data.content;
            postContainer.querySelector('#post-img img').src = response.data
              .profile_image_url
              ? response.data.profile_image_url
              : '/static/img/no_profile_img.png';
            if (response.data.tags) {
              var tagContainer = postContainer.querySelector('#post-tags');
              tagContainer.innerHTML = '';
              response.data.tags.forEach(function (tag) {
                var newTag = document.createElement('span');
                newTag.classList.add('text-[#bcbdbf]');
                newTag.id = 'tag';
                newTag.textContent = '#' + tag;
                tagContainer.appendChild(newTag);
              });
            }
            if (response.data.image_url) {
              var imageContainer = postContainer.querySelector('#post-image');
              imageContainer.innerHTML = '';
              var newImage = document.createElement('img');
              newImage.src = response.data.image_url;
              newImage.alt = 'image';
              newImage.classList.add('rounded-lg');
              imageContainer.append(newImage);
            }
            if (response.data.user == requestuser) {
              postContainer.querySelector('#dropdown-delete').style.display =
                'block';
            }
            postContainer.querySelector('#edit-post-form').remove();
            editForm.reset();
          } else {
            var divIdContent = editForm.querySelector('#div_id_content');
            var newP = document.createElement('p');
            newP.id = 'error_1_id_content';
            newP.className = 'text-red-500 text-xs italic';

            var strongElement = document.createElement('strong');
            strongElement.textContent = JSON.parse(
              response.data.errors
            ).content[0].message;
            newP.appendChild(strongElement);
            divIdContent.appendChild(newP);
          }
        })
        .catch(function (error) {
          console.error('AJAX request failed:', error);
        });
    }
  });
});
