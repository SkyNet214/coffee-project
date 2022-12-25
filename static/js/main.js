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
            element = document.getElementById("result");
            if (responseJSON.success) {
            
                element.innerHTML = '<i class="success">&#10003;</i> Success';
                element.className = 'success';
                form.elements.code.value = "";
                form.elements.context.value = "";
            } else {
                element.innerHTML = '<i class="failure">&#10007;</i> Failure';
                element.className = 'failure';
                
            }
        })
        .catch(error => console.error(error));
});