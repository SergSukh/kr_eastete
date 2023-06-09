this.addEventListener('click', (e) => {
const elHeader = e.target.closest('.accordion__header');
if (!elHeader) {
    return
    console.log('Element not find');
}
const elips = elHeader.querySelector('.section-questions__question-icon');
elHeader.parentElement.classList.toggle('body_show');
elips.classList.toggle('deactivate')
});