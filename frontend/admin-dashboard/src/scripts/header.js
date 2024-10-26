
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("arrow").addEventListener("click", function () {
        document.getElementById("full__content").classList.toggle("hiden");
        document.getElementById("arrow").classList.toggle("arrow_rev");
        document.getElementById("show__btn").classList.toggle(".license__card__full");
    })
});