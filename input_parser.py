import sys
import gen_graph
import re

def parse_input(st_db):
    
    #user_input = sys.stdin.readline().strip()
    user_input = input().strip()

    # check if correct option given
    option_regex = re.compile(r'^\s*[arc]\s+|^\s*[g]\s*$')
    while not re.match(option_regex,user_input): 
        print("Error: incorrect command given. Please choose 'a', 'c' 'r' or 'g' as a command.")
        user_input = input()

    # if option matches extract option
    user_option = ((re.findall(option_regex,user_input))[0]).strip()
    
    assert(user_option == 'a' or user_option == 'r' or user_option == 'c' or user_option == 'g')

    # parse input for each specific option
    if (user_option == 'a'):
        command = parse_a(user_input)
        st_db.add(command)

    if (user_option == 'c'):
        command = parse_c(user_input)
        st_db.change(command)

    if (user_option == 'r'):
        command = parse_r(user_input)
        st_db.remove(command)

    if (user_option == 'g'):
        command = parse_g(user_input)
        st_db.graph()

#  parse_a - check if the input for a is correct 
def parse_a(user_input):

    #print("Came here")
    a_regex = re.compile(r'^\s*[a]\s+["][a-zA-Z\s]+["]\s+([(]\s*-?[\d]+\s*[,]\s*-?[\d]+\s*[)]\s*){2,}\s*$')

    while not re.match(a_regex,user_input):
        print("Error: You have not formatted your command correct. Please try again with the following format: a \"<STREET NAME>\" (X1,Y1) (X2,Y2)..(Xn,Yn)")
        
        user_input = input()

    #Split the command into command, street_name and coordinates
    # strip any extra white spaces
    command = user_input.split("\"")
    command[0] = command[0].strip()
    command[2] = command[2].strip()
    # for i in range(len(command)):
    #   command[i] = command[i].strip()
    
    #print (command)

    return command

#  parse_c - check if the input for c is correct 
def parse_c(user_input):

    c_regex = re.compile(r'^\s*[c]\s+["][a-zA-Z\s]+["]\s+([(]\s*-?[\d]+\s*[,]\s*-?[\d]+\s*[)]\s*){2,}\s*$')

    while not re.match(c_regex,user_input):
        print("Error: You have not formatted your command correct. Please try again with the following format: c \"<STREET NAME>\" (X1,Y1) (X2,Y2)..(Xn,Yn)")
        
        user_input = input()

    #Split the command
    command = user_input.split("\"")
    command[0] = command[0].strip()
    command[2] = command[2].strip()
    # for i in range(len(command)):
    #   command[i] = command[i].strip()
    
    #print (command)

    return command

#  parse_r - check if the input for r is correct 
def parse_r(user_input):

    r_regex = re.compile(r'^\s*[r]\s+["][a-zA-Z\s]+["]\s*$')
    
    while not re.match(r_regex,user_input):
        print("Error: You have not formatted your command correctly. Please try again with the following format: r \"<STREET NAME>\"")
        
        user_input = input()

    
    command = user_input.split("\"")
    command = [command[0].strip(),command[1]]
    # for i in range(len(command)):
    #   command[i] = command[i].strip()
    
    #print (command)

    return command

#  parse_g - check if the input for g is correct 
def parse_g(user_input):

    g_regex = re.compile(r'^\s*[g]\s*$')

    while not re.match(g_regex,user_input):
        print("Error: You have not formatted your command correctly. Please enter only 'g' to generate the graph")
        
        user_input = input()

    # Remove all white spaces
    command = user_input.strip()

    return command

def main():

    st_db = gen_graph.Street_Database()

    try:
        while (True):
            parse_input(st_db)
    except EOFError:
        return

    
if __name__ == '__main__':
    main()
