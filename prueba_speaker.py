from speaker import Speaker

sp = Speaker()
text = ""

while text != "x":
    text = input("> ")
    sp.speak_async(text)