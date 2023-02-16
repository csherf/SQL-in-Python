#Author: Chad Sherf
#Date: 2/15/23

# Keywords

CREATE = "CREATE"
DROP = "DROP"
USE = "USE"
ALTER = "ALTER"
SELECT = "SELECT"
EXIT = ".EXIT"

listKeywords = [CREATE, DROP, USE, ALTER, SELECT, EXIT]

def main():
    print("#------ Sql in Python Started -------#\n")
    while(1):
        # get the commands from the users input. A user can enter multiple commands seperated by ;
        #  example CREATE DATABASE db_1; CREATE DATABASE db_1;
        command = getInput()
        commands = command.split(";")

        for command in commands:
            parsedCommand = parseCommand(command)
            
            for word in parsedCommand:
                if word.upper() == EXIT:
                    return exit()
                elif testKeyword(word):
                    runCommand(parsedCommand)
                else:
                    print("invalid input\n")


# Get the users input from terminal 
def getInput():
    # type: () -> str
    userInput = input()
    return userInput

# parse the users input for key words and make sure its valid
def parseCommand(command):
    # type: (str) -> list[str]
    parsedCommand = command.split()
    return parsedCommand

# test if its a valid keyword
def testKeyword(keyword):
    # type: (str) -> bool
    keyword = keyword.upper()
    if listKeywords.count(keyword) != 0:
       return 1
    return 0

# run a given command 
def runCommand(command):
    # type: (list[str]) -> bool
    firstWord = command[0]
    if firstWord == CREATE:
        create(command)
    if firstWord == DROP:
        drop(command)
    if firstWord == USE:
        useDatabase(command)
    if firstWord == ALTER:
        alterTable(command)
    if firstWord == SELECT:
        select(command)
    return 0


# create a table or database
def create(command):
    return 0

# create a database (in this case a new folder)
def createDatabase():
    return 0 

# create a table (a file in a folder)
def createTable():
    return 0

# run the commands needed for dropping a table or database
def drop(command):
    return 0

# delete a database by deleting the folder asscoaited with it
def dropDatabase():
    return 0

# drop a table in a database (file in a folder)
def dropTable():
    return 0

#d efines which db/folder the user is working out of
def useDatabase(command):
    return 0

# edits a given table (file)
def alterTable():
    return 0

# select query 
def select(command):
    return 0

#quit out of the application
def exit():
    return 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClosing DB\n")
        