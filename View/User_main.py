from Control.FlightBot import FlightBot
from Control.BBCbot import BBCbot
from Control.nlpbbc import summarize, sentiment_analysis


def flightBot_action():
    bot = FlightBot()
    bot.start()
    action = int(input("Choose Action:\n"
                       "1)Search keyword:"))
    if action == 1:
        word = input("\nEnter keyword:")
        bot.search(word)


def BBCbot_action():
    bot = BBCbot()
    bot.get_data()
    action = input(input("Choose Action:\n"
                         "1)Search keyword:"))
    if action == 1:
        word = input("\nEnter keyword:")
        df = bot.search(word)
        sentiment_analysis(df)
        print(summarize(df))


bot_choice = int(input("Choose Bot:\n"
                       "1)Flight Bot\n"
                       "2)BBC Bot\n"))
if bot_choice == 1:
    flightBot_action()
elif bot_choice == 2:
    BBCbot_action()
else:
    print("Wrong choice")
