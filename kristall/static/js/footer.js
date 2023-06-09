// Визуализация скрытых полей футер
this.addEventListener('click', (e) => {
const elHeader = e.target.closest('.footer__nav-item');
if (!elHeader) {
    return
    console.log('Element not find');
}
const field = elHeader.querySelector('.footer_partnership_field');
field.classList.toggle('visible');
});