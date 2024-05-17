# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"copies": 3, "cost": 2},
    "Super Mario Bros": {"copies": 5, "cost": 3},
    "Tetris": {"copies": 2, "cost": 1}
}

# Dictionary to store user accounts with their balances, points, and inventory
user_accounts = {}

# Admin credetials
admin_username = "admin"
admin_password = "adminpass"

# Space function to make the output cleaner
def space(lines=2):
    for i in range(lines):
        print()

# Function to display available games with their numbers and rental costs
def view_available_games():
    print("AVAILABLE GAMES MENU")
    for menu, (game, game_info) in enumerate(game_library.items(), start=1):
        print("*****************************************")
        print(f"{menu}. {game}\n")
        print(f"- Copies available: {game_info['copies']} copies")
        print(f"- Price: ${game_info['cost']}")
        print("*****************************************")
        space()

# Function to display the user's rented games
def view_inventory(username):
    print("This is your inventory:")
    user_inventory = user_accounts[username]["inventory"]
    for store, (game_name, owned) in enumerate(user_inventory.items(), start=1):
        print("*****************************************")
        print(f"{store}. {game_name}")
        print(f"{owned} owned")
        print("*****************************************")
        space()

# Function to register a new user
def register_user():
    username = input("Please enter your username: ")
    # Check if username is already stored in users dict
    if username == "": #if the user input is empty it will return to prompting the user for username
        print("Empty username.") # will let print out to let the user know their input is a blank
        return register_user()
    if username in user_accounts: #checks if the username already exists on the user_accounts lib
        print("Username already signed up.")
        return
        
    while True: #to let the user attempt again if ever their password is not valid
        password = input("Please enter your password: ")
        # Put a limit on the chars of the pass
        if len(password) < 5 or len(password) > 8:
            print("Please enter another password for your account.\n"
            "Your password should be 5-8 characters long.")
        else:
            break

    # Ask the user to top up their account balance
    while True:
        try:
            initial_balance = float(input("Please top up your account balance: $"))
            if initial_balance <= 0: #prevents the user from inputting negative value 
                print("Please enter a positive amount.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    # Initialize user account
    user_accounts[username] = {
        "password": password,
        "balance": initial_balance,
        "points": 0,
        "inventory": {game: 0 for game in game_library}  # Initialize inventory with 0 owned for each game
    }
    print("Sign up successful.")
    space()

# Function to rent a game
def rent_game(username):
    try:
        # initiate variables since they are not global variables
        user_account = user_accounts[username]
        user_wallet = user_account["balance"]
        user_points = user_account["points"]
        user_inventory = user_account["inventory"]
        
        view_available_games() #display available games first for the user to look at
        game_choice = input("Which game do you want to borrow? (Enter the game's number): ")
        if game_choice.strip() == "": # condition for the leave blank cancellation
            print("Transaction cancelled.")
            return
        game_choice = int(game_choice)
        
        if game_choice in range(1, len(game_library) + 1): #checks if the user's choice is within the available games
            game_name = list(game_library.keys())[game_choice - 1] #make a list of the games in game lib dict as game_name
            game_details = game_library[game_name] #initialize game_details 
            if game_details["copies"] > 0 and user_wallet >= game_details["cost"]: 
                #checks if there are stil copies and user's balance is enough to rent
                user_inventory[game_name] += 1 #adds game rented user inventory
                game_library[game_name]["copies"] -= 1 #decreases 1 copy from the game lib
                user_wallet -= game_details["cost"] #deducts price of game from user wallet
                # Update user's balance
                user_account["balance"] = user_wallet
                # Update reward points
                user_points += game_details["cost"] // 2
                user_account["points"] = user_points
                space()
                print(f"Successfully rented {game_name}.")
                print(f"Your remaining balance is {user_wallet}.")
                print(f"Your total reward points are {user_points}.")
            else:
                space()
                print("Game is out of stock or you have insufficient balance.")
        else:
            print("Invalid game number.")
    except ValueError as e:
        print(f"Error: {e}")

# Function to return a game
def return_game(username):
    user_account = user_accounts[username]
    user_wallet = user_account["balance"]
    user_inventory = user_account["inventory"]
    try:
        view_inventory(username)
        game_choice = input("Enter the number of the game you want to return (leave blank to cancel): ")
        if game_choice.strip() == "": #leave blank to cancel
            print("Transaction cancelled.")
            return
        game_choice = int(game_choice)
        if game_choice in range(1, len(user_inventory) + 1):
            game_name = list(user_inventory.keys())[game_choice - 1]
            if user_inventory[game_name] > 0: #game owned should be > 1 since the user is returning
                user_inventory[game_name] -= 1 #runs if the games owned is > 1
                game_library[game_name]["copies"] += 1 #retrieves game on the game library
                refund = game_library[game_name]["cost"] #initialize refund variable
                user_wallet += refund # refund will be added on the user wallet
                user_account["balance"] = user_wallet #account balance will have the same value as user_wallet
                print(f"{game_name} is successfully returned.")
                print(f"Your new balance is {user_wallet}.") 
            else:
                print("You don't have any copies of this game to return.") #runs if the games owned by the user is none
        else:
            print("Invalid game number.") 
    except ValueError as e:
        print(f"Error: {e}")

# Function to top-up user account
def top_up_account(username):
    #initial variables again
    user_wallet = user_accounts[username]["balance"]
    user_points = user_accounts[username]["points"]
    try:
        amount = input("How much would you like to add to your balance? (Leave blank to cancel): ")
        if amount.strip() == "": #for the transaction to be cancelled if the user leaves a blank as input
            print("Transaction cancelled.")
            return
        amount = float(amount) #initialize amount as float
        if amount > 0: #to limit the amount to be added as positive value only
            user_wallet += amount #adds amount to the user_wallet
            user_accounts[username]["balance"] = user_wallet #assigns the same value to the account balance
            print(f"Successfully deposited {amount}. New balance: {user_wallet}.")
            print(f"Your total reward points are {user_points}.")
        else:
            print("Invalid deposit amount.") #runs if the amount input is not more than 0
    except ValueError:
        print("Please enter a valid amount.") #error handling

# Function for admin to update game details
def admin_update_game():
    space()
    admin_menu()
    try:
        admin_choice = int(input("What would you like to do?: "))
        if admin_choice == 1:
            change_game_details()
        elif admin_choice == 2:
            print("Returning...")
            return 
        else:
            print("Invalid input.")
    except ValueError as e:
            print(f"Error: {e}")

# Function for the admin to change the game details only
def change_game_details():
    view_available_games()
    game_name = input("Which game do you want to modify: ")
    space()
    if game_name.strip() == "": #cancellation when left blank
        print("Action canceled.")
        space()
        return
    if game_name in game_library: #checks if the game to be changed is in the game lib
        copies = int(input("Enter the new number copies of the game: ")) #ask for the new num of copy
        cost = int(input("How much should it cost?: $")) #ask for the new price
        game_library[game_name]["copies"] = copies #pass new values
        game_library[game_name]["cost"] = cost
        print("Game library updated successfully.")
    else:
        print("Invalid game name.")
        return change_game_details()

# Function for admin login
def admin_login():
    print("Welcome to admin log in!")
    #prompt for the admin username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username == admin_username and password == admin_password: #checks if the credentials matches
        print("Admin log in successful.")
        return admin_update_game()
    else:
        print("Admin not recognized.") #prints out if credentials dont match and admin is not recognized
        return 

# Admin menu for when the admin logged in
def admin_menu():
    print("ADMIN MENU")
    print("****************************")
    print("||1. Change game details. ||")
    print("||2. Exit                 ||")
    print("****************************")
    return 

# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    #initialize variables needed in the function
    user_account = user_accounts[username]
    user_points = user_account["points"]
    user_inventory = user_account["inventory"]
    print(f"Your current reward points: {user_points}")
    try:
        if user_points >= 3: #checks if the points of the user is enough to redeem
            view_available_games()
            game_to_redeem = input("What game would you like to redeem? (Enter the game number)\n(Leave it blank to cancel.) ")
            if game_to_redeem.strip() == "": #if user leaves a blank
                print("Redemption cancelled.")
                return
            game_to_redeem = int(game_to_redeem) #initialize integer
            if game_to_redeem in range(1, len(game_library) + 1): #check whether the game to be redeemed is game lib
                game_name = list(game_library.keys())[game_to_redeem - 1]
                game_details = game_library[game_name]
                if game_details["copies"] > 0: #checks if the game to be redeemed has enough copies
                    user_inventory[game_name] += 1 #game redeemed will be added to user's inventory
                    game_library[game_name]["copies"] -= 1 #copies available will be decreased by 1
                    user_points -= 3  # Assuming each redemption costs 3 points
                    user_account["points"] = user_points #points on the user_account will be updated
                    print(f"Successfully redeemed {game_name}.")
                    print(f"Your remaining reward points: {user_points}")
                else:
                    print("Game is out of stock.") 
            else:
                print("Invalid game number.")
        else:
            print("Not enough points for a free rental.")
    except ValueError as e:
        print(f"Error: {e}")

# Function to display the main menu
def menu():
    print("==================")
    print("|1. Sign up      |")
    print("|2. Log in       |")
    print("|3. Admin Login  |")
    print("|4. Quit         |")
    print("==================")
    space()

# Log in function
def log_in():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    # Check if the account exists on the users dictionary
    if username in user_accounts and user_accounts[username]["password"] == password:
        print("Account logged in successfully.")
        space()
        logged_in_menu(username)
    else:
        print("Error. Invalid username and password.")

# Function to handle user's logged-in menu
def logged_in_menu(username):
    while True:
        print("====================================")
        print("|Choices:                          |")
        print("|1. Check game list                |")
        print("|2. Rent game                      |")
        print("|3. Check my games                 |")
        print("|4. Return game                    |")
        print("|5. Add account balance            |")
        print("|6. Check account balance          |")
        print("|7. Redeem points for free rental  |")
        print("|8. Return                         |")
        print("====================================")
        action = input("What would you like to do? ")
        space()

        if action == "1":
            view_available_games()
        elif action == "2":
            rent_game(username)
        elif action == "3":
            view_inventory(username)
        elif action == "4":
            return_game(username)
        elif action == "5":
            top_up_account(username)
        elif action == "6":
            show_balance(username)
        elif action == "7":
            redeem_free_rental(username)
        elif action == "8":
            return
        else:
            print("Please choose only from 1-8.")

# Function to show the user's balance
def show_balance(username):
    user_wallet = user_accounts[username]["balance"]
    print("**** User Wallet ****")
    print(f"Your wallet currently has ${user_wallet}.")

# Main function to run the program
def main():
    try:
        while True:
            menu()
            choice = int(input("Welcome to GAME RENTALS! What would you like to do? "))

            if choice == 1:
                register_user()
            elif choice == 2:
                log_in()
            elif choice == 3:
                admin_login()
            elif choice == 4:
                print("Okay, thank you for checking us out.")
                break
            else:
                print("Invalid choice, please choose only from 1-4.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
