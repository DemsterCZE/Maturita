var logout_btn = document.createElement("input")
if(localStorage.getItem("login_check",1)){
    alert("Úspěšně přihlášen")
    localStorage.removeItem("login_check")
}
if(localStorage.getItem("registered")){
    alert("Úspěšně registrován")
    localStorage.removeItem("registered")
}
const login_btn = document.getElementById("login_btn");
const navbar = document.getElementById("navbar");


function get_user_details() {
        const http = new XMLHttpRequest();
        http.onload = function() {
            if (http.status === 200) {
                const response = JSON.parse(this.responseText);
                logout_btn.setAttribute("class","login")
                logout_btn.setAttribute("type","image")
                logout_btn.setAttribute("src","assets/logout.svg")
                logout_btn.setAttribute("width","48px")
                logout_btn.setAttribute("height","48px")
                login_btn.remove();
                navbar.appendChild(logout_btn)
                var user_detail = document.createElement('p');
                user_detail.setAttribute("style","right: 220px;")
                user_detail.setAttribute('class', 'login');
                user_detail.innerText = "Přihlášen jako " + response[0]["username"];
                navbar.appendChild(user_detail);
                if(response[0]["roleID"] === 1){
                    var control_panel = document.createElement("a")
                    control_panel.setAttribute("href","./admin_panel")
                    control_panel.setAttribute("class","odkaz")
                    control_panel.innerText = "Panel správce"
                    navbar.appendChild(control_panel)
                    control_panel.addEventListener
                }

            } else {
                
            }
        };
        http.withCredentials = true
        http.open('GET', 'http://localhost:5000/get_me',true);
        http.setRequestHeader('Content-Type', 'application/json');
        http.send();
    };

if(localStorage.getItem("logged_in")){
get_user_details()
}


function logout(){
    const http = new XMLHttpRequest();
    http.withCredentials = true
    http.open('GET', 'http://localhost:5000/logout',true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.send();
    localStorage.removeItem("logged_in")
    window.location.reload()
}
logout_btn.addEventListener("click", logout)