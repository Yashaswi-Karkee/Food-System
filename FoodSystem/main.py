import sqlite3
from os import system

connection = sqlite3.connect("FoodItems.db")
cursor = connection.cursor()

# query = '''CREATE TABLE Menu(Name varchar(30), Type varchar(30), Price float, Quantity int(2))'''
# query = '''CREATE TABLE Credentials(Username varchar(30), Password varchar(30), isAdmin BIT)'''
# query = '''INSERT INTO Credentials VALUES(?,?,?)'''
# values = [
#             ("user","password",0),
#             ("admin","password",1)
#         ]



# cursor.execute(query)
# cursor.executemany(query,values)

# connection.commit()


class Credentials:

    def __init__(self):
        
        self.user_uname = "user"
        self.user_pwd = "password"
        self.admin_uname = "admin"
        self.admin_pwd = "password"
        
        
    def changeUserCredentials(self,newUsername,newPassword):
        self.user_uname = newUsername
        self.user_pwd = newPassword
        
        #Inserting new credentials to database
        query = """INSERT INTO Credentials VALUES(?,?,?)"""
        valu = [(newUsername,newPassword,0)]
        cursor.executemany(query,valu)
        connection.commit()
        
        
    def changeAdminCredentials(self,newUsername,newPassword):
        self.admin_uname = newUsername
        self.admin_pwd = newPassword
        
        #Inserting new credentials to database
        query = """INSERT INTO Credentials VALUES(?,?,?)"""
        valu = [(newUsername,newPassword,1)]
        cursor.executemany(query,valu)
        connection.commit()
        
        
    def showUserCredentials(self):
        return self.user_uname,self.user_pwd
        
    def showAdminCredentials(self):
        return self.admin_uname,self.admin_pwd
        

credentials = Credentials()

        
#Customer Portal Functions
def customer_portal():
    
    #Displaying Default Credentials
    print("\n")
    print("*********Default Credentials************")
    print("Username: user")
    print("Password: password")
    print('\n')
    
    #Asking user for Credentials
    uname = input("Enter your username: ")
    pwd = input("Enter your password: ") 
    print("\n")
    
    #Checking Credentials

    if (uname == credentials.user_uname and pwd == credentials.user_pwd):
        return True   
      
    else:
        system('cls')
        print("Invalid Username or Password!")
        customer_portal()
        
    
def orderFood():
    query = '''SELECT * FROM Menu'''
    cursor.execute(query)
    items = cursor.fetchall()
    
    food_list = []
    item_list = []
    
    for item in items:
        food_list.append((item[1],item[0],item[2],item[3]))
        
    while True:
        i=0
        print("\n\t-------RESTAURANT MENU-------\n")
        print("\n\t Name\t\t\tPrice\t Available Quantity\n")
    
        for item in items:
            i = i + 1
            print(f"Press {i}: {item[1]} {item[0]}\t\t{item[2]}\t\t{item[3]}")
            
        #Exception Handling   
        try:
            choice = checkChoice(i,food_list)
            
        except Exception as e:
            system('cls')
            print(e)
            orderFood()
        
        try:        
            quantity = checkQuantity(choice)
            
        except Exception as er:
            system('cls')
            print(er)
            orderFood()
            
        item_list.append((choice[0],choice[1],choice[2],quantity))  #type,name,price,quan
        opt = input("Do you want to buy more?(Y/N): ")
        if opt == 'N' or opt == 'n':
            break
        
    #Printing Bill
    system('cls')
    print("\n\t\tName\t\t\tQuantity\t\tRate\t\tAmount\n")
    sum = 0
    for x in item_list:
        print(f"\t\t{x[0]} {x[1]}\t\t\t{x[3]}\t\t{x[2]}\t\t{x[2]*x[3]}")
        sum = sum + (x[2]*x[3])
        
    print("\nTotal Amount is: " + str(sum))
    a = input("Press enter key to continue...")
        
    
    

def checkChoice(i,food):
    print("\n")
    choice = int(input("Enter: "))
    if (choice<=0 and choice>i):
        raise Exception("Invalid Choice!")
    else:
        foods = food[choice-1]
        return foods
    
def checkQuantity(choi):
    print("\n")
    quan = int(input("Enter Quantity: "))
        
    if (quan>choi[3]):
        raise Exception("Out of Stock")
    elif quan<=0:
        raise Exception("Error! Entered number is negative.")
    else:
        querr = f'''UPDATE Menu SET Quantity = Quantity - ? WHERE (Name = ? and Type = ?)'''
        valu = (quan,choi[1],choi[0])
        cursor.execute(querr,valu)
        connection.commit()
        return quan
    
