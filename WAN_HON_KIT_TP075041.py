#Wan Hon Kit
#TP075041
import datetime
def load_users():
    users=[]
    try:
        with open("UserDB.txt", "xt") as UserDB:
            UserDB.write('Username, Password, Role, Approval, Usage\n')
            UserDB.write('Klccc,987,super_user,True,0\n')
    except FileExistsError:
        pass
    finally:
        with open("UserDB.txt", "r") as UserDB:
            next(UserDB)
            for line in UserDB:
                username, password, role, approved, usage = line.strip().split(',')
                users.append([username, password, role, approved, int(usage)])
    return users

def save_users(users):
    with open("UserDB.txt", "w") as UserDB:
        UserDB.write('Username,Password,Role,Approval,Usage\n')
        for user in users:
            username, password, role, approved, usage = user
            UserDB.write(f"{username},{password},{role},{approved},{usage}\n")

def register():
    print('\nRegister')
    while True:
        username = input('Username (Press Enter to go back): ').strip().capitalize()
        if username == '':
            print("\nGoing back to the previous menu.")
            return None
        #Below check if username already taken
        users = load_users()
        username_taken = False
        for user in users:
            if user[0] == username:
                print('Username is taken!')
                username_taken = True
                break
        if username_taken:
            continue
        #user enter password if no error
        password = input('Enter Password: ').strip()
        if password == '':
            print("Password cannot be empty. Please try again.")
            continue
        while True:
            role = input("Enter role (customer/admin): ").strip()
            if role in ['customer', 'admin']:
                break
            else:
                print("Invalid role. Please try again.")
        user=[username, password, role, 'False', 0]
        users.append(user)
        save_users(users)
        print('User registered successfully,waiting for approval!')
        newuser = user
        return (newuser)

def login():
    users = load_users()
    username = str(input('\nUsername: ')).capitalize()
    password = str(input('Enter Password: '))
    for user in users:
        if user[0] == username and user[1] == password:
            if user[3]=="True":
                print(f"Welcome, {username}!")
                return user
            elif user[3]=="Disabled":
                print("User access is disabled.")
                return None
            else:
                print("User not approved yet.")
                return None
    print("Invalid username or password.")
    return None


#CUSTOMER
def load_customerdetails():
    customers=[]
    try:
        with open("CustomerDetails.txt", "xt") as CustomerDetails:
            CustomerDetails.write('username, IC/passport number, name, phone, city of domicile, date of registration\n')
    except FileExistsError:
        pass
    finally:
        with open("CustomerDetails.txt", "r") as CustomerDetails:
            next(CustomerDetails)
            for line in CustomerDetails:
                username, ICpassport, name, phone, city_of_domicile, date_of_registration = line.strip().split(',')
                customers.append((username, ICpassport, name, phone, city_of_domicile, date_of_registration))
    return customers

def checkcustomerfilleddetails(user):
    customers=load_customerdetails()
    print(user[0])
    for customer in customers:
        if customer[0]==user[0]:
            return
    print('Customer has not filled in details')
    ICpassport= str(input('Enter IC/Passport Number: '))
    name = str(input('Enter Name as per IC/Passport: '))
    phone = str(input('Enter Phone Number: '))
    city_of_domicile = str(input('Enter City Of Domicile: '))
    current_date = datetime.date.today()
    date_of_registration = current_date.strftime("%Y-%m-%d")
    customer = [user[0],ICpassport, name, phone, city_of_domicile, date_of_registration]
    customers.append(customer)
    save_customer(customers)
    print('Registered Successfully!')
    return

def save_customer(customers):
    with open("CustomerDetails.txt", "w") as CustomerDetails:
        CustomerDetails.write('username, IC/passport number, name, phone, city of domicile, date of registration\n')
        for customer in customers:
            username, ICpassport, name, phone, city_of_domicile, date_of_registration = customer
            CustomerDetails.write(f"{username},{ICpassport},{name},{phone},{city_of_domicile},{date_of_registration}\n")


def customermanagementmenu(user):
    while True:
        print("\nCustomer Management System")
        print("1. Place Order")
        print("2. Make Payment")
        print("3. Inquire Order Status")
        print("4. Modify Order")
        print("5. Cancel Order")
        print("6. View Reports")
        print("7. Log Out")

        choice = input("Enter your choice: ")
        if choice == "1":
            print("Customer order menu...")
            neworder=cus_placeorder(user)
            if neworder == None:
                continue
            cus_addorder_log(user,neworder)
        elif choice == "2":
            print("Payment Screen")
            cus_payment(user)
        elif choice == "3":
            print("Inquire Order Screen")
            cus_inquireorder(user)
        elif choice == "4":
            print("Modify Order Menu")
            modifyorder = cus_modifyorder(user)
            if modifyorder == None:
                continue
            cus_modifyorder_log(user,modifyorder)
        elif choice == "5":
            print("Modify Order Menu")
            cancelorder=cus_cancelorder(user)
            if cancelorder == None:
                continue
            cus_cancelorder_log(user,cancelorder)
        elif choice == "6":
            cus_report(user)
        elif choice == "7":
            print("Log Out Successfully")
            logout_log(user)
            break
        else:
            print("Invalid choice. Please try again.")

def load_carts():
    carts=[]
    try:
        with open("CartDB.txt", "x") as CartDB:
            CartDB.write('Username, StockName, Quantity, Price, Category, Status\n')
    except FileExistsError:
        pass
    finally:
        with open("CartDB.txt", "r") as CartDB:
            next(CartDB)
            for line in CartDB:
                Username, StockName, Quantity, Price, Category, Status = line.strip().split(',')
                carts.append([Username, StockName, int(Quantity), float(Price), Category, Status])
    return carts

