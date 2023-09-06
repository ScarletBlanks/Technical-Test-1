import datetime

def truncate(dateTimeObj): #returns dateTime without seconds
    #Omit seconds and sort by datetime
    return dateTimeObj.replace(second = 0)

def startsWithDate(string):
    return len(string) > 9 and (string[0:4].isdigit() and string[4] == "-" and string[5:7].isdigit() and string[7] == "-" and string[8:10].isdigit())
    

def parseLine(line): #parses the line, returns DateTime Object, EventType String, Message String
    separated_data = line.split(" ") #split by spacebar
    date_str = separated_data[0]
    time_str = separated_data[1]
    event_str = separated_data[2]
    message_str = ""
    
    for message in separated_data[3::]: #combine the separated message
        message_str += (message + " ")
    message_str = message_str[:-1] #remove last unneeded " "

    dateTime_str = date_str + " " + time_str #separate date, time by space so it's easier to parse
    dateTimeObj = truncate(datetime.datetime.strptime(dateTime_str, '%Y-%m-%d %H:%M:%S'))
    
    return dateTimeObj, event_str, message_str

def query(event_type_str):
    print(event_type_str, ":")
    for events in processed_events:
        if events[1] == event_type_str:
            print(events[0], events[2])

def queryForAssert(event_type_str):
    str = event_type_str + " :\n"
    for events in processed_events:
        if events[1] == event_type_str:
            str += events[0].strftime('%Y-%m-%d %H:%M:%S') + " " + events[2] + "\n"
    return str[:-1]

file = open("log.txt", "r") # limit permissions to read to protect data

def processFile(file):
    post_processed = []
    complete_instruction = ""
    isFirstLine = True
    lineNumber = 0

    while True:
        line = file.readline()
        if not line:
            complete_instruction = complete_instruction[:-1] #remove last unneeded " "
            post_processed.append(parseLine(complete_instruction))
            complete_instruction = cleaned_line + " "
            break
        cleaned_line = line.strip()#strip() cleans up lines that shows up as empty
        if (startsWithDate(cleaned_line) and not isFirstLine):
            complete_instruction = complete_instruction[:-1] #remove last unneeded " "
            post_processed.append(parseLine(complete_instruction))
            complete_instruction = cleaned_line + " "
        else:
            complete_instruction += cleaned_line + " "
            isFirstLine = False
    return post_processed
    
processed_events = sorted(processFile(file), key=lambda entry: entry[0])

#QUERIES
query("INFO")
query("ERROR")

#TEST_CASES
assert queryForAssert("ERROR") == "ERROR :\n2023-08-10 08:35:00 An error occurred: File not found"
assert queryForAssert("INFO") == "INFO :\n2023-08-10 08:30:00 This is a log message\n2023-08-10 08:40:00 Another message"


    
    
