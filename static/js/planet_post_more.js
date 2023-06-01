// eventlistener
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('body').addEventListener('click', function(e) {
    var target = e.target;

    // 더보기 클릭
    if (target.tagName == 'circle' || (target.tagName == 'svg' && target.id == 'more')) {
      var parentDiv = target.closest('#post-container');
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

      dropdownMenus.forEach(function(menu) {
        if (menu.style.display == 'block') {
          menu.style.display = 'none';
        }
      });
    }
  });

  document.querySelector('body').addEventListener('submit', function(e) {
    var target = e.target;
    
    // 게시글 삭제
    if (target.matches('#delete-post-form')) {
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
  });
});

