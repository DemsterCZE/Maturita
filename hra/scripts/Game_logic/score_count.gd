extends Label

func _on_coin_coin_taken():
	self.text = "Tvoje skóre : " + str(Globalvar.score)
