
// Для визуализации активных кнопок меню
let menuLinks = document.querySelectorAll('.auto_active_link');
for (let link of menuLinks) {
link.classList.remove('active');
}
for (let link of menuLinks) {
let currentLink = localStorage.getItem('active_link');
if (link.id === currentLink) {
    link.classList.add('active');
}
}

document.addEventListener('click', (event) => saveNextLink(event));

function saveNextLink(event) {
let link = event.target.closest('.auto_active_link');
if (link) {
    localStorage.setItem('active_link', link.id);
}
}

// Для визуализации меню быстрый поиск

this.addEventListener('click', (e) => {
const elHeader = e.target.closest('.header__search-link');
if (!elHeader) {
    return
    console.log('Element not find');
}
const field = elHeader.parentElement.querySelector('.header__icon-search_field');
field.classList.toggle('search');
});