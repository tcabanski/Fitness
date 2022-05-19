import os
import logging
from logging import config
from pickle import NONE
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
    #command is /leaderboard [ts of last leaderboard] For example, "1652975243.809649".  Have to test to see if the dot is required
    ack()
    try:
        logger.debug(f"received {command}")
        channel_id = command.get('channel_id')
        last_leaderboard_id = command.get("text")
        if last_leaderboard_id is None:
            respond("You must include the ID of the last leaderboard.  For exanmple, /leaderboard 1652975243.809649")
        else:
            #post a placeholder leaderboard
            response = say(f'Building Leaderboard from {last_leaderboard_id}')
            #add a visible timestamp to it
            ts = response.get("ts")
            client.chat_update(channel=channel_id, ts=ts, text=f'Building Leaderboard ID:{ts} from: {last_leaderboard_id}')

            #collect data since then (the while loop handles the pqagination of the call)
            while True:
                result = client.conversations_history(channel=channel_id, oldest=last_leaderboard_id, limit=100)
                #parse results
                conversation_history = result["messages"]
                #paginate
                next_cursor = result.get("next_cursor")
                if next_cursor is NONE or next_cursor="":
                    break
            #post leaderboard
            
            logger.info("{} messages found in {}".format(len(conversation_history), id))
            
            logger.debug('done')
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")

configure_logging()
logger = logging.getLogger("app")
logger.info('\n\n\n')
logger.info("====================================================== STARTUP ==============================================")

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