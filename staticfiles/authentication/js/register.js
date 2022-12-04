console.log("register javascript")

const usernameField = document.getElementById("usernameField");
const feedbackArea = document.getElementsByClassName("invalid-feedback")[0];
const usernameSuccessOutput = document.getElementsByClassName("usernameSuccessOutput")[0];
const passwordToggle = document.getElementsByClassName("passwordToggle")[0];
const passwordField = document.getElementById("passwordField");

// togle SharedWorker/hide password
passwordToggle.addEventListener('click',()=> {
    if(passwordToggle.textContent === "Show") {
        passwordToggle.textContent = "Hide";
        passwordField.setAttribute('type',"text") 
    }
    else {
        passwordToggle.textContent = "Show";
        passwordField.setAttribute('type',"password") 
    }
})

// Checking whether username is valid or not.
usernameField.addEventListener('keyup',(e)=>{
    let usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";
    usernameSuccessOutput.textContent = `Checking for '${usernameVal}'...`
    
    
    if(usernameVal.length>0){
        usernameSuccessOutput.style.display = "block";
        fetch("/authenticate/validate-username/", {
            body:JSON.stringify({username:usernameVal}),
            method :"POST",
        }).then((res) =>res.json()).then((data)=> {
            // console.log("data",data);
            usernameSuccessOutput.style.display = "none";
            if(data.username_error) {
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML = `<p> ${data.username_error} </p>`;
            }
        });
    }
    // console.log("username:", usernameVal);
})