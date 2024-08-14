from flask import Flask,render_template, request, Response
import anthropic
import dotenv 
import os

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"

app = Flask(__name__)
app.secret_key = 'alura'

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)