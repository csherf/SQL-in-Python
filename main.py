#Author: Chad Sherf
#Date: 2/15/23

#Imports
import os
import json

# Keywords
CREATE = "CREATE"
DROP = "DROP"
USE = "USE"
ALTER = "ALTER"
SELECT = "SELECT"
EXIT = ".EXIT"
FROM = "FROM"
DATABASE = "DATABASE"
TABLE = "TABLE"

listKeywords = [CREATE, DROP, USE, ALTER, SELECT, EXIT]

def main():
    print("#------ Sql in Python Started -------#\n")
    ##path of current database being used
    currentDatabase = "_none"
    while(1):
        # get the commands from the users input. A user can enter multiple commands seperated by ;
        #  example CREATE DATABASE db_1; CREATE DATABASE db_1;
        command = getInput()
        if command[-1] != ';':
            print("!Close Command With ;")
        else:
            commands = command.split(";")
            for command in commands[:-1]:
                parsedCommand = parseCommand(command)
                print("parsedCommand", parsedCommand)
                firstWord = parsedCommand[0]
                if firstWord.upper() == EXIT:
                    return exit()
                elif firstWord.upper() == USE:
                    currentDatabase = useDB(parsedCommand)
                elif testKeyword(firstWord):
                    runCommand(parsedCommand, currentDatabase)
                else:
                    print("!invalid input\n")


# Get the users input from terminal 
def getInput():
    # type: () -> str
    userInput = input()
    return userInput

# parse the users input for key words and make sure its valid
def parseCommand(command):
    # type: (str) -> list[str]
    parsedCommand = command.split(' ')
    return parsedCommand

# test if its a valid keyword
def testKeyword(keyword):
    # type: (str) -> bool
    keyword = keyword.upper()
    if listKeywords.count(keyword) != 0:
       return 1
    return 0

# run a given command 
def runCommand(command, currentDatabase):
    # type: (list[str], str) -> bool
    firstWord = command[0].upper()
    if firstWord == CREATE:
        return create(command, currentDatabase)
    elif firstWord == DROP:
        return drop(command)
    elif firstWord == ALTER:
        return alterTable(command)
    elif firstWord == SELECT:
        return select(command)
    else:
        return 0

# look up if db exists and set it as current database
def useDB(command):
    # type: (list[str]) -> str
    if len(command) != 2:
        print("!Invalid input for USE")
        return "_none"
    
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, command[1])

    if os.path.exists(final_directory):
        print(f"Using database {command[1]}.")
        return final_directory
    else:
        print("!Database does not exist")
        return "_none"

# create a table or database
def create(command, currentDatabase):
    # type: (list[str], str) -> bool
    if not len(command) > 2:
        return 0
    if command[1].upper() == DATABASE:
        createDatabase(command[2])
        return 1
    elif command[1].upper() == TABLE:
        createTable(command[2:], currentDatabase)
        return 1
    else:
        return 0

# create a database (in this case a new folder)
def createDatabase(name):
    # type: (str) -> bool
    if name == "":
        print("!Please enter a name for the database.")
        return 0 
    
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, name)
    if os.path.exists(final_directory):
        print(f"!Failed to create database {name} because it already exists.")
        return 0
    try: 
        if not os.mkdir(final_directory):
            print(f"Database {name} created.")
    except OSError as error: 
        print(error)  
   
# create a table (a file in a folder)
def createTable(tableCommand, currentDatabase):
    # type: (list[str], str) -> bool
    if currentDatabase == "_none":
        print("!No Database Selected.")
        return 0

    print("creating table ", tableCommand)
    tableName = tableCommand[0]
    tableHeaders = listToString(tableCommand[1:])
    tableHeaders = parseTableHeaders(tableHeaders)
    print(tableHeaders)
    
    tableDict = {
        "currentId": 3,
        "count": 2,
    }

    for keys in tableHeaders:
        tableDict[keys] = {
            "type":tableHeaders[keys],
            "rows": []
        }
    print(tableDict)

    json_object = json.dumps(tableDict, indent=4)
    final_directory = os.path.join(currentDatabase, tableName + ".json")
    with open(final_directory, "w") as outfile:
        if outfile.write(json_object):
            return 1
    
    return 0

# parse the table headers into a dictionary 
# returns dictionary in format {header name : column type}
def parseTableHeaders(tableHeader):
    # type: (str) -> dict
    if tableHeader[:-1] != '0' and tableHeader[0] != '(':
        print("!Invalid table header format")
        return []
    #parsing the header
    headers = tableHeader[1:-1]
    headers = headers.split(', ')
    print(headers)

    headersDict = {}
    for header in headers:
        header = header.split(' ')

        headersDict[header[0]] = header[1]
    print(headersDict)
    return headersDict

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

def listToString(s):
    # type: (list[str]) -> str
    empty = " "
    # return string 
    return (empty.join(s))

#quit out of the application
def exit():
    return 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClosing DB\n")
        