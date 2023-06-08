const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const deletePostForms = document.querySelectorAll('.delete-post-form')
deletePostForms.forEach((btn) => {
  btn.addEventListener('submit', (e) => {
    e.preventDefault()
    const postPk = e.target.dataset.postPk
    const planetName = e.target.dataset.planetName
    
    const reportPostList = document.getElementById('report-post-list')

    if(confirm('게시물 삭제처리 하시겠습니까 ?')) {
      axios({
        method:'post',
        url:`/planets/${planetName}/post/${postPk}/delete/`,
        headers:{'X-CSRFToken': csrftoken,}
      })
      .then((response) => {
        if(response.data.success === true) {
          alert('삭제 완료되었습니다.')
          const reportDiv = document.getElementById(`report-postform-${postPk}`)
          reportDiv.remove()

          if(reportPostList.childElementCount < 1) {
            const nolistDiv = document.createElement('p')
            nolistDiv.textContent = '신고된 내역이 없습니다.'
            reportPostList.appendChild(nolistDiv)
          }
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
    }
  })
})

const deleteCommentForms = document.querySelectorAll('.delete-comment-form')
deleteCommentForms.forEach((btn) => {
  btn.addEventListener('submit', (e) => {
    e.preventDefault()
    const commentPk = e.target.dataset.commentPk
    const planetName = e.target.dataset.planetName
    
    const reportCommentList = document.getElementById('report-comment-list')

    if(confirm('댓글 삭제처리 하시겠습니까 ?')) {
      axios({
        method:'post',
        url:`/planets/${planetName}/comment/${commentPk}/delete/`,
        headers:{'X-CSRFToken': csrftoken,}
      })
      .then((response) => {
        if(response.data.success === true) {
          alert('삭제 완료되었습니다.')
          const reportDiv = document.getElementById(`report-commentform-${commentPk}`)
          reportDiv.remove()

          if(reportCommentList.childElementCount < 1) {
            const nolistDiv = document.createElement('p')
            nolistDiv.textContent = '신고된 내역이 없습니다.'
            reportCommentList.appendChild(nolistDiv)
          }
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
    }
  })
})

const deleteRecommentForms = document.querySelectorAll('.delete-recomment-form')
deleteRecommentForms.forEach((btn) => {
  btn.addEventListener('submit', (e) => {
    e.preventDefault()
    const recommentPk = e.target.dataset.recommentPk
    const planetName = e.target.dataset.planetName
    
    const reportRecommentList = document.getElementById('report-recomment-list')

    if(confirm('대댓글 삭제처리 하시겠습니까 ?')) {
      axios({
        method:'post',
        url:`/planets/${planetName}/recomment/${recommentPk}/delete/`,
        headers:{'X-CSRFToken': csrftoken,}
      })
      .then((response) => {
        if(response.data.success === true) {
          alert('삭제 완료되었습니다.')
          const reportDiv = document.getElementById(`report-recommentform-${recommentPk}`)
          reportDiv.remove()
          
          if(reportRecommentList.childElementCount < 1) {
            const nolistDiv = document.createElement('p')
            nolistDiv.textContent = '신고된 내역이 없습니다.'
            reportRecommentList.appendChild(nolistDiv)
          }
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
    }
  })
})