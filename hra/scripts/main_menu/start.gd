extends Button

@onready var text_prompt = $"../../label"


func _on_pressed() ->  void:
	if Globalvar.loggedIn:
		get_tree().change_scene_to_file("res://scenes/game.tscn")
	else:
		text_prompt.text = "Nejste přihlášený"
		await wait(2)
		text_prompt.text = ""
		
	
func wait(seconds: float) -> void:
	await get_tree().create_timer(seconds).timeout
