document.addEventListener('DOMContentLoaded', function () {
  const addTermBtn = document.getElementById('add-term-btn');
  const termFieldsContainer = document.getElementById('term-fields-container');
  let termCount = 0;

  addTermBtn.addEventListener('click', function () {
    termCount++;

    const termField = document.createElement('div');
    termField.innerHTML = `
      <label for="term_content_${termCount}">Term Content:</label>
      <input type="text" class="text-black" id="term_content_${termCount}" name="term_content_${termCount}">
      <button type="button" class="delete-term-btn" data-term-count="${termCount}">Delete</button>
      <br>
    `;

    termFieldsContainer.appendChild(termField);
    document.getElementById('num-terms').value = termCount;
  });

  termFieldsContainer.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-term-btn')) {
      const termCount = event.target.getAttribute('data-term-count');
      const termField = document.getElementById(`term_content_${termCount}`).parentNode;
      termField.remove();
      document.getElementById('num-terms').value = termFieldsContainer.children.length;
    }
  });
});