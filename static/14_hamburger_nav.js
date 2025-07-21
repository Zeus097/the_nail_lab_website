document.addEventListener("DOMContentLoaded", () => {

    const hamburger = document.getElementById('hamburger');
    const nav = document.querySelector('.base-navigation-bar');

    if (hamburger && nav) {
        hamburger.addEventListener('click', () => {
            nav.classList.toggle('open');
        });
    }
});
