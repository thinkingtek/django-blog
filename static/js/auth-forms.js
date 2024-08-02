const emailInput = document.getElementById("id_email");

// Converting email input to lowerCase
emailInput.addEventListener("input", function () {
    this.value = this.value.toLowerCase().trim();
});

// remove alert btn
function removeAlert() {
    const btn = document.querySelector(".message-alert");
    btn.classList.add("remove_alert")

}