def save_carts(carts):
    with open("CartDB.txt", "w") as CartDB:
        CartDB.write('Username, StockName, Quantity, Price, Category, Status\n')
        for cart in carts:
            Username, StockName, Quantity, Price, Category, Status = cart
            CartDB.write(f"{Username},{StockName},{Quantity},{Price},{Category},{Status}\n")

def cus_placeorder(user):
    while True:
        print("\nPlace Order Menu:")
        stocks = load_stock()
        display_index = 1
        for stock in stocks:
            print(f"{display_index}. StockName: {stock[0]}, Quantity: {stock[1]}, Price: {stock[2]}, Category: {stock[3]}")
            display_index+=1
        stock_choice=input("Which stock do you want to purchase? (Type 0 to exit)")
        if stock_choice == "0":
            print("exiting..")
            return None
        elif stock_choice.isdigit():
            stock_choice = int(stock_choice) - 1
            if 0 <= stock_choice < len(stocks):
                stock = stocks[stock_choice]
                carts = load_carts()
                already_in_cart = False
                for cart in carts:
                    if cart[0] == user[0] and cart[1] == stock[0]:
                        already_in_cart = True
                        break
                if not already_in_cart:
                    print(
                        f"StockName: {stock[0]}, Quantity: {stock[1]}, Price: {stock[2]}, Category: {stock[3]}")
                    addcartquantity = input(f"How much do you want to add to cart? (There is {stock[1]} in stock) ")
                    if addcartquantity.isdigit():
                        addcartquantity = int(addcartquantity)
                        if addcartquantity > stock[1]:
                            print("Not enough item in stock.")
                        else:
                            cart = [user[0], stock[0], addcartquantity, stock[2], stock[3], "Unpaid"]
                            carts.append(cart)
                            save_carts(carts)
                            print("Added to Cart Successfully!")
                            neworder = cart
                            return (neworder)
                    else:
                        print("Please enter a valid quantity.")
                else:
                    print("Item already in cart")
            else:
                print("Invalid stock number!")
        else:
            print("Invalid input! Please enter a valid stock number or type 0 to exit.")

def cus_modifyorder(user):
    while True:
        carts=load_carts()
        cart_indices = []
        cart_count=0
        display_index = 1
        for i, cart in enumerate(carts):
            if user[0]==cart[0] and cart[5]=="Unpaid":
                print(f"{display_index}. StockName: {cart[1]}, Quantity: {cart[2]}, Price: {cart[3]}, Category: {cart[4]}")
                cart_indices.append(i)
                cart_count += 1
                display_index += 1
        if cart_count == 0:
            print("No item in cart!")
            return None

        cart_choice=input("Which item do you want to modify? (Type 0 to exit): ")
        if cart_choice == "0":
            print("exiting..")
            return None
        elif cart_choice.isdigit():
            cart_choice = int(cart_choice) - 1
            if 0 <= cart_choice < len(cart_indices):
                cart=carts[cart_indices[cart_choice]]
                stocks=load_stock()
                stock = None
                for stock in stocks:
                    if stock[0]==cart[1]:
                        stock=stock
                        break
                if stock is not None:
                    newquantity = input(f"Enter how much you want to change to ({stock[1]} is available)")
                    if newquantity.isdigit():
                        newquantity = int(newquantity)
                        if newquantity > stock[1]:
                            print("Not enough item in stock.")
                        else:
                            cart = [user[0], cart[1], newquantity, cart[3], cart[4],cart[5]]
                            del carts[cart_indices[cart_choice]]
                            carts.append(cart)
                            save_carts(carts)
                            print("Modified Item Quantity Successfully!")
                            modifyorder = cart
                            return (modifyorder)
                    else:
                        print('Please enter a valid quantity')
                else:
                    print("Stock not found.")
            else:
                print('Invalid item number')
        else:
            print("Invalid input! Please enter a valid stock number or type 0 to exit.")

def cus_cancelorder(user):
    while True:
        carts=load_carts()
        cart_indices = []
        cart_count=0
        display_index = 1
        for i, cart in enumerate(carts):
            if user[0]==cart[0] and cart[5]=="Unpaid":
                print(f"{display_index}. StockName: {cart[1]}, Quantity: {cart[2]}, Price: {cart[3]}, Category: {cart[4]}")
                cart_indices.append(i)
                cart_count += 1
                display_index += 1
        if cart_count == 0:
            print("No item in cart!")
            break
        cart_choice = input("Which item do you want to cancel? (Type 0 to exit): ")
        if cart_choice == "0":
            print("exiting..")
            break
        elif cart_choice.isdigit():
            cart_choice = int(cart_choice) - 1
            if 0 <= cart_choice < len(cart_indices):
                cancelorder = carts[cart_indices[cart_choice]]
                del carts[cart_indices[cart_choice]]
                print("Order Cancelled Successfully!")
                save_carts(carts)
                return cancelorder
            else:
                print("Invalid Item")
        else:
            print("Invalid Item")

def cus_payment(user):
    while True:
        carts=load_carts()
        cart_indices = []
        cart_count=0
        total=0.0
        stocks=load_stock()
        display_index = 1
        not_enough_item_in_stock = False

        for i, cart in enumerate(carts):
            for stock in stocks:
                if stock[0] == cart[1] and user[0]==cart[0] and stock[1]<cart[2]:
                    not_enough_item_in_stock = True
                    print(f"Not enough stock for {cart[1]} (Requested: {cart[2]}, Available: {stock[1]})")
                    break
            if not_enough_item_in_stock == True:
                break
            if user[0]==cart[0] and cart[5]=="Unpaid":
                print(f"{display_index}. StockName: {cart[1]}, Quantity: {cart[2]}, Price: {cart[3]}, Category: {cart[4]}")
                cart_indices.append(i)
                cart_count += 1
                display_index += 1
                total+=(float(cart[2])*float(cart[3]))
        if not_enough_item_in_stock == True:
            break
        if cart_count == 0:
            print("No item in cart!")
            return None
        print("Total: RM",total)
        print("\nPlease Bank in the Money to the Following Details:")
        print("Bank: Maybank")
        print("Bank Name: KLCCC")
        print("Bank No.: 9087 5678 4396")
        print("Please send the Bank In Receipt Screenshot to +60109437156")
        choice = input("Press 0 to Exit / Type in (y) After Sent in Receipt: ")

        if choice == "0":
            print("Exit to Customer Menu")
            break
        elif choice == "y":
            madepayment = update_stock_after_payment(cart_indices)
            cus_makepayment_log(user, madepayment)
            print("Payment Complete")
            break
        else:
            print("Invalid Choice")

