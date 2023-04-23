const back = () => {
  window.history.back()
}

const collapseBtn = document.querySelector('.nav-collapse-btn')
const collapseArea = document.querySelector('.nav-collapse')
const collapseHidden = document.querySelector('.collapse-hidden')
const collapseBody = document.querySelector('section')

collapseBtn.addEventListener('mouseenter', () => {
  if (collapseArea.classList.contains('show')) {
    return;
  }
  collapseArea.classList.add('show');
});

collapseBtn.addEventListener('mouseleave', function(event) {
  if (!event.relatedTarget || !collapseArea.contains(event.relatedTarget)) {
    if (collapseArea.classList.contains('show')) {
      collapseArea.classList.remove('show')
    }
  }
})

collapseArea.addEventListener('mouseleave', () => {
  if (collapseArea.classList.contains('show')) {
    collapseArea.classList.remove('show');
  }
});

const searchBtns = document.querySelectorAll('.search-button')
const searchOption = document.querySelector('#search-option')
const searchSubmit = document.querySelector('#search-submit')
const searchCollapse = document.querySelector('.search-collapse')

searchBtns.forEach((btn) => {
  btn.addEventListener('click', (event) => {
    searchOption.textContent = event.target.textContent
    searchSubmit.value = event.target.textContent
    if (searchCollapse.classList.contains('show')) {
      searchCollapse.classList.remove('show')
    }
  })
})
