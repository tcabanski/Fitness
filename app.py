import os
import logging
from logging import config
from slack_bolt import App

def configure_logging():
    log_config = {
        "version":1,
        "root":{
        "handlers" : ["console", "file"],
        "level": "DEBUG"    
        },
        "handlers":{
            "console":{
                "formatter": "std_out",
                "class": "logging.StreamHandler",
                "level": "DEBUG"
            },
            "file":{
                "formatter":"std_out",
                "class":"logging.handlers.TimedRotatingFileHandler",
                "level":"DEBUG",
                "filename":"logs/app.log",
                "when": "D"
            }
        },
        "formatters":{
            "std_out": {
                "format": "%(asctime)s %(levelname)s : %(module)s : %(funcName)s : %(message)s",
                "datefmt":"%d-%m-%Y %I:%M:%S"
            }
        },
    }

    config.dictConfig(log_config)

def handle_echo_command(ack, respond, command):
    ack()
    logger.debug(f"received {command}")
    respond(f"{command['text']}")

def handle_leaderboard_command(ack, say, respond, command, client):
    ack()
    logger.debug(f"received {command}")
    channelId = command.get('channel_id')
    response = say('Handling leaderboard')
    ts = response.get("ts")
    client.reactions_add(channel=channelId, name='smile', timestamp=ts)
    logger.debug('done')

configure_logging()
logger = logging.getLogger("app")

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# The echo command simply echoes on command
@app.command("/echo")
def echo_command(ack, respond, command):
    handle_echo_command(ack, respond, command)

@app.command("/leaderboard")
def leaderboard_command(ack, say, respond, command, client):
    handle_leaderboard_command(ack, say, respond, command, client)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))