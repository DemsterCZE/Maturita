extends Node2D

func _on_micek_body_entered(body):
	if(body.name == "paddle"):
		$ping.play()
