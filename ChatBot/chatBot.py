import aiml
import os

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("./chatBot/covid-bot.aiml")
kernel.respond("load aiml files")




# Press CTRL-C to break this loop

#addTopic("stuff")

#createTopic("topicName", ["test1", "test2"], [])


#addString()
while True:
    inputed = input("Enter your message >> ")
    res = kernel.respond(inputed)
    if(len(res)>0):
        print(res)
    else:
        print('loopiloop')
