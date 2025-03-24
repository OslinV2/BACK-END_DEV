# Welcome to my application!
print("~~ Welcome to your checkbook! ~~\n")

# How the user will be prompted
prompt = '> Your option: '

# menu options the user can pick from to proceed
def menu():
    print("How would you like to proceed?")
    print("""
    1) View current balance333
    2) Make a withdrawl 
    3) Make a deposit  
    4) Exit\n""")

# opens and reads the checkbook text file balance and converts it into a float
def read_balance():
    f = open("checkbook.txt", "r")
    bal = float(f.read())
    return bal

# opens and writes to the checkbook text file
def write_balance(new_balance):
    f = open("checkbook.txt", "w")
    f.write(str(new_balance))

# this function takes the read_balance function as current_balance and adds the deposit amount to it to create a new balance, then calls the write_balance(new_balance) function to display the new amount
def make_deposit(deposit_amount):
    current_amount = read_balance()
    new_balance = int(current_amount) + int(deposit_amount)
    write_balance(new_balance)

# this function takes the current_amount, (the read_balance()), and subtracts the withdraw_amount from it to to create a new balance, then calls the write_balance(new_balance) function to display the new amount
def make_withdraw(withdraw_amount):
    current_amount = read_balance()
    new_balance = int(current_amount) - int(withdraw_amount)
    write_balance(new_balance)

# this function calls the menu() function to prompt the user on how they wish to proceed. 
def main():
    menu()
    option = input(prompt)
    print("\n")

# if the user picks opt 1., it will display their current balance by calling the read_balance() function, then calls the main() function to continue. It will also format the float to 2 decimal points and add a '$' to the amouunt.
    if option == "1":
        print("Your current balance is ${:.2f}" .format(read_balance()))  
        print("\n")
        input("Press 'ENTER' to continue.\n")
        main()  

# if the user picks opt 2., it prompts user to enter withdraw amount, then calls the make_withdraw(withdraw_amount) function to perform the operation and prints the read_balance() to show new amount.
    elif option == "2":
        withdraw_amount = input("How much do you wish to withdraw?\n")
        make_withdraw(withdraw_amount)

# If the read_balance > 0, then it will call the make_withdraw(withdraw_amount) function and it will format the float to 2 decimal points and add a '$' to the amouunt.     
        if float(read_balance()) > 0: 
            print("Your new balance is ${:.2f}" .format(read_balance()))
            print("\n")
            input("Press 'ENTER' to continue.\n")

# If the read_balance < 0, then it will print 'insufficient' message and show new balance with float formatting.
        else: 
            print("Insufficient funds. Your account is negative. \n")
            print("Your new balance is ${:.2f}\n" .format(read_balance()))
        main()

# if user picks opt 3., user is prompted to enter deposit amount then the make_deposit(deposit_amount) is called, then read_balance() function displays new balance after deposit
    elif option == "3":
        deposit_amount = input("How much to do you wish to deposit?\n")
        make_deposit(deposit_amount)
        print("Your new balance is ${:.2f}" .format(read_balance()))
        print("\n")
        input("Press 'ENTER' to continue.\n")
        main()

# if user picks opt 4., prints exit string and exits the application
    elif option == "4":
        print("Thank you, have a great day!\n")

# if user picks option not listed, prints sorry statement the calls main() function to bring back to main menu and pick again.
    else:
        print("Sorry, that is an invalid option.\n")
        main()

main()

