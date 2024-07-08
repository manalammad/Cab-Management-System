class user:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.trips = 0
        self.ID = 0

    def get_contact_number(self):
        return self.contact_number

    def get_password(self):
        return self.password

    def get_email(self):
        print(self.email)
        return self.email

    def get_name(self):
        return self.name

    def get_ID(self):
        return self.ID

    def signup(self, user_type, obj, vehicle_type):
        self.name = input('Enter your name ')
        self.contact_number = int(input('Enter your contact number '))
        self.trips = 0
        valid = True

        filename = user_type + '.txt'
        openfile = open(filename, 'a+')  # opening user type file
        found = False
        for line in openfile:
            line = line.strip('\n')
            line = line.split(',')
            if line != '':  # checking if file empty
                if line[2] == self.email:  # checking if email already registered
                    found = True
                    print('User already exists,log in to proceed')
                    valid = False
                    break
        if found == False:
            import random
            self.ID = random.randint(100000, 999999)  # generating random id
            for line in openfile:
                line = line.split(',')
                if self.ID == line[2]:  # checking if id already exists
                    self.ID = random.randint(100000, 999999)
            if user_type == 'driver':  # adding vehicle info for driver
                openfile2 = open('vehicle info.txt', 'a')
                vehicle_info = self.email + ',' + obj.vehicle_number + ',' + obj.vehicle_name + ',' + obj.vehicle_color + ',' + vehicle_type
                openfile2.write(vehicle_info + '\n')
                openfile2.close()
                current_location = input('Enter your current location : ')
                info = str(self.ID) + ',' + self.name + ',' + self.email + ',' + self.password + ',' + str(
                    self.contact_number) + ',' + str(self.trips) + ',' + current_location + ',' + vehicle_type
            else:
                info = str(self.ID) + ',' + self.name + ',' + self.email + ',' + self.password + ',' + str(
                    self.contact_number)  # concatinating user info

            outfile = open(filename, 'a')
            outfile.write(info + '\n')  # write user data into the file

            outfile.close()
            openfile.close()

            print('New user registered')
            print('Welcome', self.name, 'to this app')
        return valid

    def signin(self, user_type):
        # opening user_type files
        if user_type == 'customer':
            openfile = open('customer.txt', 'r')
        elif user_type == 'driver':
            openfile = open('driver.txt', 'r')
        else:
            print('Invalid option try again')
            openfile = None
        found = False
        for line in openfile:  # iterating through lines
            line = line.strip('\n')
            line = line.split(',')
            if line[2] == self.email and self.password == line[3]:  # checking if email and password registered
                found = True
                if found == True:
                    self.ID = line[0]
                    self.name = line[1]
                    self.contact_number = line[4]
        return found

    def setname(self, name):
        self.name = name

    def setpassword(self, password):
        self.password = password

    def setnumber(self, number):
        self.contact_number = number

    def display(self, user_type):
        if user_type == 1:
            filename = 'customer.txt'
        elif user_type == 2:
            filename = 'driver.txt'
        else:
            filename = None
        openfile = open(filename, 'r')
        for line in openfile:
            line = line.strip('\n')
            line = line.split(',')
            if line[2] == self.email:  # checking for required username's data
                print('User info:')
                print('Name: ', line[1])
                print('User name : ', self.email)
                print('Contact Number : ', line[4])
                if user_type == 2:
                    print('Trips : ', line[5])