def update_stock_after_payment(cart_indices):
    carts = load_carts()
    stocks = load_stock()
    madepayment=[]
    paiditems= []
    for i in range(len(cart_indices)):
        cart = carts[cart_indices[i]]
        for stock in stocks:
            if cart[1] == stock[0]:
                stock[1]-=cart[2]
                cart[5] = "Paid"
                madepayment.append(cart)
                break
    for i in range(len(carts) - 1, -1, -1):
        if carts[i][5] == 'Paid':
            paiditems.append(carts[i])
            del carts[i]
    save_stock(stocks)
    save_carts(carts)
    add_purchase_history(paiditems)
    return (madepayment)

def cus_inquireorder(user):
    while True:
        carts=load_carts()
        cart_indices = []
        cart_count=0
        display_index = 1
        for i, cart in enumerate(carts):
            if user[0]==cart[0] and cart[5]=="Unpaid":
                print(f"{display_index}. StockName: {cart[1]}, Quantity: {cart[2]}, Price: {cart[3]}, Category: {cart[4]}")
                cart_indices.append(i)
                cart_count += 1
                display_index+=1
        if cart_count == 0:
            print("No item in cart!")
            return None
        choice = input("Type 0 if you are done checking:")
        if choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

def loadpurchasehistory():
    purchasehistories = []
    try:
        with open("Purchase_HistoryDB.txt", "xt") as Purchase_HistoryDB:
            pass
    except FileExistsError:
        pass
    finally:
        with open("Purchase_HistoryDB.txt", "r") as Purchase_HistoryDB:
            for line in Purchase_HistoryDB:
                username, stock_name, quantity, price, category = line.strip().split(',')
                purchasehistories.append([username, stock_name, int(quantity), float(price), category])
    return purchasehistories

def cus_report(user):
    while True:
        print("\nPurchase History")
        totalspent=0.0
        purchase_count=0
        purchasehistories = loadpurchasehistory()
        for i in purchasehistories:
            if user[0]==i[0]:
                print(f"Stock Name:{i[1]}, Quantity:{i[2]}, Price:{i[3]}, Category:{i[4]}")
                purchase_count+=1
                totalspent+=(float(i[2])*float(i[3]))
        if purchase_count == 0:
            print("No Purchases Made Yet")
            break
        else:
            print(f"Total: RM{totalspent}")
            choice = input("Type 0 If You Want to Exit")
            if choice == "0":
                print("Going back to Customer Menu...")
                break
            else:
                print("Type 0 If You Want to Exit")


#ADMIN/USERMANAGEMENT

