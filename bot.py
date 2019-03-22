# coding=utf-8
import logging, settings, time

from telegram import *
from telegram.ext import *

import feedparser

last_update = time.localtime()

updater = Updater(settings.key) #api key from file "key.py", create your's as shown in "key_sample.py"


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def update(bot, job):
    global last_update
    posts = feedparser.parse(settings.rss_feed).entries
    new = []
    for post in posts:
        if post.published_parsed >= last_update:
            new.append(post.link)
    logger.info("sending {} posts".format(len(new)))
    new.reverse()
    for post in new:
        bot.sendMessage(text = post, chat_id = settings.chat)
    last_update = time.localtime()


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    logger.info("Starting")
    dp = updater.dispatcher #not double penetration
    dp.add_error_handler(error)

    j = updater.job_queue
    j.run_repeating(update, interval=60, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