class customer(user):

    def __init__(self, name, username, password, number):
        super().__init__(username, password)

    def display(self, user_type):
        super().display(user_type)

    def book_ride(self, bookingobj):
        filename = (self.email + '.txt')  # opening desired customer's file
        openfile = open(filename, 'a')
        bookingobj = bookingobj
        self.trips += 1
        vehicle_type = input('Do you want to book a car or bike or rikshaw?(c/b/r)')
        objects = None
        if vehicle_type == 'c':
            objects = bookingobj.book_car(self.email)
        elif vehicle_type == 'b':
            objects = bookingobj.book_bike(self.email)
        elif vehicle_type == 'r':
            objects = bookingobj.book_rickshaw(self.email)
        openfile.close()
        return (objects)

    def cancel_ride(self):

        filename = username + '.txt'  # opening desired customer's file
        readfile = open(filename, 'r')
        bookings_list = []  # creating empty list
        for line in readfile:
            bookings_list.append(line)  # writing each line into the list
        bookings_list.pop(-1)  # deleting last entry/line
        writefile = open(filename, 'w')
        for i in bookings_list:
            writefile.write(i)  # writing back modified data
        print('ride cancelled')

        readfile.close()
        writefile.close()

        print('Your ride has been cancelled')

    def tip(self):
        amount = 0
        choice = input('Do you want to tip your driver?')
        if choice == 'y':
            amount = int(input('Enter amount : '))
        return amount

    def transaction_history(self):
        total = 0
        line_count = 0
        desired_trips = int(input('For how many previous trips do u want to see your transaction history?'))
        filename = username + '.txt'  # opening desired customer's file
        openfile = open(filename, 'a')  # creating file if not present already
        openfile = open(filename, 'r')
        for line in openfile:
            if line_count <= desired_trips:
                line = line.strip('\n')
                line = line.split(',')
                line_count += 1
                print('driver name :', line[0], end=' ')
                print(', fare :', line[4], end=' ')
                print(', payment type: ', line[-1])
                total += int(line[4])  # calculating total money
        print('Total Money spent : ', total)

        openfile.close()

    def view_booking_history(self):
        filename = username + '.txt'  # opening desired customer's file
        openfile = open(filename, 'a')
        openfile = open(filename, 'r')
        for line in openfile:
            line = line.strip('\n')
            line = line.split(',')
            print('driver name :', line[0], end=' ')
            print(', vehicle type :', line[1], end=' ')
            print(', color :', line[2], end=' ')
            print(', registeration number :', line[3], end=' ')
            print(', fare :', line[4])

        openfile.close()


