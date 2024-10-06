document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const navig = document.querySelector('.navig');

    burger.addEventListener('click', () => {
        navig.classList.toggle('nav-active');
    });
});
