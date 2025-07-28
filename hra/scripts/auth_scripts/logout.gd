extends Button
@onready var text_label = $"../Label"
@onready var log_out = $"."
func _ready():
	if Globalvar.loggedIn:
		log_out.visible = true

func _pressed():
	if Globalvar.loggedIn:
		Globalvar.token = ""
		Globalvar.loggedIn = false
		text_label.text = "Úspěšně odhlášen"
		text_label.add_theme_color_override("font_color",Color(0,255,255,120))
		log_out.visible = false
		await wait(2)
		text_label.text = ""
		

func wait(seconds: float) -> void:
	await get_tree().create_timer(seconds).timeout
