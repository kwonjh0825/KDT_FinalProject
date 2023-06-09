// 이미지를 눌러야 투표 폼이 생김
const voteToggle = document.getElementById('vote-toggle');
const voteTopicsContainer = document.getElementById('vote-topics-container');

voteToggle.addEventListener('click', function () {
  if (voteTopicsContainer.style.display === 'none') {
    voteTopicsContainer.style.display = 'block';
  } else {
    voteTopicsContainer.style.display = 'none';
  }
});

const plusButton = document.getElementById('plus-button');
const voteTopics = document.getElementById('vote-topics');

plusButton.addEventListener('click', function () {
  event.preventDefault(); // 폼 제출 방지
  const newTopicInput = document.createElement('input');
  newTopicInput.type = 'text';
  newTopicInput.name = 'title';
  newTopicInput.classList.add(
    'block',
    'mt-2',
    'w-full',
    'bg-[#101013]',
    'text-white',
    'rounded-lg',
    'py-2',
    'px-3'
  );

  const deleteButton = document.createElement('button');
  deleteButton.textContent = '-';
  deleteButton.setAttribute('class', 'delete-button');
  deleteButton.addEventListener('click', function () {
    voteTopics.removeChild(newTopicInput.parentNode);
  });

  const inputWrapper = document.createElement('div');
  inputWrapper.setAttribute('class', 'vote-topic-input');
  inputWrapper.appendChild(newTopicInput);
  inputWrapper.appendChild(deleteButton);

  voteTopics.appendChild(inputWrapper);
});

// function submitForm(event) {
//   event.preventDefault(); // 폼 제출 방지
//   const form = document.getElementById('post-form');
//   const topicInputs = form.querySelectorAll('.vote-topic-input input');
//   const contentInput = form.querySelector('#id_content');
//   const formData = new FormData();

//   let hasEmptyInput = false;

//   for (let i = 0; i < topicInputs.length; i++) {
//     const topicValue = topicInputs[i].value.trim();
//     if (topicValue !== '') {
//       formData.append('title', topicValue);
//     } else {
//       hasEmptyInput = true;
//     }
//   }

//   const contentValue = contentInput.value.trim();
//   if (contentValue === '') {
//     alert('내용 입력란을 채워주세요.');
//     return;
//   }
//   formData.append('content', contentValue);

//   if (hasEmptyInput) {
//     alert('투표 주제 입력란을 모두 채워주세요.');
//     return;
//   }

//   // AJAX를 통해 폼 데이터 전송하거나 formData 객체를 이용해 폼 제출
//   // fetch API를 사용한 예시:
//   // fetch('/your-form-endpoint/', {
//   //     method: 'POST',
//   //     body: formData
//   // })
//   //     .then(response => {
//   //         // 성공적인 응답 처리
//   //     })
//   //     .catch(error => {
//   //         // 에러 처리
//   //     });
//   // 폼을 직접 제출하는 예시:
//   // form.submit();
// }
