  // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  // const deleteForms = document.querySelectorAll('.delete-post-form')
  // deleteForms.forEach((btn) => {
  //   btn.addEventListener('submit', (e) => {
  //     e.preventDefault()
  //     const postPk = e.target.dataset.postPk
  //     const planetName = e.target.dataset.planetName
  //     if(confirm('삭제처리 하시겠습니까 ?')) {
  //       axios({
  //         method:'post',
  //         url:`/planets/${planetName}/${postPk}/delete/`,
  //         headers:{'X-CSRFToken': csrftoken,}
  //       })
  //       .then((response) => {
  //         if(response.data.success === true) {
  //           Swal.fire('삭제 완료되었습니다.')
  //           const reportDiv = document.getElementById(`report-form-${postPk}`)
  //           reportDiv.remove()
  //         }
  //       })
  //       .catch((error) => {
  //         console.log(error.response)
  //       })
  //     }
  //   })
  // })

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const deleteForms = document.querySelectorAll('.delete-post-form');
  deleteForms.forEach((btn) => {
    btn.addEventListener('submit', (e) => {
      e.preventDefault();
      const postPk = e.target.dataset.postPk;
      const planetName = e.target.dataset.planetName;
      Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
          axios({
            method:'post',
            url:`/planets/${planetName}/${postPk}/delete/`,
            headers:{'X-CSRFToken': csrftoken,}
          })
          .then((response) => {
            if(response.data.success === true) {
              Swal.fire('삭제 완료되었습니다.')
              const reportDiv = document.getElementById(`report-form-${postPk}`)
              reportDiv.remove()
            }
          })
          .catch((error) => {
            console.log(error.response)
          })
        }
      });
    })
  });
  
