
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("burger").addEventListener("click", function () {
        document.getElementById("burger").classList.toggle("active");
        document.getElementById("sidebar").classList.toggle("sactive");
    })
});