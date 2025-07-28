extends Area2D

@onready var Area = $"."

func _on_body_exited(body):
	if(body.name == "micek"):
		get_tree().change_scene_to_file("res://scenes/game_over.tscn")
		Input.set_custom_mouse_cursor(null)
