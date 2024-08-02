function deletePost() {
    const body = document.querySelector("#body");
    const overlay = document.querySelector("#overlay-container");
    overlay.style.display = 'flex';
    body.style.overflow = 'hidden';
}

function rvmOverlay() {
    const body = document.querySelector("#body");
    const overlay = document.getElementById("overlay-container");
    overlay.style.display = 'none';
    body.style.overflow = 'auto';
}