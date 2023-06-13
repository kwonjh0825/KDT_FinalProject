const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const planetName = document.querySelector('.planet_name').innerHTML
    
const joinConfirms = document.querySelectorAll('.join-confirm')
joinConfirms.forEach((confirms) => {
  confirms.addEventListener('submit', (event) => {
    event.preventDefault()
    const userpk = event.target.dataset.userPk
    if (confirm('승인하시겠습니까 ?')) {
      axios({
        method:'post',
        url:`/planets/${planetName}/admin/join/${userpk}/confirm/`,
        headers:{'X-CSRFToken': csrftoken,},
      })
      .then(function(response) {
        if (response.data.success) {
          const confirmDiv = document.getElementById(`join-form-${userpk}`)
          confirmDiv.remove()
          alert('승인 처리되었습니다. ')
          const confirmList = document.querySelector('.confirm-list')
          if (confirmList.textContent.trim() === '') {
            const noList = document.createElement('p')
            noList.textContent = '가입 대기중인 유저가 없습니다.'
            confirmList.appendChild(noList)
          }
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
    }
  })
})

const joinRejects = document.querySelectorAll('.join-reject')
joinRejects.forEach((reject) => {
  reject.addEventListener('submit', (event) => {
    event.preventDefault()
    const userpk = event.target.dataset.userPk
    if (confirm('가입 거부 하시겠습니까?')) {
      axios({
        method:'post',
        url:`/planets/${planetName}/admin/join/${userpk}/reject/`,
        headers:{'X-CSRFToken': csrftoken,},
      })
      .then(function(response) {
        if (response.data.success) {
          const confirmDiv = document.getElementById(`join-form-${userpk}`)
          confirmDiv.remove()
          alert('거부 처리되었습니다. ')
          const confirmList = document.querySelector('.confirm-list')
          if (confirmList.textContent.trim() === '') {
            const noList = document.createElement('p')
            noList.textContent = '가입 대기중인 유저가 없습니다.'
            confirmList.appendChild(noList)
          }
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
    }
  })
})