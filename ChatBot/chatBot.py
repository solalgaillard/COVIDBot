import aiml
import os

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("./chatBot/covid-bot.aiml")
kernel.respond("load aiml b")

def addString():
    stringtoAdd = "<category><pattern>WHAT ARE YOU</pattern><template>I'm a bot, silly!</template></category>"
    with open('./chatBot/basic-chat2.aiml', "r+", encoding = "utf-8") as file:

        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
        file.write(stringtoAdd)
        file.write('\n< / aiml >')


def insertValue(value):
    with open('./chatBot/basic-chat2.aiml', 'r+') as fd:
        contents = fd.readlines()
        contents.insert(index, new_string)  # new_string should end in a newline
        fd.seek(0)  # readlines consumes the iterator, so we need to start over
        fd.writelines(contents)  # No need to truncate as we are increasing filesize

def delValue(value):
    with open('./chatBot/basic-chat2.aiml', 'r+') as fd:
        contents = fd.readlines()
        contents.insert(index, new_string)  # new_string should end in a newline
        fd.seek(0)  # readlines consumes the iterator, so we need to start over
        fd.writelines(contents)  # No need to truncate as we are increasing filesize

# Press CTRL-C to break this loop

addString()
while True:
    inputed = input("Enter your message >> ")
    res = kernel.respond(inputed)
    if(len(res)>0):
        print(res)
    else:
        print('loopiloop')