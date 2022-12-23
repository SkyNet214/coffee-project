async function checkId(id) {
    const json = await fetch(`/idlist?id=${id}`).then(response => response.json())
    const valid = await json.valid ? json !== {} : false
    return valid
    
}

async function useId(id, remarks) {
    const valid = await checkId(id)
    if (valid) {
        const json = JSON.stringify({
            id: id,
            valid: false,
            remarks: remarks
        })
        const response = await fetch(`/idlist`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: `${json}`
        }).then((response) => response.json())
        success = response.success ? response != {} : false
        return {
            valid: true,
            success: success
        }
        
    } else {
        return {
            valid: false,
            success: false
        }
    }
}

document.getElementById("check").addEventListener("click", function () {
    checkId(document.getElementById("id").value).then(function (valid) {
            result_element = document.getElementById("validation")
            if (valid) {
                result_element.innerHTML = "\u2714 VALID"
                result_element.classList.remove("invalid")
                result_element.classList.add("valid")
            } else {
                result_element.innerHTML = "\u274C INVALID"
                result_element.classList.remove("valid")
                result_element.classList.add("invalid")
            }
        })
})

document.getElementById("submit").addEventListener("click", function () {
    useId(document.getElementById("id").value, document.getElementById("remarks").value).then((result) => {
        element = document.getElementById("validation")
        if (result.valid && result.success) {
            element.innerHTML = "\u2714 SUCCESS"
            element.classList.remove("invalid")
            element.classList.add("valid")
            document.getElementById("id").value = ""
            document.getElementById("remarks").value = ""
        } else if (!result.valid) {
            element.innerHTML = "\u274C INVALID"
            element.classList.remove("valid")
            element.classList.add("invalid")
        } else if (!result.success) {
            element.innerHTML = "\u274C ERROR 500"
            element.classList.remove("valid")
            element.classList.add("invalid")
        } else {
            element.innerHTML = "\u274C ERROR"
            element.classList.remove("valid")
            element.classList.add("invalid")
        }
    })
})

