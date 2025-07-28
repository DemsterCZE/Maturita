extends Node2D
signal coin_taken

func _ready():
	self.global_position = Vector2(randf_range(0,get_viewport().get_visible_rect().size.x-16),randf_range(0,get_viewport().get_visible_rect().size.y-100))
	

func _on_area_2d_body_entered(body):
	if(body.name == "micek"):
		Globalvar.score += 1
		coin_taken.emit()
		self.global_position = Vector2(randf_range(30,get_viewport().get_visible_rect().size.x-100),randf_range(30,get_viewport().get_visible_rect().size.y-100))
		

