from datetime import time, timedelta, date, datetime
import math
import random
from time import sleep

class Human:
    """This holds all the user information"""

    # initialize the user with a name, current stress level and at Home
    def __init__(self, name, stress):
        self.name = name
        self.stress = stress
        self.loc = Places("Home", 25, 25)

    # gets the name of the user
    def get_name(self):
        return str(self.name)

    # gets the current stress level of the user
    def get_stress(self):
        return float(self.stress)

    # Sets the stress level by adjusting the current stress level
    def set_stress(self, adjust):
        self.stress -= adjust

    # Checks in the user is out of energy
    def stress_over(self):
        if self.stress <= 0:
            return True
        else:
            return False

    # Get the current location of the user
    def get_loc(self):
        return self.loc.name

    # Sets the location of the user. uses the Places object.
    def set_loc(self, loc, x, y):
        self.loc = Places(loc, x, y)

    # get the x, y coordinate of the user.
    def get_loc_coord(self):
        return self.loc.get_location()


class WorldTime:
    """Holds and controls the time for the user"""

    # set the current time of the user. Accepts a string separated by space.
    # HH MM
    def __init__(self, times):
        time_list = times.split(" ")
        self.current_time = time(hour=int(time_list[0]), minute=int(time_list[1]))

    # set the end time of the errands. Accepts a string separated by space.
    # HH MM
    def set_end_time(self, times):
        time_list = times.split(" ")
        self.end_time = time(hour=int(time_list[0]), minute=int(time_list[1]))

    # gets the current time
    def get_current_time(self):
        return str(self.current_time)

    # adjusts the time based on the input in minutes.
    # Converts time to datatime type then adjusts with a
    # timedelta and converts back to time type.
    def adjust_time(self, mins):
        delta = timedelta(minutes=mins)
        temp = datetime.combine(date(1, 1, 1), self.current_time)
        self.current_time = (temp + delta).time()

    # Check if the current time is greater than the set end time
    def is_over(self):
        if self.current_time > self.end_time:
            return True
        else:
            return False


class Places:
    """This is the location of the places in the users world"""

    # Initialize the name and coordinates of a place
    def __init__(self, name, x, y):
        self.name = name
        self.x_loc = float(x)
        self.y_loc = float(y)

    # gets the name if the place
    def get_name(self):
        return self.name

    # get the x,y coordinated of the place
    def get_location(self):
        return self.x_loc, self.y_loc


class Activities:
    """This contains the activities that a user can perform through the day"""

    # initialize the activities with its name, time anf stress required to perform the activity
    def __init__(self, name, time_taken, stress_required):
        self.name = name
        self.time_taken = time_taken
        self.stress_required = float(stress_required)

    # gets the name of activities.
    def get_name(self):
        return self.name

    # gets the time taken for activities.
    def get_time_taken(self):
        return self.time_taken

    # gets the stress required to perform the activity
    def get_stress(self):
        return self.stress_required


class Car:
    """This hold the users car information and
    can perform operations with the car"""

    # initialize the Car with a car name, transmission type and average speed
    def __init__(self, name, transmission, speed):
        self.name = name
        self.transmission = transmission
        self.speed = float(speed)

    # this performs the task of driving between locations.
    # Measures the distance and time taken.
    # There is a random variable to account for traffic that affect the time and stress for a drive.
    def drive(self, place_1, place_2):
        traffic = random.uniform(1.0, 1.5)  # traffic factor that affect stress and time taken to drive
        distance = ((abs(place_1[0] - place_2[0])) ** 2 +
                    abs(place_1[1] - place_2[1]) ** 2) ** 0.5
        drive_time = math.ceil((distance / self.speed) * 60 * traffic)  # time in mins

        if self.transmission.lower() == "man":
            drive_stress = math.ceil(1.35 * (drive_time / 4) * traffic)
        else:
            drive_stress = math.ceil((drive_time / 4) * traffic)

        print(f"The drive took {drive_time}mins"
              f" and reduced your energy by {drive_stress}"); sleep(0.5)
        return drive_time, drive_stress


