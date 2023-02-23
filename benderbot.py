import os
import praw
from datetime import datetime
import csv
import re
#from replit import db

reddit = praw.Reddit(
  client_id = os.environ['client_id'],
  client_secret = os.environ['client_secret'],
  user_agent = os.environ['user_agent'],
  username = os.environ['username'],
  password = os.environ['password'],
)

def clean_string(raw_string):
  cleaned_string = raw_string.lower()
  cleaned_string = re.sub("r[^A-Za-z0-9 ]+", "", cleaned_string)
  return cleaned_string

class Bot:
  def __init__(self, filename):
    self.responses = []

    #if len(db) == 0:
    with open(filename) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter = ";")
      for row in csv_reader:
        self.responses.append({'phrase': clean_string(row[0]), 'reply': row[1]})
    #print(self.responses)
    #db['responses'] = self.responses

    #else:
     # print("pulling from DB")
     # self.responses = db['responses']
    
    

  def find_match(self, comment):
    cString = clean_string(comment.body)
    for i, r in enumerate(self.responses):
      testC = r['phrase']
      if re.search(rf"\s{testC}$|^{testC}\s|\s{testC}\s|^{testC}$", cString):
      
      #if r['phrase'] in clean_string(comment.body):
        if self.cooldown(i):
          self.reply(i, comment)
          

  def cooldown(self, i):
    dic = self.responses[i]
    if 'last_posted' not in dic.keys():
      return True
    else:
      now = datetime.now()
      duration = now - datetime.fromtimestamp(dic['last_posted'])
      duration_seconds = duration.total_seconds()
      hours = divmod(duration_seconds, 3600)[0]
      if hours >= 24:
        return True
      else:
        print(f"Couldn't post {dic['phrase']}  Cooldown time: {24 - hours}")

    return False

  def reply(self, i, comment):
    dic = self.responses[i]
    try:
      #comment.reply(dic['reply'])
      print(comment.body)
      print(dic['phrase'])
      print(dic['reply'])
      
    except Exception as e:
      print(e)

    now = datetime.now()
    self.responses[i]['last_posted'] = now.timestamp()
    #db['responses'] = self.responses

#db.clear() #WARNING CLEARS DB AND TIMES
bot = Bot("BenderResponses.csv")
subreddit = reddit.subreddit("all")
for comment in subreddit.stream.comments(skip_existing=True):
  try:
    bot.find_match(comment)
  except Exception as e:
    print(e)