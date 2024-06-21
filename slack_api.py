from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_SOCKET_TOKEN = os.getenv('SLACK_SOCKET_TOKEN')
SERVICE_URL = os.getenv('SERVICE_URL')
ANSWERS_STR = str(os.getenv('ANSWERS'))

ANSWERS = json.loads(ANSWERS_STR)


app = App(token=SLACK_TOKEN)

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    """
    Function to handle the app home
    Args:
        Client: the view object
        event: The event which called the function
        logger: an object to write things in the log
    """
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Welcome home, <@" + event["user"] + "> :house:"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "To use Emotion is simple, just type /predict and the text which you want to analyze"
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

@app.command("/prescribe")
def predict_command(ack, say, command):
    """
    /prescribe command handler
    Args:
        ack (ack): function to confirm the request was sent
        say (callable): function to write something in the slack channel (the app need to have been added).
        command (dict): what was sent to this command by the user.

    Returns:
        A message in slack channel
    """

    ack()
    text = command["text"]
    say(f"Analisando: {text}")

    try:
        url = f"{SERVICE_URL}/prescribe"
        request_clean = requests.get(url, params={"text": text})
        request_clean.raise_for_status()
        response_clean = request_clean.json()
        
        response_predict = str(response_clean["predictions"])
        
        possible_answers = ANSWERS
        
        bool = response_predict in  possible_answers 

        if bool:
            sentiment = possible_answers[response_predict]
            say(f"Resultado: {sentiment}")
            say(":white_check_mark: Concluído!")
        else:
            raise Exception
        
    except requests.exceptions.RequestException as e:
        say(f":x: Erro ao processar: {text}\n> {str(e)}")
   
# Run the app using Socket Mode Handler
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_SOCKET_TOKEN)
    handler.start()