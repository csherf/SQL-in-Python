#Author: Chad Sherf
#Date: 2/15/23

# Keywords
CREATE = "CREATE"
DROP = "DROP"
USE = "USE"
ALTER = "ALTER"
SELECT = "SELECT"
EXIT = ".EXIT"

def main():
    while(1):
        input = getInput()
        parsedInput = parseInput()
        for word in parsedInput:
            if parsedInput[0].upper() == EXIT:
                return exit()
            elif testKeyword():
                runCommand()
            else:
                invalidInput()


# Get the users input from terminal 
def getInput():
    # type: () -> str
    return "1"

# parse the users input for key words and make sure its valid
def parseInput(input):
    # type: (str) -> list[str]
    return [""]

# test if its a valid keyword
def testKeyword(keyword):
     # type: (str) -> bool
    return 0

# run a given command 
def runCommand(command):
    # type: (str) -> bool
    return 0

def invalidInput():
    return 0

# create a database (in this case a new folder)
def createDatabase():
    return 0 

# create a table (a file in a folder)
def createTable():
    return 0

# delete a database by deleting the folder asscoaited with it
def dropDatabase():
    return 0

# drop a table in a database (file in a folder)
def dropTable():
    return 0

#defines which db/folder the user is working out of
def useDatabase():
    return 0

#edits a given table (file)
def alterTable():
    return 0

def select():
    return 0

#quit out of the application
def exit():
    return 0

if __name__ == "__main__":
    main()