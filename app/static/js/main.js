const form = document.getElementById("form");
const message = document.getElementById("error-message");
const input = document.getElementById("username-input");
const result = document.getElementById("result");
const counter = document.getElementById("counter");
const count = document.getElementById("count");
const button = document.getElementById("submit")


form.addEventListener("submit", (event) => {
    // Prevent the form from being submitted the default way
    event.preventDefault();

    // Send the fetch request
    if (input.className === "valid")
        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `username=${encodeURIComponent(form.elements.username.value)}&context=${encodeURIComponent(form.elements.context.value)}`
        })
            .then(response => response.json())
            .then(responseJSON => {
                console.log(responseJSON)
                const element = document.getElementById("result");
                const error = document.getElementById("error-message");
                const input = document.getElementById("username-input")
                if (responseJSON.count < 0) {
                    element.innerHTML = '<i class="failure">&#10007;</i> Failure';
                    element.className = 'failure';
                    error.innerHTML = "Invalid username";
                    error.style.display = "block";
                    input.className = "invalid";
                } else {
                    element.innerHTML = '<i class="success">&#10003;</i> Success';
                    element.className = 'success';
                    form.elements.context.value = "";
                    count.innerHTML = responseJSON.count.toString();
                }
            })
            .catch(error => console.error(error));
});


input.addEventListener("blur", () => {
    counter.style.display = "none";
    fetch("/checkname", {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: `${form.elements.username.value}`
    })
        .then(response => response.json())
        .then(responseJSON => {
            if (Object.keys(responseJSON).length === 0 && responseJSON.constructor === Object) {
                input.className = "invalid";
                message.style.display = "block";
                message.innerHTML = "Please enter a valid username"

                
            } else {
                counter.style.display = "block";
                count.innerHTML = responseJSON.count.toString();
                input.className = "valid";
                message.style.display = "none";
                result.innerHTML = "";
            }
        })
});