#Author: Chad Sherf
#Date: 2/15/23

#Imports
import os
import json
import shutil
### Keywords
CREATE = "CREATE"
DROP = "DROP"
USE = "USE"
ADD = "ADD"
ALTER = "ALTER"
SELECT = "SELECT"
EXIT = ".EXIT"
FROM = "FROM"
DATABASE = "DATABASE"
TABLE = "TABLE"

## List of Valid beginning Keywords
listKeywords = [CREATE, DROP, ALTER, SELECT, EXIT]

## List Valid Datatypes for tables
listDataTypes = [
    "int",
    "float",
    "varchar",
    "char",
]

## Dictionary with default values incase there already rows in a table
dictDefaultDataType = {
    "int": 0,
    "float": 0,
    "varchar": "",
    "char": ""
}


def main():
    print("#------ Sql in Python Started -------#")
    ##path of current database being used
    currentDatabase = "_none"
    while(1):
        # get the commands from the users input. A user can enter multiple commands seperated by ;
        #  example CREATE DATABASE db_1; CREATE DATABASE db_1;
        command = getInput()
        if command.upper() == EXIT:
            print("All done.")
            return 0
        if command[-1] != ';':
            print("!Close Command With ;")
        else:
            commands = command.split(";")
            for command in commands[:-1]:
                parsedCommand = parseCommand(command)
             
                # print("parsedCommand", parsedCommand)
                firstWord = parsedCommand[0]
                if firstWord.upper() == EXIT:
                    print("All done.")
                    return exit()
                elif firstWord.upper() == USE:
                    currentDatabase = useDB(parsedCommand)
                elif testKeyword(firstWord):
                    runCommand(parsedCommand, currentDatabase)
                        # print(f"!Error running command \"{command}\"")
                        
                else:
                    print("!invalid input\n")

# Get the users input from terminal 
def getInput():
    # type: () -> str
    userInput = input().strip()
    return userInput

# parse the users input for key words and make sure its valid
def parseCommand(command):
    # type: (str) -> list[str]
    parsedCommand = command.strip().split(' ')
    return parsedCommand

# test if its a valid keyword
def testKeyword(keyword):
    # type: (str) -> bool
    keyword = keyword.upper()
    if listKeywords.count(keyword) != 0:
       return 1
    return 0

# turn a list into a single string
def listToString(s):
    # type: (list[str]) -> str
    empty = " "
    # return string 
    return (empty.join(s))

# test if a str is a valid data type
def testDataType(strType):
    # type: (str) -> bool
    strType = strType.lower()
    if listDataTypes.count(strType) != 0:
       return 1
    return 0

# run a given command 
def runCommand(command, currentDatabase):
    # type: (list[str], str) -> bool
    firstWord = command[0].upper()
    if firstWord == CREATE:
        return create(command, currentDatabase)
    elif firstWord == DROP:
        return drop(command, currentDatabase)
    elif firstWord == ALTER:
        return alterTable(command, currentDatabase)
    elif firstWord == SELECT:
        return select(command, currentDatabase)
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


def constructHeaderJson(headerType, rowCount):
    # type: (str, int) -> dict
    dictHeader = {
        "type":headerType,
        "rows": []
    }

    # # Add blank rows for an existing table 
    # for i in range(rowCount):
    #    
    return dictHeader

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

    tableName = tableCommand[0]

    #Turns split up list of headers back into a string so it can be parsed correctly
    tableHeaders = listToString(tableCommand[1:])
    if not tableHeaders:
        print(f"!Invalid format for CREATE TABLE.")
        return 0
    
    # parse table headers and make sure its valid
    tableHeaders = parseTableHeaders(tableHeaders)
    if not tableHeaders:
        print("!Invalid table headers.")
        return 0
    
    # make sure that table doesnt already exist
    table_path = os.path.join(currentDatabase, tableName+".json")
    if os.path.exists(table_path):
        print(f"!Failed to create table {tableName} because it already exists.")
        return 0

    # Create Table in a json format
    tableDict = {
        "currentId": 1,
        "count": 0,
        "columns" : []
    }

    for keys in tableHeaders:
        tableDict["columns"].append(keys)
        tableDict[keys] = constructHeaderJson(tableHeaders[keys], 0)

    json_object = json.dumps(tableDict, indent=4)
    final_directory = os.path.join(currentDatabase, tableName + ".json")
    with open(final_directory, "w") as outfile:
        if outfile.write(json_object):
            print(f"Table {tableName} created.")
            return 1
    
    return 0

