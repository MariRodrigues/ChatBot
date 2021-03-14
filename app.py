from flask import Flask, render_template, request
from bot import Bot

app = Flask('Chat_02')

bot = Bot()

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/get")
def get_bot_response():
	userText = request.args.get('msg') #Recebe o que o usuário escreveu
	return str(bot.processamento(userText.lower()))

if __name__ == "__main__":
	app.run()