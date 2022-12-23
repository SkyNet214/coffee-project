document.getElementById("button").addEventListener("click", function () {
    fetch("/", {
        method: "GET"
        /*headers: {
            "Content-Type": "text/plain"
        },
        body: "login"*/
    })
})