class Driver(user):

    def __init__(self, number, trips, ID, name, vehicleobj, email, password):
        super().__init__(email, password)
        self.number = number
        self.trips = trips
        self.vehicleobj = vehicleobj  # aggregation
        self.walletobj = wallet(email)
        self.total = 0

    def get_vehicle_number(self):
        return self.vehicleobj.get_vehicle_number()

    def get_vehicle_type(self):
        return self.vehicleobj.get_vehicle_type()

    def get_vehicle_name(self):
        return self.vehicleobj.get_vehicle_name()

    def get_vehicle_color(self):
        return self.vehicleobj.vehicle_color()

    def get_wallet_obj(self):
        return self.walletobj

    def transaction_history(self):
        line_count = 0
        desired_trips = int(input('For how many previous trips do u want to see your transaction history?'))
        print(super().get_email(),'email')
        filename = (super().get_email())+ '_transactions' + '.txt'  # opening desired driver's transactions file
        openfile = open(filename, 'a')
        openfile = open(filename, 'r')
        for line in openfile:
            if line_count < desired_trips:
                line = line.strip('\n')
                line = line.split(',')
                line_count += 1
                print("Transaction by : ", line[0], end=' ')
                print(', fare :', line[1])
                self.total += int(line[1])
        print('Total Money spent : ', self.total)  # total money

        openfile.close()

    def change_vehicle(self):
        self.vehicleobj = None
        print('Changing vehicle: ')
        print('New vehicle information :')
        vehicle_num = input('Enter vehicle number: ')
        vehicle_color = input('Enter vehicle color: ')
        vehicle_name = input('Enter vehicle name: ')
        print('Is your vehicle a:')
        print('1. Car')
        print('2. Bike')
        print('3. Rickshaw')
        vehicle_type = int(input('Enter choice:'))
        if vehicle_type == 1:
            vehicle_type = 'car'
            vehicleobj = car(email, vehicle_num, vehicle_color, vehicle_name)  # creating vehicle obj
        elif vehicle_type == 2:
            vehicle_type = 'bike'
            vehicleobj = bike(email, vehicle_num, vehicle_color, vehicle_name)
        else:
            vehicle_type = 'rickshaw'
            vehicleobj = rickshaw(email, vehicle_num, vehicle_color, vehicle_name)
        self.vehicleobj = vehicleobj
        openfile = open('vehicle info.txt', 'r')
        vehicles = []
        line_num = -1
        index = 0
        info = ''
        for line in openfile:
            line_num += 1
            line = line.strip('\n')
            vehicles.append(line)
            line = line.split(',')
            if email == line[0]:
                index = line_num
                info = self.email + ',' + vehicle_num + ',' + vehicle_name + ',' + vehicle_color + ',' + vehicle_type
        openfile.close()
        vehicles[index] = info
        writefile = open('vehicle info.txt', 'w')
        for i in range(len(vehicles)):
            writefile.write(vehicles[i] + '\n')
        writefile.close()

    def edit_profile(self):
        openfile = open('driver.txt', 'r')
        drivers = []
        line_num = -1
        index = 0
        info = ''
        location = input('Enter location: ')
        name = input('Enter name : ')
        password = input('Enter new password : ')
        for line in openfile:
            line_num += 1
            line = line.strip('\n')
            drivers.append(line)
            line = line.split(',')

            if email == line[2]:
                index = line_num
                ID = line[0]
                info = str(ID) + ',' + name + ',' + self.email + ',' + password + ',' + str(self.number) + ',' + str(
                    self.trips) + ',' + location + ',' + self.get_vehicle_type()

        openfile.close()
        drivers[index] = info
        writefile = open('driver.txt', 'w')
        for i in range(len(drivers)):
            writefile.write(drivers[i] + '\n')
        writefile.close()

    def withdraw_money(self):
        amount = int(input('How much money do you want to withdraw from your wallet?'))
        walletobj = self.get_wallet_obj()
        walletobj.withdraw(amount)

    def increment_trips(self):
        openfile = open('driver.txt', 'r')
        drivers = []
        line_num = -1
        trips = 0
        ID = 0
        name = ''
        user_name = ''
        password = ''
        number = 0
        location = ''
        vehicle_type = ''
        index = 0
        for line in openfile:
            line_num += 1
            line = line.strip('\n')
            drivers.append(line)
            line = line.split(',')

            if self.email == line[2]:
                index = line_num
                ID = line[0]
                name = line[1]
                user_name = line[2]
                password = line[3]
                number = line[4]
                trips = line[5]
                location = line[6]
                vehicle_type = line[7]
                desired_line = line
        trips = int(trips) + 1
        info = str(ID) + ',' + name + ',' + user_name + ',' + password + ',' + str(number) + ',' + str(
            trips) + ',' + location + ',' + vehicle_type
        openfile.close()
        drivers[index] = info
        writefile = open('driver.txt', 'w')
        for i in range(len(drivers)):
            writefile.write(drivers[i] + '\n')
        writefile.close()

    def view_profile(self):
        super().display(2)


class vehicle:

    def __init__(self, username, vehicle_num, vehicle_color, vehicle_name):
        self.username = username
        self.vehicle_number = vehicle_num
        self.vehicle_name = vehicle_name
        self.vehicle_color = vehicle_color

    def get_vehicle_number(self):
        return self.vehicle_number

    def get_vehicle_name(self):
        return self.vehicle_name

    def get_vehicle_color(self):
        return self.vehicle_color


class car(vehicle):

    def __init__(self, username, vehicle_num, vehicle_name, vehicle_color):
        super().__init__(username, vehicle_num, vehicle_name, vehicle_color)
        self.rate_per_km = 40
        self.vehicle_type = 'car'

    def get_rate_per_km(self):
        return self.rate_per_km

    def get_vehicle_type(self):
        return self.vehicle_type


