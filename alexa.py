def main():
    process_file()

def add_name(name, title, content, frequency, line, file): #read name, title
#if an user wants to keep reading, read content
#if 'read', add frequency
#***frequency cannot be sorted based on the 'name'*** --> if same name appears\
#more than once, frequency should be more than 1. <-- which is not achieved
#readed_name_list has both frequency and name
#frequency<10 is considered as "not important" and frequency>100 is considered\
#as "very important"
    name_txt = [""]    
    print("frequency begining", frequency)    
    readed_name_list = []
    non_deleted = []
    frequency_copy = []
    for k in range(0, len(frequency)):
        frequency_copy.append(frequency[k])
    print(frequency_copy)
    for i in range(0, len(name)):
        print(name[i],"sent you an email titled with", title[i])
        command = input("Do you want to read the email?")
        if "yes" in command.lower():
            #name_txt.append(name[i])
            frequency[i] += 1
            print("The mail says", content[i])
            for j in range(0, len(name_txt)):
                if name[i] == name_txt[j]:
                    frequency[i] += 1 
                else:
                    name_txt.append(name[i])
        if frequency[i] < 10:
            frequency_copy[i] = 100
        elif frequency[i] > 99:
            frequency_copy[i] = 0
        elif frequency[i]>10 and frequency[i]<100:
            frequency_copy[i] = frequency[i]
        readed_name_list.append(str(frequency_copy[i])+ " "+ name[i])
        #update(readed_name_list, name)
        if "delete" in command:
            name[i], title[i], content[i] = None, None, None
        else:
            non_deleted.append(name[i] + title[i] + content[i])
        print("f", frequency)
        print("f_copy", frequency_copy)

def update(readed_name_list, name):#   
    readed = []
    for i in range(0, len(name)):
        for j in range(0, len(readed_name_list)):
                if name[i] in readed_name_list[j]:
                    readed.append(readed_name_list[j])
                    return readed 
                
def compare(readed):#readed is sorted upsidedown --> decending form
    sorted(readed)
    for i in reversed(readed):
        print("reversed", readed[i])
    
def open_file():
    file_name = input("Enter a file name: ")
    while True:
        try:
            fp = open(file_name, "r")
            fp.readline()
            return fp
        except FileNotFoundError:
            print("File not found. Try again.")
            break
            #file_name = input("Enter a file name: ")
        
def process_file():
    file = open_file()
    name, title, content, frequency = [], [], [], []
    for line in file:
        space = line.find(" ")
        space_backward = line.rfind(" ")
        name_app = line[:space].strip()
        title_app = line[space:space_backward].strip()
        content_app = line[space_backward:].strip()
        name.append(name_app)
        title.append(title_app)
        content.append(content_app)
        frequency.append(0)
    add_name(name, title, content, frequency, line, file)

main()