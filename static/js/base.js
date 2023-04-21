const back = () => {
  window.history.back()
}

const collapseBtn = document.querySelector('.nav-collapse-btn');
const collapseArea = document.querySelector('.nav-collapse');
const collapseHidden = document.querySelector('.collapse-hidden');

collapseBtn.addEventListener('mouseenter', () => {
if (collapseArea.classList.contains('show')) {
  return;
}

collapseArea.classList.add('show');
});

collapseArea.addEventListener('mouseleave', () => {
collapseArea.classList.remove('show');
});