class bike(vehicle):

    def __init__(self, username, vehicle_num, vehicle_name, vehicle_color):
        super().__init__(username, vehicle_num, vehicle_name, vehicle_color)
        self.rate_per_km = 18
        self.vehicle_type = 'bike'

    def get_rate_per_km(self):
        return self.rate_per_km

    def get_vehicle_type(self):
        return self.vehicle_type


class rickshaw(vehicle):

    def __init__(self, username, vehicle_num, vehicle_name, vehicle_color):
        super().__init__(username, vehicle_num, vehicle_name, vehicle_color)
        self.rate_per_km = 25
        self.vehicle_type = 'rickshaw'

    def get_rate_per_km(self):
        return self.rate_per_km

    def get_vehicle_type(self):
        return self.vehicle_type


# noinspection PyShadowingNames
class booking():

    def __init__(self, ploc, dloc, distance):
        self.pickup = ploc
        self.dropoff = dloc
        self.distance = distance
        self.payment_type = ''

    def get_pickup(self):
        return self.pickup

    def get_dropoff(self):
        return self.dropoff

    def book_car(self, customer_username):
        openfile = open('driver.txt', 'r')
        found = False
        driver = None
        driver_name = None
        driver_ID = None
        driver_username = None
        driver_password = None
        driver_password = None
        driver_number = None
        driver_currentloc = None
        driver_vehicle = None
        for line in openfile:
            line = line.strip('\n')
            line = line.split(',')

            if self.pickup == line[6] and line[7] == 'car':
                driver = line
                driver_ID = driver[0]
                driver_name = driver[1]
                driver_username = driver[2]
                driver_password = driver[3]
                driver_number = driver[4]
                driver_currentloc = driver[6]
                driver_vehicle = driver[7]
                found = True

        if found == False:
            print('No driver near your location')
        elif found == True:
            print('Driver found,heading your way !')
            openfile2 = open('vehicle info.txt', 'r')
            for line in openfile2:
                line = line.strip()
                line = line.split(',')
                if line[0] == driver_username:
                    username = line[0]
                    vehicle_number = line[1]
                    vehicle_color = line[2]
                    vehicle_name = line[3]
                    vehicle_type = line[4]
                    vehicleobj = car(username, vehicle_number, vehicle_name, vehicle_color)
                    driverobj = Driver(driver_number, driver[5], driver_ID, driver_name, vehicleobj, driver_username,
                                       driver_password)
                    print('driver', driverobj)
                    fare = self.calculate_fare(vehicleobj, driver_username)
                    filename = customer_username + '.txt'
                    userfile = open(filename, 'a')
                    bookingdata = driver_name + ',' + vehicle_type + ',' + vehicle_name + ',' + vehicle_number + ',' + str(
                        self.fare) + ',' + self.payment_type
                    userfile.write(bookingdata + '\n')
                    userfile.close()
                    print('Your ride has been booked')
                    driverobj.increment_trips()
                    openfile.close()
                    userfile.close()
                    return (driverobj, vehicleobj)

    def calculate_fare(self, vehicleobj, driver_username):
        rateperkm = int(vehicleobj.get_rate_per_km())
        distance = int(self.distance)
        tip = customerobj.tip()
        self.fare = (rateperkm * distance) + tip
        print('Estimated fare for your trip is : ', self.fare, ' including tip of ', tip)
        self.payment_type = input('Do you want to make your paymnet by cash or credit card')
        if self.payment_type == 'cash':
            cashobj = cash_payment(self.payment_type)
            cashobj.make_payment(self.fare)
            walletobj = wallet(driver_username)
            walletobj.deposit(self.fare)
        elif self.payment_type == 'card':
            cardobj = credit_card(self.payment_type)
            cardobj.make_payment(self.fare)
            walletobj = wallet(driver_username)
            walletobj.deposit(self.fare)
        return (self.fare)

    def book_bike(self, customer_username):
        openfile = open('driver.txt', 'r')
        found = False
        driver = None
        driver_name = None
        driver_ID = None
        driver_username = None
        driver_password = None
        driver_password = None
        driver_number = None
        driver_currentloc = None
        driver_vehicle = None
        for line in openfile:
            line = line.strip('\n')
            line = line.split(',')

            if self.pickup == line[6] and line[7] == 'bike':
                driver = line
                driver_ID = driver[0]
                driver_name = driver[1]
                driver_username = driver[2]
                driver_password = driver[3]
                driver_number = driver[4]
                driver_currentloc = driver[6]
                driver_vehicle = driver[7]
                found = True

        if found == False:
            print('No driver near your location')
        elif found == True:
            print('Driver found,heading your way !')
            openfile2 = open('vehicle info.txt', 'r')
            for line in openfile2:
                line = line.strip()
                line = line.split(',')
                if line[0] == driver_username:
                    username = line[0]
                    vehicle_number = line[1]
                    vehicle_color = line[2]
                    vehicle_name = line[3]
                    vehicle_type = line[4]
                    vehicleobj = bike(username, vehicle_number, vehicle_name, vehicle_color)
                    driverobj = Driver(driver_number, driver[5], driver_ID, vehicle_name, vehicleobj, driver_username,
                                       driver_password)
                    fare = self.calculate_fare(vehicleobj, driver_username)
                    filename = customer_username + '.txt'
                    userfile = open(filename, 'a')
                    bookingdata = driver_name + ',' + vehicle_type + ',' + vehicle_name + ',' + vehicle_number + ',' + str(
                        self.fare) + ',' + self.payment_type
                    userfile.write(bookingdata + '\n')
                    userfile.close()
                    print('Your ride has been booked')
                    driverobj.increment_trips()
                    openfile.close()
                    userfile.close()

                    return (driverobj, vehicleobj)

    def book_rickshaw(self, customer_username):
        openfile = open('driver.txt', 'r')
        found = False
        driver = None
        driver_name = None
        driver_ID = None
        driver_username = None
        driver_password = None
        driver_password = None
        driver_number = None
        driver_currentloc = None
        driver_vehicle = None
        for line in openfile:
            line = line.strip('\n')
            line = line.split(',')

            if self.pickup == line[6] and line[7] == 'rickshaw':
                driver = line
                driver_ID = driver[0]
                driver_name = driver[1]
                driver_username = driver[2]
                driver_password = driver[3]
                driver_number = driver[4]
                driver_currentloc = driver[6]
                driver_vehicle = driver[7]
                found = True

        if found == False:
            print('No driver near your location')
            return(None, None)
        elif found == True:
            print('Driver found,heading your way !')
            openfile2 = open('vehicle info.txt', 'r')
            for line in openfile2:
                line = line.strip()
                line = line.split(',')
                if line[0] == driver_username:
                    username = line[0]
                    vehicle_number = line[1]
                    vehicle_color = line[2]
                    vehicle_name = line[3]
                    vehicle_type = line[4]
                    vehicleobj = rickshaw(username, vehicle_number, vehicle_name, vehicle_color)
                    driverobj = Driver(driver_number, driver[5], driver_ID, driver_name, vehicleobj, driver_username,
                                       driver_password)
                    fare = self.calculate_fare(vehicleobj, driver_username)
                    filename = customer_username + '.txt'
                    userfile = open(filename, 'a')
                    bookingdata = driver_name + ',' + vehicle_type + ',' + vehicle_name + ',' + vehicle_number + ',' + str(
                        self.fare) + ',' + self.payment_type
                    userfile.write(bookingdata + '\n')
                    userfile.close()
                    print('Your ride has been booked')
                    driverobj.increment_trips()
                    openfile.close()
                    userfile.close()

                    return (driverobj, vehicleobj)

    '''def driver_info(self):
        print("Driver's information:")
        print("Name:",driver[1])
        print("Contact Number ",driver[6])
        print("Car registration number")'''

    def get_distance(self):
        return self.distance


