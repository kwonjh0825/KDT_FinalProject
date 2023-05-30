  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  const deleteForms = document.querySelectorAll('.delete-post-form')
  deleteForms.forEach((btn) => {
    btn.addEventListener('submit', (e) => {
      e.preventDefault()
      const postPk = e.target.dataset.postPk
      const planetName = e.target.dataset.planetName
      if(confirm('삭제처리 하시겠습니까 ?')) {
        axios({
          method:'post',
          url:`/planets/${planetName}/${postPk}/delete/`,
          headers:{'X-CSRFToken': csrftoken,}
        })
        .then((response) => {
          if(response.data.success === true) {
            alert('삭제 완료되었습니다.')
            const reportDiv = document.getElementById(`report-form-${postPk}`)
            reportDiv.remove()
          }
        })
        .catch((error) => {
          console.log(error.response)
        })
      }
    })
  })