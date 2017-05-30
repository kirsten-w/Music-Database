import os   # Needed for deleting and renaming files


# Functions for adding and stripping the file extension
def strip_file_extension(file_name):
    if file_name[-4:] == ".txt":
        stripped_file_name = file_name[:-4]
    return stripped_file_name
def append_file_extension(file_name):
    if file_name[-4:] != ".txt":
        new_file_name = file_name + ".txt"
    return new_file_name

# This function takes a username as an argument and opens the corresponding file in read mode. 
def verify_username(username):
    try:
        username = append_file_extension(username)        
        username_file = open(username, "r")
        username_file.close()
        return True
    except FileNotFoundError:
        return False
        
def add_account():
    new_account_name = input("Enter your desired username: ")
    new_account_name_extended = append_file_extension(new_account_name)
    new_account_file = open(new_account_name_extended, "w")
    new_account_file.close()
    print("Your username has been created.", "\n")
    login(new_account_name)
    
# Function calls the appropriate menu choice function username as an argument. 
def login(username):
    user = append_file_extension(username)
    valid_username = verify_username(username)
    if valid_username:    
        print("Main Menu")
        print("Current Account:", strip_file_extension(user))
        print("Enter 'L' at any prompt to log out.")
        function_prompt = (input("Do you want to (1) display all albums, (2) search for an album, (3) add an album, or (4) delete an album? "))
        if function_prompt.isdigit():
            function_prompt = int(function_prompt)
        if function_prompt == 1:
            display_all(user)
        elif function_prompt == 2:
            search(user)
        elif function_prompt ==3:
            add(user)
        elif function_prompt ==4:
            delete(user)
        elif function_prompt =="Q":
            quit()
        elif function_prompt == "L":
            logout()
        else:
            print("Not valid input")
            username = strip_file_extension(user)
            login(username)
        return user 
    else: 
        print("This account does not exist.")
        menu_prompt = (input("Would you like to (1) create an account or (2) try another login? "))
        if menu_prompt.isdigit():
            menu_prompt = int(menu_prompt)
        if menu_prompt == 1: 
            add_account()
        elif menu_prompt == 2:
            username = strip_file_extension(user)
            login(username)
        elif menu_prompt =="Q":
            quit()
        elif menu_prompt == "L":
            logout()


# Menu options called from the login with the username as an argument
# Use the argument to open the user's file and strip file extension
            
def display_all(user):  
    current_file = open(user, "r")
    file_string = current_file.read()
    current_file.close()
    if file_string == "":
        print("Sorry, there is no information associated with this account.")
        username = strip_file_extension(user)
        login(username)
    else:
        print("\n", file_string)
        username = strip_file_extension(user) 
        login(username)
    
def add(user):   
    current_file = open(user, "r")
    temp_file_original = open("temp.txt", "w") # Temp containing original music file contents
    temp_file_changed = open("temp2.txt", "w") # Temp containing the file with additions
    
    album_name = input("Enter the album name: ")
    artist = input("Enter the artist: ")
    genre = input("Enter the genre: ")
    runtime = input("Enter the runtime in format h:mm:ss ") 
    current_file_string = current_file.read() 
    
    temp_file_original.write(current_file_string)
    temp_file_changed.write(current_file_string)
    
    temp_file_changed.write(album_name + "\n")
    temp_file_changed.write(artist + "\n")
    temp_file_changed.write(genre + "\n")
    temp_file_changed.write(runtime + "\n")    
    
    current_file.close()
    temp_file_original.close()
    temp_file_changed.close()
    
    save_input = int(input("Enter 1 to save or 2 to discard changes "))
    
    # To save, user's file deleted and replaced with temp file containing any additions.
    if save_input ==1:
        os.remove(user)
        os.rename("temp2.txt", user)
    elif save_input ==2:
        os.remove(user)
        os.rename("temp.txt", user)
        
    add_menu_option = (input("Would you like to (1) add another entry, (2) return to the menu? "))
    if add_menu_option.isdigit():
        add_menu_option = int(add_menu_option)
    if add_menu_option == 1:
        add(user)
    elif add_menu_option == 2:
        username = strip_file_extension(user)
        login(username)
    elif add_menu_option =="Q":
        quit()
    
def delete(user):
    current_file = open(user, "r")
    temp_file = open("temp.txt", "w")
    
    found = False
    search_name = input("Enter the name of the album to delete: ")
    album_name = current_file.readline()
    while album_name != "":
        artist = current_file.readline()
        genre = current_file.readline()
        runtime = current_file.readline()
        album_name = album_name.rstrip("\n")
        if album_name != search_name:
            album_name = album_name + "\n"
            temp_file.write(album_name)
            temp_file.write(artist)
            temp_file.write(genre)
            temp_file.write(runtime)
            found = True
        album_name = current_file.readline()
    temp_file.close()
    current_file.close()
    if not found:
        print("The album was not found.")
        username = strip_file_extension(user)
        login(username) 
    save_input = input("Do you want to (1) save these changes or (2) discard them? ")
    if save_input.isdigit():
        save_input = int(save_input)
    if save_input == 1:
        print("Changes saved.")
        os.remove(user)
        os.rename("temp.txt", user)
        username = strip_file_extension(user)
        login(username)
    
    elif save_input ==2: 
        print("Changes discarded.")
        os.remove("temp.txt")
        username = strip_file_extension(user)
        login(username)

    
     
def search(user): 
    found = False
    search_name = input("Enter the name of the album: ")
    current_file = open(user, "r")
    album_name = current_file.readline()
    while album_name != "":
        artist = current_file.readline()
        genre = current_file.readline()
        runtime = current_file.readline()
        album_name = album_name.rstrip("\n")
        if album_name == search_name:
            print(album_name)
            print(artist.rstrip("\n"))
            print(genre.rstrip("\n"))
            print(runtime.rstrip("\n"))
            found = True
        album_name = current_file.readline()
    current_file.close()
    if not found:
        print("The album was not found.")
        username = strip_file_extension(user)
        login(username)    
    search_prompt = input("(1) Return to menu or (2) search again? ")
    if search_prompt.isdigit():
        search_prompt = int(search_prompt)
    if search_prompt ==1:
        username = strip_file_extension(user)
        login(username)
    elif search_prompt ==2:
        search(user)
    elif search_prompt =="Q":
        quit()
    elif search_prompt =="L":
        logout()
     
    
def main_menu():
    print("Enter 'Q' to quit at any prompt.")
    login_prompt = (input("Would you like to (1) log in or (2) add an account? "))
    if login_prompt.isdigit():
        login_prompt = int(login_prompt)
    if login_prompt ==1:
        username = input("Enter your username: ")
        login(username)
    elif login_prompt ==2:
        add_account()
    elif login_prompt == "Q":
        quit()
    elif login_prompt == "L":
        logout()
    else:
        print("Not valid input")
        main_menu()

def logout():
    print("You have been signed out.")
    main_menu()

def quit():
    print("Have a nice day.")

main_menu()
