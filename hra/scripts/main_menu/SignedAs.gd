extends Label
@onready var label = $"."
@onready var http = $"../get_player_name"
# Called when the node enters the scene tree for the first time.
func _ready():
	if Globalvar.loggedIn:
		http.request_completed.connect(_on_get_player_name_request_completed)
		var headers = ["Content-Type: application/json","Authorization: Bearer "+str(Globalvar.token)]
		http.request("http://127.0.0.1:5000/get_me",headers) 
	else:
		label.visible = false
		


func _on_get_player_name_request_completed(result, response_code, headers, body):
	var data = JSON.parse_string(body.get_string_from_utf8())
	label.visible = true
	label.text = "Přihlášen jako: " +str(data[0]["username"])
	
