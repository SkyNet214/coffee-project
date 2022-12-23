document.getElementById("button").addEventListener("click", function () {
    p = document.getElementById("paragraph")
    if (p.innerHTML == "") {
        fetch("text.txt").then(function (response) {
            response.text().then(function (text) {
                document.getElementById("paragraph").innerHTML = text
            })
        })
    } else {
        p.innerHTML = ""
    }
})