class payment():
    def __init__(self, payment_type):
        self.payment_type = payment_type

    def get_payment_type(self):
        return self.payment_type


def make_payment(fare):
    print('Payment of total', fare, 'made by cash')


class cash_payment(payment):
    def __init__(self, payment_type):
        super().__init__(payment_type)

    def make_payment(self, fare):
        print('Payment of total :', fare, 'made by cash')


class credit_card(payment):
    def __init__(self, payment_type):
        super().__init__(payment_type)

    def make_payment(self, fare):
        print('Payment of total :', fare, 'made by card')


class wallet():
    def __init__(self, username):
        self.total = 0
        self.username = username

    def previous_total(self):
        filename = self.username + '_' + 'transactions' + '.txt'
        openfile = open(filename, 'a')
        readfile = open(filename, 'r')
        transactions = []
        prev_total = 0
        for line in readfile:
            transactions.append(line)
            if len(transactions) > 0:
                line = transactions[-1]
                line = line.strip('\n')
                line = line.split(',')
                prev_total = line[-1]
        openfile.close()
        readfile.close()
        return prev_total

    def deposit(self, amount):
        filename = self.username + '_' + 'transactions' + '.txt'
        openfile = open(filename, 'a')
        self.total = int(self.previous_total())
        self.total += amount
        amount = '+' + str(amount)  # converting amount to string and adding sign
        transaction = username + ',' + amount + ',' + str(self.total)
        openfile.write(transaction + '\n')
        print('Money deposited successfully')

    def withdraw(self, amount):
        print(self.username)
        filename = self.username + '_' + 'transactions' + '.txt'
        openfile = open(filename, 'a')
        self.total = int(self.previous_total())
        self.total = self.total - amount
        amount = '-' + str(amount)
        transaction = self.username + ',' + amount + ',' + str(self.total)
        openfile.write(transaction + '\n')
        print('Money is withdrawn successfully')


