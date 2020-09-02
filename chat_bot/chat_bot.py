import aiml
import os

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("./chat_bot/covid_bot.aiml")
kernel.respond("load aiml files")

'''
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")
'''
# Press CTRL-C to break this loop



