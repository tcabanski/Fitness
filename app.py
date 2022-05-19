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

configure_logging()
logger = logging.getLogger("app")

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# The echo command simply echoes on command
@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")
    logger.debug(f"received {command}")
    
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))