def find(file, data, index):
    openfile = open(file, 'r')
    for line in openfile:
        line = line.strip()
        line = line.split(',')
        if line[index] == data:
            return line


customerobj = None
valid = False
while valid == False:
    user_name = ''
    password = ''
    print(' Do you want to :')
    print('1. Log in')
    print('2. Sign up ')
    print('3.Exit App')
    choice = int(input('Enter : '))
    if choice != 3:
        user_name = input('Enter username : ')
        password = input('Enter Password : ')
    if choice == 1:
        print('Do you want to login as : ')
        print('1.Customer')
        print('2.Driver')
        user_type = int(input('Enter your choice : '))
        if user_type == 1:
            userobj = user(user_name, password)
            found = userobj.signin('customer')
            if found == False:
                print('User not found, sign up or try again')
                valid = False
            else:
                line = find('customer.txt', user_name, 2)
                name = line[1]
                username = line[2]
                passsword = line[3]
                number = line[4]
                customerobj = customer(name, username, password, number)
                # valid=True
                exit_customer = 'n'
                while exit_customer == 'n':
                    print('Do u want to : ')
                    print('1.Book a ride')
                    print('2.View booking history')
                    print('3.View profile')
                    print('4.Transaction history')

                    choice = int(input('Enter choice'))
                    if choice == 1:
                        pickup = input('Enter your pickup location')
                        dropoff = input('Enter your dropoff location ')
                        distance = input('Distance travelled ')
                        bookingobj = booking(pickup, dropoff, distance)
                        objects = customerobj.book_ride(bookingobj)
                        if  objects!=None:
                            driverobj = objects[0]
                            vehicleobj = objects[1]
                            cancel = input('Do you want to cancel your ride?(y/n)')
                            if cancel == 'y':
                                customerobj.cancel_ride()
                            exit_customer = input("Do you want to logout (y/n)")

                    elif choice == 2:
                        customerobj.view_booking_history()
                        exit_customer = input("Do you want to exit logout (y/n)")
                    elif choice == 3:
                        customerobj.display(user_type)
                        exit_customer = input("Do you want to exit logout (y/n)")
                    elif choice == 4:
                        customerobj.transaction_history()
                        exit_customer = input("Do you want to exit logout (y/n)")





        elif user_type == 2:
            vtype = None
            vnumber = None
            vname = None
            vcolor = None
            number = None
            trips = None
            ID = None
            name = None
            vehicleobj = None
            email = None
            userobj = user(user_name, password)
            found = userobj.signin('driver')
            if found == False:
                print('User not found, sign up or try again')
                valid = False
            else:
                # valid=True

                openfile = open('driver.txt', 'r')
                vopenfile = open('vehicle info.txt', 'r')
                for line in openfile:
                    line = line.strip('\n')
                    line = line.split(',')
                    if user_name == line[2]:
                        number = line[4]
                        trips = line[5]
                        name = line[1]
                        ID = line[0]
                        email = line[2]
                        password = line[3]
                openfile.close()
                for line in vopenfile:
                    line = line.strip('\n')
                    line = line.split(',')
                    if user_name == line[0]:
                        vnumber = line[1]
                        vname = line[2]
                        vcolor = line[3]
                        vtype = line[-1]
                vopenfile.close()


                if vtype == 'car':
                    vehicleobj = car(user_name, vnumber, vname, vcolor)
                elif vtype == 'bike':
                    vehicleobj = bike(user_name, vnumber, vname, vcolor)
                elif vtype == 'rickshaw':
                    vehicleobj = rickshaw(user_name, vnumber, vname, vcolor)
                driverobj = Driver(number, trips, ID, name, vehicleobj, email, password)
                print(driverobj)
                exit_driver = 'n'
                while exit_driver == 'n':
                    print('Do you want to :')
                    print('1. View transaction history')
                    print('2. Change Vehicle ')
                    print('3. Edit Profile  ')
                    print('4. Withdraw from wallet')
                    print('5. View Profile')
                    choice = int(input('Enter choice: '))
                    if choice == 1:
                        driverobj.transaction_history()
                        exit_driver = input("Do you want to exit logout(y/n)")
                    elif choice == 2:
                        driverobj.change_vehicle()
                        exit_driver = input("Do you want to exit logout (y/n)")
                    elif choice == 3:
                        driverobj.edit_profile()
                        exit_driver = input("Do you want to exit logout (y/n)")
                    elif choice == 4:
                        driverobj.withdraw_money()
                        exit_driver = input("Do you want to logout (y/n)")
                    elif choice == 5:
                        driverobj.view_profile()
                        exit_driver = input("Do you want to logout (y/n)")



    elif choice == 2:
        userobj = user(user_name, password)
        print('Do you want to sign up as : ')
        print('1.Customer')
        print('2.Driver')
        vehicleobj = None
        vehicle_type = ''
        signup=None

        user_type = int(input('Enter your choice : '))
        if user_type == 1:
            signup= userobj.signup('customer', vehicleobj, vehicle_type)
            valid=False
        elif user_type == 2:
            vehicle_type = input('Enter the type of your vehicle ')
            print('main:', vehicle_type)

            vehicle_number = input('Enter your vehicle registeration number ')
            vehicle_color = input('Enter the color of your vehicle ')
            vehicle_name = input('Enter the model name of your vehicle ')
            if vehicle_type == 'car':
                rate_per_km = 20
                carobj = car(user_name, vehicle_number, vehicle_color, vehicle_name)
                signup = userobj.signup('driver', carobj, vehicle_type)
                valid=False
            elif vehicle_type == 'bike':
                rate_per_km = 8
                bikeobj = bike(user_name, vehicle_number, vehicle_color, vehicle_name)
                signup = userobj.signup('driver', bikeobj, vehicle_type)
                valid=False
            elif vehicle_type == 'rickshaw':
                rate_per_km = 13
                rickshawobj = rickshaw(user_name, vehicle_number, vehicle_color, vehicle_name)
                signup = userobj.signup('driver', rickshawobj, vehicle_type)
                valid=False
            else:
                print('Invalid vehicle type')
                valid = False
        else:
            print('Invalid option try again')
            openfile = None
    else:
        print('App exited')
        valid = True
