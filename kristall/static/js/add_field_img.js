// Скрипт управления
let imageForm = document.querySelectorAll(".unit-image")
let containerImages = document.querySelector(".images-form")
let addButtonImage = document.querySelector("#add-a-form")
let totalForms = document.getElementById("id_form-TOTAL_FORMS")

let formNum = imageForm.length-1
addButtonImage.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = imageForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')
    
    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    containerImages.insertBefore(newForm, addButtonImage)

    totalForms.setAttribute('value', `${formNum+1}`)
}
