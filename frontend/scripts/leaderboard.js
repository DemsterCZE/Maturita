function get_leaderboard_data(){
    const http = new XMLHttpRequest();
    http.onload = function() {
        var json_data = JSON.parse(this.responseText)["data"];
        var current_position = 1;
        const tabulka = document.getElementById("tabulka")
        json_data.forEach(element => {
           var row = tabulka.insertRow(-1);
            var position_cell = row.insertCell(0);
            position_cell.innerHTML = String(current_position);
            var username_cell = row.insertCell(1);
            username_cell.innerHTML = element["username"];
            var score_cell = row.insertCell(2);
            score_cell.innerHTML = element["highest_score"];
            current_position++;
        });
    }

    http.open('GET','http://127.0.0.1:5000/get_users')
    http.send()
}

get_leaderboard_data();