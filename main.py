from telegram.ext import Updater, CommandHandler
import requests
from xkcd import *
import logging
import re
import os.path
import json

subscriberChats = []
latestComic = 0
subscribersFile = "subscribers.json"

def start(bot, update):
	update.message.reply_text(
		"Hey! I'm xkcd bot. "
		"Here is my list of commands:\n"
		"/subscribe - I'll notify you whenever a new xkcd is released.\n"
		"/unsubscribe - I'll stop notifying you when new xkcd comics are released.\n"
		"/xkcd - Type in the comic number and I'll find it for you! Type nothing and I'll send you the latest xkcd.\n"
		"/random - I'll send you a random xkcd.")

def subscribe(bot, update):
	global subscriberChats
	if update.message.chat_id not in subscriberChats:
		subscriberChats.append(update.message.chat_id)
		update.message.reply_text(
			"You are now subscribed.\n"
			"From now on I will send you new xkcd comics when they are released.\n"
			"If you wish to unsubscribe, send me a /unsubscribe command.")
	else:
		update.message.reply_text(
			"Hey you're already subscribed!\n"
			"Did you mean /unsubscribe?")

def unsubscribe(bot, update):
	global subscriberChats
	if update.message.chat_id in subscriberChats:
		subscriberChats.remove(update.message.chat_id)
		update.message.reply_text("You have been unsubscribed.")
	else:
		update.message.reply_text("Hey you're not even subscribed to begin with!")

def xkcd(bot, update):
	if update.message.text == "/xkcd" or update.message.text == "/xkcd latest":
		comic = getLatestComic()
		print(comic["img"])
		print(comic["num"])
		bot.send_photo(update.message.chat_id, comic["img"])
		bot.send_message(update.message.chat_id, "xkcd "+str(comic["num"])+"\nAlt-text: "+comic["alt"])

	elif update.message.text == "/xkcd random":
		comic = getRandomComic(latestComic)
		print(comic["img"])
		print(comic["num"])
		bot.send_photo(update.message.chat_id, comic["img"])
		bot.send_message(update.message.chat_id, "xkcd "+str(comic["num"])+"\nAlt-text: "+comic["alt"])

	else:
		xkcdNumber = int(re.search(r'\d+', update.message.text).group())
		comic = getComic(xkcdNumber)
		print(comic["img"])
		print(comic["num"])
		bot.send_photo(update.message.chat_id, comic["img"])
		bot.send_message(update.message.chat_id, "xkcd "+str(comic["num"])+"\nAlt-text: "+comic["alt"])

def random(bot, update):
	comic = getRandomComic(latestComic)
	print(comic["img"])
	print(comic["num"])
	bot.send_photo(update.message.chat_id, comic["img"])
	bot.send_message(update.message.chat_id, "xkcd "+str(comic["num"])+"\nAlt-text: "+comic["alt"])

def comicNotify(bot, job):
	comic = getLatestComic()
	if comic["num"] > latestComic:
		for chat_id in subscriberChats:
			bot.send_message(chat_id, "A new xkcd is out!")
			bot.send_photo(chat_id, comic["img"])
			bot.send_message(chat_id, "xkcd "+str(comic["num"])+"\nAlt-text: "+comic["alt"])

		setLatestComic()

def setLatestComic():
	global latestComic
	comic = getLatestComic()
	latestComic = comic["num"]

def readSubscribers():
	global subscriberChats
	with open(subscribersFile, "r") as infile:
		subscriberJson = json.load(infile)
		subscriberChats = subscriberJson["subscribers"]

def saveSubscribers(bot, job):
	with open(subscribersFile, "w") as outfile:
		finalJson = {}
		finalJson["subscribers"] = subscriberChats
		json.dump(finalJson, outfile)

def main():
	# First load our subscriber list if it exists:
	if os.path.isfile(subscribersFile):
		readSubscribers()

	# Set up logging to stdout. Todo: Actually make a log file.
	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	
	# Configure updater with our API token.
	updater = Updater("You should insert your API token here")

	# Create dispatcher and register commands.
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", start))
	dp.add_handler(CommandHandler("commands", start))
	dp.add_handler(CommandHandler("subscribe", subscribe))
	dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
	dp.add_handler(CommandHandler("xkcd", xkcd))
	dp.add_handler(CommandHandler("random", random))

	# Set latest available comic.
	setLatestComic()

	# Create scheduled job for notifying people about new comics (checks every 30 min).
	notifierJob = updater.job_queue.run_repeating(comicNotify, interval=1800, first=0)
	notifierJob.enabled = True

	# Create scheduled job for saving the subscriber list to disk every minute.
	subscriberSavingJob = updater.job_queue.run_repeating(saveSubscribers, interval=60, first=60)
	subscriberSavingJob.enabled = True

	# Start the bot.
	updater.start_polling()

	updater.idle()

	# Save the subscribers one last time before exiting.
	saveSubscribers(updater.bot, subscriberSavingJob)

if __name__ == '__main__':
	main()