# parse the table headers into a dictionary 
# returns dictionary in format {header name : column type}
def parseTableHeaders(tableHeader):
    # type: (str) -> dict
    # print("table headers", tableHeader)
    if tableHeader[:-1] != ')' and tableHeader[0] != '(':
        return {}
    #parsing the header
    headers = tableHeader[1:-1]
    headers = headers.split(', ')
    
    headersDict = {}
    for header in headers:
        header = header.split(' ')
        if len(header) != 2:
            return 0
        headersDict[header[0]] = header[1]
    # print(headersDict)
    return headersDict

# run the commands needed for dropping a table or database
def drop(command, currentDatabase):
    # type: (list[str], str) -> bool
   if len(command) != 3:
        print("!Invalid Input for DROP.")
        return 0
   toDrop = command[1].upper() 
   if toDrop == DATABASE:
        return dropDatabase(command[2])
   elif toDrop == TABLE:
        return dropTable(command[2], currentDatabase)
   else:
        print("!Invalid Input for DROP.")

# delete a database by deleting the folder asscoaited with it
def dropDatabase(dbName):
    # type: (str) -> bool
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, dbName)
    if not os.path.exists(final_directory):
        print(f"!Failed to delete {dbName} because it does not exist.")
        return 0
    elif not shutil.rmtree(final_directory, ignore_errors=True):
        print(f"Database {dbName} deleted.")
    return 0

# drop a table in a database (file in a folder)
def dropTable(tableName, currentDatabase):
    # type: (str, str) -> bool
    if currentDatabase == "_none":
        print("!No Database In Use.")
        return 0
    table_path = os.path.join(currentDatabase, tableName + ".json")
    if not os.path.exists(table_path):
        print(f"!Failed to delete {tableName} because it does not exist.")
        return 0
    elif not os.remove(table_path):
        print(f"Table {tableName} deleted.")
        return 1
    return 0

# runs the alter command and parses to see what to do next 
def alterTable(command, currentDatabase):
    # type: (list[str], str) -> bool
    if currentDatabase == "_none":
        print("!No Database Selected")
        return 0
    
    if not len(command) == 6:
        print("!Invalid ALTER Command.")
        return 0
    
    if command[1].upper() != TABLE:
        print("!Invalid ALTER command.")
        return 0
    
    if command[3].upper() == ADD:
        return addToTable(command[2], command[4:], currentDatabase)
    
    return 0

#adds a new column to a table
def addToTable(tableName, headers, currentDatabase):
    # type: (str, list(str), str) -> bool
    table_path = os.path.join(currentDatabase, tableName + ".json")
    if not os.path.exists(table_path):
        print(f"!Failed to ADD to {tableName} because it does not exist.")
        return 0
    
    headerName = headers[0]
    headerType = headers[1]

    if not testDataType(headerType): 
        print(f"!Failed to ADD to {tableName} because {headerType} is not a valid type.")
        return 0
    
    with open(table_path, "r+") as jsonFile:
        data = json.load(jsonFile)
        # print(data)
        # See if header already exists
        if headerName in data:
            print(f"!Column header with name {headerName} already exists.")
            return 0
        
        # add header to the columns array and add an entry for it
        data["columns"].append(headerName)
        data[headerName] = constructHeaderJson(headerType, 0)
        
        jsonFile.seek(0)   
        if not json.dump(data, jsonFile, indent=4):
            jsonFile.truncate()
            print(f"Table {tableName} modified.")
            return 1
        return 0
    
# select query 
def select(command, currentDatabase):
    # type: (list[str], str) -> bool
    if currentDatabase == "_none":
        print("!No Database Selected.")
        return 0

    if not len(command) >= 4:
        print("!Invalid input for SELECT")
        return 0
    
    if command[1] == "*":
        selectAll(command[2:], currentDatabase)

    return 0

def selectAll(command, currentDatabase):
    # type: (list[str], str) -> bool
    if command[0].upper() != FROM:
        print("!Invalid use of Select.")

    tableName = command[1]
    table_path = os.path.join(currentDatabase, tableName+".json")

    if not os.path.exists(table_path):
        print(f"!Failed to query table {tableName} because it does not exist.")
        return 0
    
    with open(table_path, "r") as jsonFile:
        data = json.load(jsonFile)
        # print(data)
        # See if header already exists
        headersString = ""
        for columns in data["columns"]:
            if not headersString == "":
                headersString += " | "
            headersString += f"{columns} {data[columns]['type']}"
        print(headersString)
        return 1




#quit out of the application
def exit():
    return 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClosing DB\n")
        