def usermanagementmenu1(user):
    while True:
        print("\nUser Management Menu:\n"
              "1. Add Users\n"
              "2. Verify New Customer or New Admin\n"
              "3. Modify User Personal Details\n"
              "4. Disable User Access\n"
              "5. User's system usage\n"
              "6. Check Customer Order Status\n"
              "7. Reports\n"
              "8. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            newuser=adduser()
            if newuser == None:
                continue
            adduser_log(user, newuser)
        elif choice == "2":
            approvalmenu(user)
        elif choice == "3":
            modifycustomer=modify_customer()
            if modifycustomer == None:
                continue
            modifyuser_log(user, modifycustomer)
        elif choice == "4":
            disableuser = disable_user()
            if disableuser == None:
                continue
            disableuser_log(user, disableuser)
        elif choice == "5":
            inquire_system_usage()
        elif choice == "6":
            admin_check_order()
        elif choice == "7":
            admin_check_customer()
        elif choice == "8":
            logout_log(user)
            print("\nExiting User Management Menu...")
            print("Exiting User Management Menu Successfully")
            break
        else:
            print("\nInvalid options! Please try again.")

def usermanagementmenu2(user):
    while True:
        print("\nUser Management Menu:\n"
              "1. Verify New Customer\n"
              "2. Check Customer Order Status\n"
              "3. Reports\n"
              "4. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            approveuser = approving_customer()
            if approveuser == None:
                continue
            approveuser_log(user, approveuser)
        elif choice == "2":
            admin_check_order()
        elif choice == "3":
            admin_check_customer()
        elif choice == "4":
            logout_log(user)
            print("\nExiting User Management Menu...")
            print("Exiting User Management Menu Successfully")
            break
        else:
            print("\nInvalid options! Please try again.")


def adduser():
    while True:
        print('\nAdd User Menu:')

        # Input for username with option to go back
        username = input('Username (Press Enter to go back): ').strip().capitalize()
        if username == '':
            print("\nGoing back to the previous menu.")
            return None

        users = load_users()
        username_taken = False
        for user in users:
            if user[0] == username:
                print('\nUsername is taken!')
                username_taken = True
                break
        if username_taken:
            continue

        # Input for password
        password = input('Enter Password: ').strip()
        if password == '':
            print("\nPassword cannot be empty. Please try again.")
            continue

        # Input for role with option to go back
        while True:
            role = input("Enter role (customer/admin/staff): ").strip()
            if role in ['customer', 'admin', 'staff']:
                break
            else:
                print("Invalid role. Please try again.")

        # Add user if all inputs are valid
        user = [username, password, role, 'True', 0]
        users.append(user)
        save_users(users)
        print('\nUser added successfully.')
        newuser = user
        return (newuser)

def approving_customer():
    while True:
        print("\nCustomer approval menu:\n")
        users = load_users()
        customer_indices = []
        customer_count = 0
        display_index = 1
        for i, user in enumerate(users):
            if user[2]=='customer' and (user[3]=='False' or user[3]=='Disabled'):
                print(f"{display_index}. Username: {user[0]}, Password: {user[1]}, Role: {user[2]}, Approval: {user[3]}")
                customer_indices.append(i)
                customer_count += 1
                display_index += 1
        if customer_count == 0:
            print("No pending customer approvals!")
            return None
        customer_choice = input("Which customer do you want to approve? (Type 0 to exit)")
        if customer_choice == "0":
            print("Exiting..")
            return None
        elif customer_choice.isdigit():
            customer_choice = int(customer_choice) - 1
            if 0 <= customer_choice < len(customer_indices):
                user=users[customer_indices[customer_choice]]
                user[3]="True"
                del users[customer_indices[customer_choice]]
                users.append(user)
                save_users(users)
                print('\nCustomer Approved Successfully!')
                approveuser = user
                return (approveuser)
            else:
                print("Invalid Customer")
        else:
            print("Invalid Customer")


def approving_admin():
    while True:
        print("\nAdmin Approval Menu:\n")
        users = load_users()
        admin_indices = []
        admin_count = 0
        display_index = 1
        for i, user in enumerate(users):
            if user[2]=='admin' and (user[3]=='False' or user[3]=='Disabled'):
                print(f"{display_index}. Username: {user[0]}, Password: {user[1]}, Role: {user[2]}, Approval: {user[3]}")
                admin_indices.append(i)
                admin_count += 1
                display_index += 1
        if admin_count == 0:
            print("No pending admin approvals!")
            return None
        admin_choice = input("Which admin do you want to approve? (Type 0 to exit)")
        if admin_choice == "0":
            print("Exiting..")
            return None
        elif admin_choice.isdigit():
            admin_choice = int(admin_choice) - 1
            if 0 <= admin_choice < len(admin_indices):
                user=users[admin_indices[admin_choice]]
                user[3]="True"
                del users[admin_indices[admin_choice]]
                users.append(user)
                save_users(users)
                print('\nAdmin Approved Successfully!')
                approveuser = user
                return (approveuser)
            else:
                print("Invalid Admin")
        else:
            print("Invalid Admin")

def approvalmenu(user):
    while True:
        print("\nApproval Menu:\n"
              "1. Customer Approval\n"
              "2. Admin Approval\n"
              "3. Back")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            approveuser=approving_customer()
            if approveuser==None:
                continue
            approveuser_log(user, approveuser)
        elif choice == "2":
            approveuser=approving_admin()
            if approveuser==None:
                continue
            approveuser_log(user, approveuser)
        elif choice == "3":
            break
        else:
            print("\nInvalid options! Please try again.")

def modify_customer():
    while True:
        print("\nModify Customer Details Menu:\nPress '0' to exit")
        customers = load_customerdetails()
        indices = []
        count = 0

        # Display the list of customers with indices starting from 1
        for i in range(len(customers)):
            customer = customers[i]
            print(f"{count + 1}. Username: {customer[0]} Name: {customer[2]}")
            indices.append(i)
            count += 1

        # Input validation for customer selection
        while True:
            try:
                choice = int(input('\nEnter Number: '))
                if choice == 0:
                    print("\nExiting Modify Customer Details Menu ...")
                    return None
                if choice < 1 or choice > count:
                    print("\nInvalid choice. Please select a valid number.")
                    continue
                break
            except ValueError:
                print("\nInvalid input. Please enter a numeric value.")

        customer = customers[indices[choice - 1]]

        while True:
            print(f"\nModify {customer[0]}'s Details:")
            print("1. IC/Passport Number:", customer[1])
            print("2. Name:", customer[2])
            print("3. Phone Number:", customer[3])
            print("4. City of Domicile:", customer[4])
            print("Press '0' to go back to previous menu.")

            try:
                modify = int(input("\nEnter Number: "))
                details = list(customer)

                if modify == 1:
                    details[1] = str(input("\nEnter IC or Passport Number: "))
                elif modify == 2:
                    details[2] = str(input("\nEnter Name: "))
                elif modify == 3:
                    details[3] = str(input("\nEnter Phone Number: "))
                elif modify == 4:
                    details[4] = str(input("\nEnter City of Domicile: "))
                elif modify == 0:
                    break
                else:
                    print("\nInvalid option! Please try again.")
                    continue

                # Update customer details
                newdetails = [details[0], details[1], details[2], details[3], details[4], details[5]]
                del customers[indices[choice - 1]]
                customers.append(newdetails)
                save_customer(customers)
                print('\nCustomer Details Modified Successfully!')
                modifycustomer=newdetails
                return(modifycustomer)
            except ValueError:
                print("\nInvalid input. Please enter a numeric value.")

def disable_user():
    users = load_users()

    while True:
        indices = []
        count = 0
        print("\nDisable User Access Menu:\n")

        for i in range(len(users)):
            user = users[i]
            if (user[2] == "customer" or user[2] == "admin" or user[2]=="staff") and user[3] == "True":
                print(f"{count + 1}. Username: {user[0]}, Password: {user[1]}, Role: {user[2]}, Status: {user[3]}")
                indices.append(i)
                count += 1

        if count == 0:
            print("\nNo active users to disable.")

        print("\nPress 0 to go back.")

        choice = input('Enter Number: ')
        if not choice.isdigit():
            print("\nInvalid input. Please enter a numeric value.")
            continue

        choice = int(choice)

        if choice == 0:
            print("\nGoing back to the previous menu.")
            return None

        if choice < 1 or choice > count:
            print("\nInvalid choice.")
            continue

        user = users[indices[choice - 1]]
        user[3] = "Disabled"
        del users[indices[choice - 1]]
        users.append(user)
        save_users(users)

        print('\nUser Access Disabled Successfully!')
        disableuser = user
        return (disableuser)


def admin_check_order():
    while True:
        print("\nCheck Customer Order menu:\n")
        users = load_users()
        customer_indices = []
        customer_count = 0
        display_index = 1
        for i, user in enumerate(users):
            if user[2] == 'customer' and (user[3] == 'True'):
                print(f"{display_index}. Username: {user[0]}, Password: {user[1]}, Role: {user[2]}, Approval: {user[3]}")
                customer_indices.append(i)
                customer_count += 1
                display_index += 1
        if customer_count == 0:
            print("No Customer orders Available")
            return None
        customer_choice = input("Which customer do you want check? (Type 0 to exit)")
        if customer_choice == "0":
            print("Exiting..")
            return None
        elif customer_choice.isdigit():
            customer_choice = int(customer_choice) - 1
            if 0 <= customer_choice < len(customer_indices):
                user = users[customer_indices[customer_choice]]
                cus_inquireorder(user)
            else:
                print("Invalid Customer")
        else:
            print("Invalid Customer")

def inquire_system_usage():
    while True:
        users=load_users()
        for user in users:
            if user[4]>0:
                print(f"Username:{user[0]},Role:{user[2]},Usage:{user[4]}")
        choice = input("Type 0 After Done Checking:")
        if choice =="0":
            break
        else:
            print("Type 0 to Exit")

def admin_check_customer():
    while True:
        try:
            with open("payment_history.txt", "r") as payment_history:
                lines = payment_history.readlines()

            if not lines:
                print("No one made a purchase yet.")
                break
            else:
                print("Latest 10 Payment Transactions:")
                latest_lines = lines[-10:]
                for line in latest_lines:
                    print(line.strip())
                print("For Complete Payment History Please Refer to (payment_history.txt)")
                choice = input("Type 0 After Done Checking:")
                if choice == "0":
                    break
                else:
                    print("Invalid Option")
        except FileNotFoundError:
            print("No purchase records found.")
            break

#LOG

def log_activity(username,role, activity,details=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if details:
        log_message = f"{current_time} - {username} ({role}): {activity} {details}\n"
    else:
        log_message = f"{current_time} - {username} ({role}): {activity}\n"
    with open("activity_log.txt", "a") as log_file:
        log_file.write(log_message)

def login_log(user):
    log_activity(user[0],user[2], "Logged in")
    users = load_users()
    for index, i in enumerate(users):
        if user[0] == i[0]:
            users[index][4] += 1
            break
    save_users(users)

def logout_log(user):
    log_activity(user[0],user[2], "Logged out")

def newuser_log(newuser):
    log_activity(newuser[0], newuser[2], "Created Account:", newuser)

def adduser_log(user, newuser):
    log_activity(user[0], user[2], "Added new user:", newuser)

def approveuser_log(user, approveuser):
    log_activity(user[0], user[2], "Approved User:", approveuser)

def modifyuser_log(user, modifycustomer):
    log_activity(user[0], user[2], "Modified Customer:", modifycustomer)

def disableuser_log(user, disableuser):
    log_activity(user[0], user[2], "Disabled User:", disableuser)

def cus_addorder_log(user,neworder):
    log_activity(user[0], user[2], "Placed Order:",neworder)

def cus_modifyorder_log(user,modifyorder):
    log_activity(user[0], user[2], "Modified Order:",modifyorder)

def cus_cancelorder_log(user,cancelorder):
    log_activity(user[0], user[2], "Cancelled Order:",cancelorder)

def paymenthistory_log(username,role, activity,details=None):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if details:
        log_message = f"{current_time} - {username} ({role}): {activity} {details}\n"
    with open("payment_history.txt", "a") as payment_history:
        payment_history.write(log_message)

def cus_makepayment_log(user,madepayment):
    for paymentitem in madepayment:
        paymenthistory_log(user[0], user[2], "Made Payment for",paymentitem)
    log_activity(user[0], user[2], "Made Payment for",f"{len(madepayment)} items")

def add_purchase_history(paiditems):
    for paiditem in paiditems:
        purchase_history = f"{paiditem[0]},{paiditem[1]},{paiditem[2]},{paiditem[3]},{paiditem[4]}\n"
        with open("Purchase_HistoryDB.txt", "a") as Purchase_HistoryDB:
            Purchase_HistoryDB.write(purchase_history)

def inv_modify_stock_log(user,modifiedstock):
    log_activity(user[0], user[2], "Modified Stock:", modifiedstock)

def inv_add_order_log(user, neworder):
    log_activity(user[0], user[2], "Placed Order:", neworder)

def inv_modify_order_log(user, modifiedorder):
    log_activity(user[0], user[2], "Modified Order:", modifiedorder)

def inv_cancel_order_log(user, cancelorder):
    log_activity(user[0], user[2], "Canceled Order:", cancelorder)

def inv_add_new_stock(user, newstock):
    log_activity(user[0], user[2], "Added Stock:", newstock)

#INVENTORY
def inventorymenu(user):
    while True:
        print("\nHello!, Please choose an option.....")
        print("1. Create Purchase Order")
        print("2. Check/Add/Modify Stock")
        print("3. Check Purchase Order Status")
        print("4. Modify Purchase Order")
        print("5. Cancel Purchase Order")
        print("6. Make Payment")
        print("7. Generate Reports")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nPurchase Order selected...")
            neworder=purchase_order()
            if neworder == None:
                continue
            inv_add_order_log(user, neworder)
        elif choice == "2":
            print("\nChecking Stock....")
            stock_menu(user)
        elif choice == "3":
            print("\nCheck Purchase Order Status....")
            check_purchase_order_status()
        elif choice == "4":
            print("\nModify Purchase Order....")
            modifiedorder=modify_purchase_order()
            if modifiedorder == None:
                continue
            inv_modify_order_log(user, modifiedorder)
        elif choice == "5":
            print("Cancel Purchase order...")
            cancelorder=cancel_inv_purchase_order()
            if cancelorder == None:
                continue
            inv_cancel_order_log(user, cancelorder)
        elif choice == "6":
            inv_makepayment()

        elif choice == "7":
            print("\nGenerating Reports...")
            inv_report()
        elif choice == "8":
            logout_log(user)
            print("Exiting...")
            break
        else:
            print("Invalid Choice for Option")

def load_stock():
    stocks = []
    try:
        with open("StockDB.txt", "x") as StockDB:  # Use 'x' mode to create the file if it doesn't exist
            StockDB.write('StockName, Quantity, Price, Category\n')
            StockDB.write('Logitech G304, 20, 100.00, mouse\n')
            StockDB.write("Ajazz Ak820, 10, 180.00, keyboard\n")
            StockDB.write("Kingston SSD (512GB), 20, 200.00, hard disk\n")
            StockDB.write("Repair, 999999999, 100.00, Repair\n")
    except FileExistsError:
        pass
    finally:
        with open("StockDB.txt", "r") as StockDB:
            next(StockDB)  # Skip the header
            for line in StockDB:
                StockName, Quantity, Price, Category = line.strip().split(',')
                stocks.append([StockName, int(Quantity), float(Price), Category])
    return stocks

def save_stock(stocks):
    with open("StockDB.txt", "w") as StockDB:
        StockDB.write('StockName, Quantity, Price, Category\n')
        for user in stocks:
            StockName, Quantity, Price, Category = user
            StockDB.write(f"{StockName},{Quantity},{Price},{Category}\n")

def stock_menu(user):
    while True:
        print("\n1. Check Stock\n"
              "2. Add New Stock\n"
              "3. Modify Stock\n"
              "4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            check_stock()
        elif choice == "2":
            newstock=add_new_stock()
            if newstock == None:
                continue
            inv_add_new_stock(user, newstock)
        elif choice == "3":
            modifiedstock=modify_stock()
            if modifiedstock == None:
                continue
            inv_modify_stock_log(user, modifiedstock)
        elif choice == "4":
            print("Exiting Back to Inventory Menu ")
            break
        else:
            print("Invalid choice, Please type (1/2/3).")

def check_stock():
    while True:
        print("\nCheck Stock Page:\n")
        stocks = load_stock()
        stock_indices = []
        stock_count = 1
        for i in range(len(stocks)):
            stock = stocks[i]
            print(stock_count, stock[0], stock[1], stock[2], stock[3])
            stock_indices.append(i)
            stock_count +=1
        print("Do you finish checking?\n"
                "1. Yes\n"
                "2. No\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Exiting Check Stock...")
            break
        elif choice == "2":
            print("Alright, take your time....")
        else:
            print("Invalid choice, Please enter a number (1/2).")

def modify_stock():
    while True:
        print("\nModify Stock Details Menu:\n")
        stocks = load_stock()
        display_index = 1
        for stock in stocks:
            print(f"{display_index}. StockName: {stock[0]}, Quantity: {stock[1]}, Price: {stock[2]}, Category: {stock[3]}")
            display_index+=1
        print("Do you want to modify stock?\n"
              "1. Yes\n"
              "2. No\n")

        choice = input("Enter your choice: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                display_index = 1
                for stock in stocks:
                    print(f"{display_index}. StockName: {stock[0]}, Quantity: {stock[1]}, Price: {stock[2]}, Category: {stock[3]}")
                    display_index += 1
                stock_choice = input("Enter the number of the stock item to modify:"
                                         "\n (Type anything back to modify stock menu...) ")
                if stock_choice.isdigit():
                    stock_choice = int(stock_choice)-1
                    if 0 <= stock_choice < len(stocks):
                        stock = stocks[stock_choice]
                        print(f"\n1. Stock name: {stock[0]}")
                        print(f"2. Quantity: {stock[1]}")
                        print(f"3. Price: {stock[2]}")
                        print(f"4. Category: {stock[3]}")
                        modify = input("\nEnter the number of the detail you want to modify (1-4): ")
                        if modify == "1":
                            stocks[stock_choice][0] = input("Enter new stock name: ")
                            save_stock(stocks)
                            print('Stock details modified successfully!')
                            modifiedstock = stocks[stock_choice]
                            return (modifiedstock)
                        elif modify == "2":
                            new_quantity = input("Enter new quantity: ")
                            if new_quantity.isdigit():
                                stocks[stock_choice][1] = int(new_quantity)
                                save_stock(stocks)
                                print('Stock details modified successfully!')
                                modifiedstock = stocks[stock_choice]
                                return (modifiedstock)
                            else:
                                print("Invalid input! Please enter a valid number for quantity.")
                        elif modify == "3":
                            new_price = input("Enter new price: ")
                            if new_price.replace('.', '', 1).isdigit():
                                stocks[stock_choice][1] = float(new_price)
                                save_stock(stocks)
                                print('Stock details modified successfully!')
                                modifiedstock = stocks[stock_choice]
                                return (modifiedstock)
                            else:
                                print("Invalid input! Please enter a valid number for quantity.")
                        elif modify == "4":
                            stocks[stock_choice][3] = input("Enter new category: ")
                            save_stock(stocks)
                            print('Stock details modified successfully!')
                            modifiedstock = stocks[stock_choice]
                            return (modifiedstock)
                        else:
                            print("Invalid option!")
                    else:
                        print("Invalid stock number!")
                else:
                    print("Invalid stock number!")
            elif choice == 2:
                print("Exiting....")
                return None
            else:
                print("Invalid choice. Please enter 1 or 2.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

#INVENTORY PURCHASE ORDER
def load_inv_orders():
    orders=[]
    try:
        with open("InvOrdersDB.txt", "x") as InvOrdersDB:
            InvOrdersDB.write('StockName, Quantity, BuyingPrice, SellingPrice, Category, Status\n')
    except FileExistsError:
        pass
    finally:
        with open("InvOrdersDB.txt", "r") as InvOrdersDB:
            next(InvOrdersDB)
            for line in InvOrdersDB:
                StockName, Quantity, BuyingPrice, SellingPrice, Category, Status = line.strip().split(',')
                orders.append([StockName, int(Quantity), float(BuyingPrice), float(SellingPrice), Category, Status])
    return orders

def save_inv_orders(orders):
    with open("InvOrdersDB.txt", "w") as InvOrdersDB:
        InvOrdersDB.write('StockName, Quantity, BuyingPrice, SellingPrice, Category, Status\n')
        for order in orders:
            StockName, Quantity, BuyingPrice, SellingPrice, Category, Status = order
            InvOrdersDB.write(f"{StockName},{Quantity},{BuyingPrice},{SellingPrice},{Category},{Status}\n")


def purchase_order():
    while True:
        print("\nYour Options have:")
        print("1. Enter new purchase order.")
        print("2. Back to menu.")
        try:
            option = int(input("Select your choice: "))
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        if option == 1:
            print(f"\nEnter details for New purchase order stock..:")
            stockname = input("Stock Name: ")

            try:
                quantity = int(input("Quantity: "))
            except ValueError:
                print("Invalid input! Quantity should be a numeric value.")
                continue

            try:
                buyingprice = float(input("Buying Price (RM): "))
            except ValueError:
                print("Invalid input! Buying Price should be a numeric value.")
                continue

            try:
                sellingprice = float(input("Selling Price (RM): "))
            except ValueError:
                print("Invalid input! Selling Price should be a numeric value.")
                continue
            category = input("Category: ")
            if not category.isalnum():
                print("Invalid input! Category should only contain alphanumeric characters.")
                continue
            order = [stockname, quantity, buyingprice, sellingprice, category, 'unpaid']
            orders = load_inv_orders()
            orders.append(order)
            save_inv_orders(orders)
            print("Order Placed Successfully")
            neworder = order
            return (neworder)
        elif option == 2:
            print("Returning to menu...")
            return None
        else:
            print("Invalid option. Please select 1 or 2.")


def check_purchase_order_status():
    while True:
        orders=load_inv_orders()
        order_count = 0
        for i, order in enumerate(orders):
            print(f"{i + 1}. StockName: {order[0]}, Quantity: {order[1]}, Buying Price: {order[2]}, Selling Price: {order[3]}, Category: {order[4]}, Status:{order[5]}")
            order_count += 1
        if order_count == 0:
            print("No Orders Pending Payment!")
            return None
        choice = input("Type 0 if you are done checking:")
        if choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice")





def modify_purchase_order():
    while True:
        print("\nModify Purchase Order:\n")
        orders=load_inv_orders()
        for i, order in enumerate(orders):
            print(f"{i+1}. StockName: {order[0]}, Quantity: {order[1]}, Buying Price: {order[2]}, Selling Price: {order[3]}, Category: {order[4]}, Status:{order[5]}")

        order_choice = input("Enter the number of the purchase order to modify (or type 'back' to return): ")

        if order_choice.lower() == 'back':
            print("Returning to Inventory Menu...")
            return

        if not order_choice.isdigit() or not (1 <= int(order_choice) <= len(orders)):
            print("Invalid purchase order number! Please try again.")
            continue

        order_choice = int(order_choice) - 1
        order = orders[order_choice]
        print("Selected Purchase Order;")
        print(f"1. Stock name: {order[0]}")
        print(f"2. Quantity: {order[1]}")
        print(f"3. Buying Price: {order[2]}")
        print(f"4. Selling Price: {order[3]}")
        print(f"5. Category: {order[4]}")


        modify_choice = input("Enter the number of the detail you want to modify: ")
        if modify_choice == "1":
            orders[order_choice][0] = input("Enter new stock name: ")
            save_inv_orders(orders)
            print('Purchase order modified successfully!')
            modifiedorder = orders[order_choice]
            return (modifiedorder)
        elif modify_choice == "2":
            new_quantity = input("Enter new quantity: ")
            if new_quantity.isdigit():
                orders[order_choice][1] = int(new_quantity)
                save_inv_orders(orders)
                print('Purchase order modified successfully!')
                modifiedorder = orders[order_choice]
                return (modifiedorder)
            else:
                print("Invalid input! Please enter a valid number for quantity.")
        elif modify_choice == "3":
            new_buying_price = input("Enter new Buying Price: ")
            if new_buying_price.replace('.', '', 1).isdigit():
                orders[order_choice][2] = float(new_buying_price)
                save_inv_orders(orders)
                print('Purchase order modified successfully!')
                modifiedorder = orders[order_choice]
                return (modifiedorder)
            else:
                print("Invalid input! Please enter a valid number for buying price.")
        elif modify_choice == "4":
            new_selling_price = input("Enter new Selling Price: ")
            if new_selling_price.replace('.', '', 1).isdigit():
                orders[order_choice][3] = float(new_selling_price)
                save_inv_orders(orders)
                print('Purchase order modified successfully!')
                modifiedorder = orders[order_choice]
                return (modifiedorder)
            else:
                print("Invalid input! Please enter a valid number for selling price.")
        elif modify_choice == "5":
            orders[order_choice][4] = input("Enter New Category: ")
            save_inv_orders(orders)
            print('Purchase order modified successfully!')
            modifiedorder = orders[order_choice]
            return (modifiedorder)
        else:
            print("Invalid choice!")








def cancel_inv_purchase_order():
    while True:
        orders = load_inv_orders()
        order_indices= []
        order_count = 0
        for i, order in enumerate(orders):
            print(f"{i + 1}. StockName: {order[0]}, Quantity: {order[1]}, Buying Price: {order[2]}, Selling Price: {order[3]}, Category: {order[4]}, Status:{order[5]}")
            order_indices.append(i)
            order_count+=1
        if order_count == 0:
            print("There are no purchase order pending")
        order_choice = input("Which purchase order do you want to cancel? (Type 0 to return): ")

        if order_choice == "0":
            print("Returning to Inventory Menu...")
            return None

        elif order_choice.isdigit():
            order_choice = int(order_choice) - 1
            if 0 <= order_choice < len(order_indices):
                cancelorder = orders[order_indices[order_choice]]
                del orders[order_indices[order_choice]]
                print("Order Cancelled Successfully!")
                save_inv_orders(orders)
                return cancelorder

            else:
                print("Invalid option")
        else:
            print("Invalid option")

def loadinvpurchasehistory():
    invpurchasehistories = []
    try:
        with open("InvPurchase_HistoryDB.txt", "xt") as InvPurchase_HistoryDB:
            InvPurchase_HistoryDB.write("Stock Name, Quantity, Buying Price, Selling Price, Category, Status\n")
    except FileExistsError:
        pass
    finally:
        with open("InvPurchase_HistoryDB.txt", "r") as InvPurchase_HistoryDB:
            for line in InvPurchase_HistoryDB:
                stock_name, quantity, buyingprice, sellingprice, category, status = line.strip().split(',')
                invpurchasehistories.append([stock_name, int(quantity), float(buyingprice), float(sellingprice), category, status])
    return invpurchasehistories

def inv_report():
    while True:
        print("\nPurchase History")
        totalspent=0.0
        purchase_count=0
        purchasehistories = loadinvpurchasehistory()
        for i in purchasehistories:
            print(f"Stock Name:{i[0]}, Quantity:{i[1]}, Buying Price:{i[2]}, Selling Price:{i[3]} Category:{i[4]}")
            purchase_count+=1
            totalspent+=(float(i[1])*float(i[2]))
        if purchase_count == 0:
            print("No Purchases Made Yet")
            break
        else:
            print(f"Total: RM{totalspent}")
            choice = input("Type 0 If You Want to Exit")
            if choice == "0":
                print("Going back to Inventory Menu...")
                break
            else:
                print("Type 0 If You Want to Exit")

def inv_makepayment():
    while True:
        orders=load_inv_orders()
        paiditems=[]
        order_count=0
        total=0.0
        display_index = 1
        for order in orders:
            if order[5]=="unpaid":
                print(f"{display_index}. StockName: {order[0]}, Quantity: {order[1]},Buying Price: {order[2]},Selling Price: {order[3]} Category: {order[4]}")

                order_count += 1
                display_index += 1
                total+=(float(order[1])*float(order[2]))
        if order_count == 0:
            print("No item in cart!")
            return None
        print("Total: RM",total)
        choice = input("Make Payment (Type 0 to Exit): ")
        if choice == "0":
            break
        for order in orders:
            order[5]= "paid"
            paiditem=order
            paiditems.append(paiditem)
        for i in range(len(orders) - 1, -1, -1):
            if orders[i][5] == 'paid':
                del orders[i]
        save_inv_orders(orders)
        add_invpurchase_history(paiditems)
        print("Payment Successful!, Please remember to change stock numbers")
        return

def add_invpurchase_history(paiditems):
    for paiditem in paiditems:
        purchase_history = f"{paiditem[0]},{paiditem[1]},{paiditem[2]},{paiditem[3]},{paiditem[4]},{paiditem[5]}\n"
        with open("InvPurchase_HistoryDB.txt", "a") as InvPurchase_HistoryDB:
            InvPurchase_HistoryDB.write(purchase_history)

def add_new_stock():
    print('\nAdd New Stock')
    while True:
        stockname=input("Enter Stock Name (Type 0 to Exit): ")
        if stockname == "0":
            return None
        stocks = load_stock()
        stocksamename = False
        for stock in stocks:
            if stock[0]==stockname:
                print("Already have stock of the same name!")
                stocksamename = True
                break
        if stocksamename == True:
            continue
        try:
            quantity = int(input("Enter Quantity: "))
        except ValueError:
            print("Invalid input! Quantity should be a numeric value.")
            continue

        try:
            price = float(input("Enter Price:RM "))
        except ValueError:
            print("Invalid input! Quantity should be a numeric value.")
            continue

        category = input("Enter Category: ")
        if not category.isalnum():
            print("Invalid input! Category should only contain alphanumeric characters.")
            continue
        stock = [stockname, quantity, price, category]
        stocks=load_stock()
        stocks.append(stock)
        save_stock(stocks)
        newstock = stock
        print("Stock Added Successfully!")
        return (newstock)


def main():
    while True:
        print('\nMenu:')
        print('''1.Register\n2.Login\n3.Exit Program''')
        choice = input('Enter your choice: ')
        if choice == '1':
            newuser=register()
            if newuser == None:
                continue
            newuser_log(newuser)

        elif choice == '2':
            user=login()
            if user:
                if user[2] == 'customer':
                    checkcustomerfilleddetails(user)
                    login_log(user)
                    customermanagementmenu(user)
                elif user[2] == 'admin':
                    login_log(user)
                    usermanagementmenu2(user)

                elif user[2] == 'super_user':
                    login_log(user)
                    usermanagementmenu1(user)

                elif user[2] == 'staff':
                    login_log(user)
                    inventorymenu(user)
        elif choice == '3':
            print("\nExiting program...")
            return
        else:
            print("Invalid choice, please try again.")

main()