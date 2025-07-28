function login_user(){
    const data = JSON.stringify({'login':document.getElementById('login').value,'password':document.getElementById('password').value});
    const http = new XMLHttpRequest();
    const label = document.getElementById("info");
    http.onload = function() {
        const response = JSON.parse(this.responseText);
        if(http.status == 200){
            localStorage.setItem("login_check",1)
            localStorage.setItem("logged_in",1)
            window.location.replace("./index.html")
        } else {
            label.textContent = response["Error"]
            label.style.color = "#ff8080"
        }
    }
    http.withCredentials = true
    http.open('POST','http://localhost:5000/login')
    http.setRequestHeader('Content-Type','application/json')
    http.send(data)
}

document.getElementById("form").addEventListener("submit", function(event){
    event.preventDefault()
    login_user()
    });
 