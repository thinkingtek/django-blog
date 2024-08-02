// remove alert btn
function removeAlert() {
    const btn = document.querySelector(".message-alert");
    btn.classList.add("remove_alert")

}

// toggle sidebar
function toggle_sidebar() {
    const body = document.getElementById('body')
    const sidebar = document.querySelector('.mobile_nav')
    if (sidebar) {
        sidebar.classList.toggle("show_sidebar")
        body.classList.toggle("body_overflow_hidden")
    }
}

// scrolltop
function showScroll() {
    const scrollTop = document.getElementById("scroll-top");
    if (this.scrollY >= 500) {
        scrollTop.classList.add("show-scroll");
    } else {
        scrollTop.classList.remove("show-scroll");
    }
}

function scrollToTop() {
    window.scroll({ top: 0, left: 0, behavior: 'smooth' });
}

window.addEventListener("scroll", showScroll);