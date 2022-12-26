const form = document.getElementById("form");

// document.getElementById("code-input").setCustomValidity("Please enter a 4-digit code!");

form.addEventListener("submit", (event) => {
    // Prevent the from from being submitted the default way
    event.preventDefault();

    // Send the fetch request
    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `code=${encodeURIComponent(form.elements.code.value)}&context=${encodeURIComponent(form.elements.context.value)}`
    })
        .then(response => response.json())
        .then(responseJSON => {
            console.log(responseJSON)
            const element = document.getElementById("result");
            const error = document.getElementById("error-message");
            const input = document.getElementById("code-input")
            if (responseJSON.success) {
            
                element.innerHTML = '<i class="success">&#10003;</i> Success';
                element.className = 'success';
                form.elements.code.value = "";
                form.elements.context.value = "";
            } else {
                element.innerHTML = '<i class="failure">&#10007;</i> Failure';
                element.className = 'failure';
                error.innerHTML = "Invalid code";
                error.style.display = "block";
                input.className = "invalid";
            }
        })
        .catch(error => console.error(error));
});

const message = document.getElementById("error-message");
const input = document.getElementById("code-input");
const result = document.getElementById("result");
input.addEventListener("blur", () => {
    if (input.checkValidity()) {
        input.className = "valid";
        message.style.display = "none";
        result.innerHTML = "";
    } else {
        input.className = "invalid";
        message.style.display = "block";
        message.innerHTML = "Please enter a 4-digit code"
    }
});