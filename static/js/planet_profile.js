// csrf token
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// 팔로잉
const followForm = document.querySelector('.follow-form')
followForm.addEventListener('submit', (e) => {
  e.preventDefault()
  const userPk = e.target.dataset.userPk
  const planetName = e.target.dataset.planetName
  
  axios({
    post:'post',
    url:`/planets/${planetName}/follow/${userPk}/`,
    headers: {'X-CSRFToken': csrftoken,}
  })
  .then((response) => {
    const isFollowed = response.data.is_followed
    const followBtn = document.querySelector('.follow-btn')

    if(isFollowed === true) {
      followBtn.value = 'following'
    }
    else {
      followBtn.value = 'follow'
    }
  })
  .catch((error) => {
    console.log(error.response)
  })
})