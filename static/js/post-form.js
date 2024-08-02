const titleInput = document.querySelector('input[name=title]');
const slugInput = document.querySelector('input[name=slug]');

const slugify = (val) => {

    return val.toString().toLowerCase().trim()
        .replace(/&/g, '-and-')         // Replace & with 'and'
        .replace(/[\s\W-]+/g, '-')      // Replace spaces, non-word characters and dashes with a single dash (-)

};

titleInput.addEventListener('keyup', (e) => {
    slugInput.setAttribute('value', slugify(titleInput.value));
    console.log('Working')
});


// checkbox validations for limit
const errorcheckbox = document.querySelector('.validate-checkbox')
const validateCheck = (e => {
    let checkboxes = document.getElementsByName('categories');
    let numofChoices = 0
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            numofChoices++
        }
        if (numofChoices < 2) {
            errorcheckbox.style.display = "none"
        } else if (numofChoices > 2) {
            errorcheckbox.style.display = "block"
            return false
        }

    }
})