def customer_menu():
    print("\n")
    print("Press 1: To order food")
    print("Press 2: To change credentials")
    print("Press 3: Go back")
    print("\n")
    opt = int(input("Enter your choice: "))
    match opt:
        case 1:
            orderFood()
                       
        case 2:
            uname = input("Enter new username: ")
            passw = input("Enter new password: ")
            credentials.changeUserCredentials(uname,passw)
            print("\nSuccessfully Changed User Credentials!")

        case 3:
            system('cls')
            main()
            
        case default:
            print("\nError Encountered!Please choose number from the menu.")
            customer_menu()


#Admin Portal Functions
def admin_portal():
    
    #Displaying Default Credentials
    print("\n")
    print("*********Default Credentials************")
    print("Username: admin")
    print("Password: password")
    print('\n')
    
    #Asking user for Credentials
    uname = input("Enter your username: ")
    pwd = input("Enter your password: ") 
    print("\n")
    
    #Checking Credentials

    if (uname == credentials.admin_uname and pwd == credentials.admin_pwd):
        return True   
      
    else:
        print("Invalid Username or Password!")
        admin_portal()

def addItem():
    while True:
        print("\n")
        name = input("Enter item name: ")
        types = input("Enter food type: ")
        price = float(input("Enter the price: "))
        print("\n")
        quantity = int(input("Enter the quantity: "))
        val = [(name,types,price,quantity)]
        query = """INSERT INTO Menu VALUES(?,?,?,?)"""
        cursor.executemany(query,val)
        connection.commit()
        
        print("\n\nItem added successfully!\n")
        option = input("Do you want to add more items?(Y/N): ")
        if option == 'N' or option == 'n':
            break
        continue
        
def addQuantity():
    while True:
        print("\n")
        name = input("Enter item name: ")
        types = input("Enter food type: ")
        print("\n")
        quantity = int(input("Enter the quantity: "))
        query = f"""UPDATE Menu SET Quantity = Quantity + ? WHERE (Name = ? and Type = ?)"""
        valu = (quantity,name,types)
        cursor.execute(query,valu)
        connection.commit()
        
        print("\n\nQuantity added successfully!\n")
        option = input("Do you want to add more quantity?(Y/N): ")
        if option == 'N' or option == 'n':
            break
        continue
 
        
def removeItem():
    while True:
        print("\n")
        name = input("Enter item name: ")
        types = input("Enter food type: ")
        query = f"""DELETE from Menu WHERE (Name = ? and Type = ?)"""
        valu = (name,types)
        cursor.execute(query)
        connection.commit()
        
        print("\n\nItem removed successfully!\n")
        option = input("Do you want to delete more item?(Y/N): ")
        if option == 'N' or option == 'n':
            break
        continue
        
def admin_menu():
    print("\n")
    print("Press 1: Add Item in Menu")
    print("Press 2: Add quantity of item")
    print("Press 3: Remove item from menu")
    print("Press 4: Reset Credentials")
    print("Press 5: Go Back\n")
    opti = int(input("Enter choice: "))
    match opti:
        case 1:
            addItem()                    
        case 2:
            addQuantity()
        case 3:
            removeItem()
  
        case 4:
            uname = input("Enter new username: ")
            passw = input("Enter new password: ")
            credentials.changeAdminCredentials(uname,passw)
            print("\nSuccessfully Changed Admin Credentials!")

        case 5:
            system('cls')
            main()
        
        case default:
            system('cls')
            print("\nError Encountered!Please choose number from the menu.")
            admin_menu()
            


#Main Program
def main():
    #Assigning last known credentials
    query_user = """SELECT * FROM Credentials WHERE isAdmin = 0"""
    results_user = cursor.execute(query_user).fetchall()
    temp = []
    for result_user in results_user[-1]:
        temp.append(result_user)
        
    credentials.changeUserCredentials(temp[0],temp[1])
                
                
    query_admin = """SELECT * FROM Credentials WHERE isAdmin = 1"""
    results_admin = cursor.execute(query_admin).fetchall()
    temp = []
    for result_admin in results_admin[-1]:
        temp.append(result_admin)
                
    credentials.changeAdminCredentials(temp[0],temp[1])
    
    #Interactive Part
    while(1):
        print("\n")
        print("\n\n-------------Welcome-------------\n\n")
        print("Press 1: Login to Customer Portal")
        print("Press 2: Login to Admin Portal")
        print("Press 3: To Exit Program\n")
        choice = int(input("Enter your choice: "))
        print(choice)
        system('cls')
        match choice:
            case 1:
                if customer_portal()==True:
                    customer_menu()
                    system('cls')
                    continue  
                continue   
                                
            case 2:
                if admin_portal() == True:
                    admin_menu()
                    system('cls')
                    continue
                continue
            
            case 3:
                system('cls')
                print("\n\n\n\t\tThank you for using!\n\n\n")
                connection.close()
                exit(0)
            
            case default:
                system('cls')
                print("Error Encountered!Please choose number from the menu.")
                continue
            
if __name__ == "__main__":
    main()
    

    
    