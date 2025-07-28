extends Button
@onready var auth_http : HTTPRequest = $"../Auth_request"
@onready var text_label = $"../Label"
@onready var log_out = $"../logout"


func _on_pressed():
	if Globalvar.loggedIn:
		text_label.add_theme_color_override("font_color",Color(0,255,0,120))
		text_label.text = "Už jste přihlášen!"
		await  wait(3)
		text_label.text = ""
		return
	
	var login = $"../login".text
	var password = $"../password".text
	var form_data = JSON.stringify({"login": login,"password":password})
	auth_http.request("http://127.0.0.1:5000/login",["Content-Type: application/json"],HTTPClient.METHOD_POST,form_data)
	print(form_data)



func _on_auth_request_request_completed(result, response_code, headers, body):
	if response_code != 200:
		text_label.add_theme_color_override("font_color",Color(255,0,0,120))
		text_label.text = JSON.parse_string(body.get_string_from_utf8())["Error"]
		await wait(1)
		text_label.text = ""
	else:
		text_label.add_theme_color_override("font_color",Color(0,255,0,120))
		var data = JSON.parse_string(body.get_string_from_utf8())
		text_label.text = data["Success"]
		Globalvar.token = data["Token"]
		Globalvar.loggedIn = true
		log_out.visible = true
		await wait(1)
		text_label.text = ""
		
		
func wait(seconds: float) -> void:
	await get_tree().create_timer(seconds).timeout
