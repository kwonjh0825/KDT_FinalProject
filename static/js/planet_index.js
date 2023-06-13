// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// eventlistener
document.addEventListener('DOMContentLoaded', function () {
  // submit event
  document.querySelector('body').addEventListener('submit', function (e) {
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
        url: '/planets/' + planetName + '/create/',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then(function (response) {
          if (response.data.success) {
            var post_pk = response.data.post_pk;
            var postList = document.getElementById('post-list');
            var newPostContainer = createpostContainer(
              response.data.profile_image_url,
              response.data.nickname,
              response.data.created_time,
              response.data.content,
              response.data.tags,
              post_pk,
              response.data.image_url,
              response.data.user,
              response.data.votetopics,
              // emote heart, thumbsup, thumbsdown은 새 게시물에서 0으로 시작
              0,
              0,
              0,
              response.data.vote_count,
              response.data.voted
            );

            postList.insertBefore(newPostContainer, postList.children[1]);
            form.reset();

            // 모달 닫기
            var modal = document.getElementById('defaultModal');
            modal.classList.add('hidden');
            var modalBackdrop = document.querySelector('[modal-backdrop]');
            if (modalBackdrop) {
              modalBackdrop.classList.add('hidden');
            }
          } else {
            var divIdContent = form.querySelector('#div_id_content');
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
