extends Control
@onready var score_label : Label = $current_score
@onready var get_highest_score = $get_highest_score
@onready var best_score_label = $best_score
@onready var update_score = $update_score
signal new_highest_score
var headers = ["Content-Type: application/json","Authorization: Bearer "+str(Globalvar.token)]
func _ready():
	score_label.text = "Your score : " + str(Globalvar.score)
	get_highest_score.request_completed.connect(_on_get_highest_score_request_completed)
	get_highest_score.request("http://127.0.0.1:5000/get_me",headers)
	
func _on_get_highest_score_request_completed(result, response_code, headers, body):
	var data = JSON.parse_string(body.get_string_from_utf8())
	var highest_score = data[0]["highest_score"]
	if Globalvar.score > highest_score:
		highest_score = Globalvar.score
		best_score_label.text = "Best score :"+ str(highest_score)
		$hi.play()
		new_highest_score.emit()
	else:
		$AudioStreamPlayer.play()
		best_score_label.text = "Best score :"+ str(highest_score)
		
	



func _on_new_highest_score():
	var payload = JSON.stringify({"score":Globalvar.score})
	update_score.request("http://127.0.0.1:5000/update_score",headers,HTTPClient.METHOD_PATCH,payload)