# Initialize a few places in the world
# Make shift grid map :50 X 50 miles
p1 = Places("Home", 25, 25)
p2 = Places("Walmart", 28, 30)
p3 = Places("Target", 26, 31)
p4 = Places("Library", 8, 48)
p5 = Places("Gym", 28, 25)
p6 = Places("Popeyes", 12, 34)
p7 = Places("McDonalds", 11, 22)
p8 = Places("Red Lobster", 14, 34)
p9 = Places("Jones Park", 8, 6)
p10 = Places("Collins Courts", 10, 2)
p11 = Places("Downtown Bars", 45, 48)
p12 = Places("Ramons House", 35, 12)
p13 = Places("Spa", 45, 25)
places = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]

# Initialize a few activities for the user. Negative stress required means you gain energy back
# (name, time_taken, stress_required)
a1 = Activities("Tennis", 90, 30)
a2 = Activities("Soccer", 90, 45)
a3 = Activities("Shopping", 45, 10)
a4 = Activities("Work out", 120, 40)
a5 = Activities("Hang out", 20, 15)
a6 = Activities("Eat", 60, -12)
a7 = Activities("Bar hop", 150, 20)
a8 = Activities("Massage", 60, -30)
a9 = Activities("Study", 160, 30)
acts = [a1, a2, a3, a4, a5, a6, a7, a8, a9]

# Start the command line interface
print("----------------------------------------------------------------------")
print("This is a simulator to help run a bunch of activities through your day.")
print("   This program will help you check the feasibility of performing")
print("   a set of activities within a time period and given energy level.")
print("                        Start estimating!")
print("-----------------------------------------------------------------------\n")

# This section collect the user, world and car information.
# The loop terminates when all the vital information is collected
# If there is an error in any of the input. The program starts collecting all the information again
while True:
    user_name = input("\nWelcome! Please enter a name for your user: "); sleep(1)
    print(f"\n{user_name}. I see you want to plan out some activities for your day."); sleep(0.5)

    try:
        user_stress = float(input("\nOn a scale of 0-100 how will you describe your current energy level: "))
        if user_stress < 0 or user_stress > 100:
            raise Exception("Please enter an energy level between 0 & 100")
    except Exception as e:
        print(e)
        print(f"Enter energy level as a number. What you entered is not a valid number."
              f"\nPlease start again.")
        continue

    new_user = Human(user_name, user_stress)
    break

while True:
    print(f"\n{user_name}. Now let's get the current time."); sleep(1)
    print("Check your clock and enter the time in the format: \'HH MM\'"); sleep(0.5)
    start_time = input("Enter the current time: "); sleep(0.5)
    end_time = input("Enter time you have to be back home by (must be the same day): "); sleep(0.5)
    try:
        if end_time <= start_time:
            raise Exception("Please enter a valid end time."
                            "\nEnd time must be greater than start time.")
        if len(start_time.split()) != 2 or len(end_time.split()) != 2:
            raise Exception("Time not entered in the format \'HH MM\'")
        new_time = WorldTime(start_time)
        new_time.set_end_time(end_time)
    except Exception as e:
        print(e)
        print(f"\nLets try that again.")
        continue
    break

while True:
    print(f"\n{new_user.get_name()}, lets get your car information."); sleep(1)
    try:
        car_name = input("Whats the make of your car: "); sleep(0.5)
        car_trans = input("Is your car automatic or manual transmission (Enter: auto/man)? ").lower(); sleep(0.5)
        car_speed = int(input("Estimate the average speed of your car in mph: ")); sleep(0.5)
        if car_trans not in ["auto", "man"]:
            raise Exception("Transmission types are either auto or man")
        if car_speed <= 0:
            raise Exception("Speed must be greater than zero"
                            "\nPlease enter a valid speed.")
    except Exception as e:
        print(e)
        print(f"\nLets try that again.")
        continue

    new_car = Car(car_name, car_trans, car_speed)

    print("\n\nThe simulator starts here. Type \'help\' for list of commands"); sleep(1)
    break

