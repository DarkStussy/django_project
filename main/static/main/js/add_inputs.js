let button_add = document.querySelector('.dynamic_fields .js-add');


button_add.addEventListener('click', function () {

    let students = document.querySelector('.dynamic_fields .students');

    let element = document.querySelector('.title_doc').cloneNode(true);

    element.classList.add('student');


    element.classList.remove('title_doc');

    students.appendChild(element);
});

document.addEventListener('click', function (el) {

    if (el.target && el.target.classList.contains('js-remove')) {

        let child = el.target.closest('.table');

        child.parentNode.removeChild(child);
    }
});