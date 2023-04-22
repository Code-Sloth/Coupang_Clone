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

// collapseBtn.addEventListener('mouseleave', () => {
//   collapseArea.classList.remove('show');
//   });
// collapseBody.addEventListener('mouseenter', () => {
//   if (collapseArea.classList.contains('show')) {
//     collapseArea.classList.remove('show');
//   }
// });

// 이벤트 객체의 relatedTarget 속성을 통해 마우스 이벤트가 일어난 대상 요소를 확인합니다.
// 만약 이벤트 대상 요소가 콜랩스 영역에 포함되어 있지 않거나,
// 관련 요소가 없는 경우(마우스가 페이지 바깥으로 이동한 경우)에만 동작합니다.
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