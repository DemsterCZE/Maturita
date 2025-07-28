extends CanvasLayer
@export var empty_cursor : Texture


# Called when the node enters the scene tree for the first time.
func _ready():
	Input.set_custom_mouse_cursor(empty_cursor,Input.CURSOR_ARROW)
	
func _process(delta):
	$Sprite.global_position = $Sprite.get_global_mouse_position()
