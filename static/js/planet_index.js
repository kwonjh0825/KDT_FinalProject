// csrf
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// 글쓰기 버튼
// var postButton = document.getElementById('post-btn');
// postButton.addEventListener('click', function () {
//   var modalBackdrop = document.querySelector('div[modal-backdrop]');
//   console.log(modalBackdrop);
//   if (!modalBackdrop) {
//     modalBackdrop = document.createElement('div');
//     modalBackdrop.setAttribute('modal-backdrop', '');
//     modalBackdrop.classList.add(
//       'bg-gray-900',
//       'bg-opacity-50',
//       'dark:bg-opacity-80',
//       'fixed',
//       'inset-0',
//       'z-40'
//     );

// eventlistener
document.addEventListener('DOMContentLoaded', function () {
  // submit event
  document.querySelector('body').addEventListener('submit', function (e) {
    var target = e.target;


//     // Append the modal backdrop element to the body
//     document.body.appendChild(modalBackdrop);
  })
});

// submit event
document.querySelector('body').addEventListener('submit', function (e) {
  console.log('gd');
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
        }
      })
      .catch(function (error) {
        console.error('AJAX request failed:', error);
      });
  }
});
