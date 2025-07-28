function registerUser(){
    const http =  new XMLHttpRequest();
    const username = document.getElementById("username_reg").value;
    const email = document.getElementById("email_reg").value;
    const password = document.getElementById("password_reg").value;
    const data = JSON.stringify({"username":username,"email":email,"password":password});
    const label = document.getElementById("info");
    http.onload = function(){
        const response = JSON.parse(this.responseText);
        if(http.status == 200){
            localStorage.setItem("registered",1)
            window.location.replace("./index.html")
        } else {
            label.textContent = response["Error"]
            label.style.color = "#ff8080"
        }
    }

http.open('POST','http://localhost:5000/register')
http.setRequestHeader('Content-Type','application/json')
http.send(data)


}


form.addEventListener("submit", function(event){

event.preventDefault();
registerUser();
});