# The program starts now with various commands
# The main command to perform activities is 'go'
while True:
    command = input(f"\n{new_user.get_name()} enter a command: ").lower()
    if command == "help":
        print(f"\nHey {new_user.get_name()}, the time is {new_time.get_current_time()}"); sleep(0.5)
        print("\nBelow is the list of possible commands:")
        print(" - places: to display a list of places the user can go to")
        print(" - activities: to display a list of activities the user can perform")
        print(" - go: to drive to a location and perform activities")
        print(" - quit: to end the simulator")

    elif command == "quit":
        print("\n GOOD BYE!!!!!!")
        break

    elif command == "places":
        # Prints out the list of Places available
        print("\nHere is a list of the places the user can go to:")
        for i in places:
            print(f" - {i.name}")

    elif command == "activities":
        # Prints out the list of Activities available
        print("\nHere is a list of the activities the user can do:")
        for i in acts:
            print(f" - {i.name}")

    elif command == "go":
        print(f"\nYou are currently at {new_user.get_loc()}. Where do you want to drive to perform your activity?: "); sleep(0.5)
        drive_to = input("- ")
        # Checks if the place is the list of available places to go to.
        # Then it performs the drive to the new location and adjusts the time and energy of the user
        if drive_to.lower() in [x.name.lower() for x in places]:
            for x in places:
                if x.get_name().lower() == drive_to.lower():
                    drive_to_obj = x
                    drive_time_stress = new_car.drive(new_user.get_loc_coord(), drive_to_obj.get_location())
                    new_user.set_stress(drive_time_stress[1])
                    new_time.adjust_time(drive_time_stress[0])

                    a = drive_to_obj.get_name()
                    b = drive_to_obj.get_location()
                    new_user.set_loc(a, b[0], b[1])
            # Checks if the energy is exhausted
            if new_user.stress_over():
                print(f"\n\n{new_user.get_name()} your are out of energy!"); sleep(0.5)
                print("The sequence of activities you tried to perform cannot be completed based on your stress level.")
                print("Please try again."); sleep(0.5)
                break
            # Checks if we are out of time
            if new_time.is_over():
                print(f"\n\n{new_user.get_name()} your are out of time!"); sleep(0.5)
                print("The sequence of activities you tried to perform cannot be completed in the given time frame.")
                print("Please try again."); sleep(0.5)
                break

        else:
            print(f"\n{drive_to} is not a valid place in this program. Can enter the "
                  f"command \'places\' to show the list of places you can go to"); sleep(0.5)

        print(f"\nYou are currently at {new_user.get_loc()}. What activity do you want to perform?: "); sleep(0.5)
        active_to = input("- ")
        # Checks if the activity is in the available activities
        # Then it performs the activity and adjusts the time and energy of the user
        if active_to.lower() in [x.name.lower() for x in acts]:
            for x in acts:
                if x.get_name().lower() == active_to.lower():
                    active_to_obj = x
                    new_user.set_stress(active_to_obj.get_stress())
            # Checks if the energy is exhausted
            if new_user.stress_over():
                print(f"\n\n{new_user.get_name()} your are out of energy!"); sleep(0.5)
                print("The sequence of activities you tried to perform cannot be completed based on your stress level.")
                print("Please try again."); sleep(0.5)
                break
            # Checks if we are out of time
            if new_time.is_over():
                print(f"\n\n{new_user.get_name()} your are out of time!"); sleep(0.5)
                print("The sequence of activities you tried to perform cannot be completed in the given time frame.")
                print("Please try again."); sleep(0.5)
                break

            print(f"\nThe time is {new_time.get_current_time()} and you have {new_user.get_stress()} energy left")

        else:
            print(f"\n{active_to} is not a valid activity in this program. Can enter the "
                  f"command \'activities\' to show the list of activities you can go do"); sleep(0.5)

    else:
        print("\nPlease enter a valid command. Type \'help\' for the list of commands."); sleep(0.5)
        continue
