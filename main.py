import time
import random

class CoffeeMachine:
    WATER_MAX_STOCK = 500
    COFFEE_MAX_STOCK = 100
    MILK_MAX_STOCK = 300

    def __init__(self):
        self.coffee_options = ["espresso", "americano", "latte", "cappuccino"]
        self.size_options = ["small", "medium", "large"]

        self.inserted_money = 0
        self.change = 0
        self.account_balance = random.randint(15000, 1000000)

        self.name = ""

        self.stock = {
            "water": self.WATER_MAX_STOCK,
            "milk": self.MILK_MAX_STOCK,
            "coffee": self.COFFEE_MAX_STOCK
        }

        base_ingredients = {
            "espresso": {"water": 30, "milk": 0, "coffee": 7},
            "latte": {"water": 30, "milk": 150, "coffee": 7},
            "cappuccino": {"water": 30, "milk": 100, "coffee": 7},
            "americano": {"water": 120, "milk": 0, "coffee": 7}
        }

        self.options = {
            coffee: {
                "ingredients": ingredients,
                "price": price
            }
            for coffee, ingredients, price in [
                ("espresso", base_ingredients["espresso"], 10000),
                ("latte", base_ingredients["latte"], 30000),
                ("cappuccino", base_ingredients["cappuccino"], 20000),
                ("americano", base_ingredients["americano"], 25000)
            ]
        }

    def check_stock(self, coffee):
        isEnough = True
        for item in self.options[coffee]["ingredients"]:
            if self.options[coffee]["ingredients"][item] >= self.stock[item]:
                print(f"\nSorry, {item} stock not enough.")
                isEnough = False
        
        return isEnough

    def set_multiplier(self, coffee_type, size):
        if size == "small": return

        size_multipliers = {
            'medium': (1.2, 1.5),
            'large': (1.5, 2)
        }

        if size in size_multipliers:
            stock_multipliers, price_multipliers = size_multipliers[size]

        for ingredient in self.options[coffee_type]["ingredients"]:
            self.options[coffee_type]["ingredients"][ingredient] *= stock_multipliers
        
        self.options[coffee_type]["price"] *= price_multipliers

    def refill(self):
        time.sleep(5)
        self.stock["water"] = self.WATER_MAX_STOCK
        self.stock["milk"] = self.MILK_MAX_STOCK
        self.stock["coffee"] = self.COFFEE_MAX_STOCK

    def calculate_cash_denomination(self):
        cash_denominations = [1, 2, 5, 10, 20, 50, 100]
        count = 0
        print("Choose the cash denomination: ", end=" ")
        for denom in cash_denominations:
            if count % 3 == 0:
                print() 
            print(f"{count + 1}. Rp{denom}000\t", end=" ")
            count += 1
        
        try:
            option = int(input("\nOption: "))
        except:
            print("\nSomething went wrong. Please only enter a valid integer.")
            return False

        if option < 1 or option > 4:
            print("\nInvalid cash denomination.")
            return False
        
        self.inserted_money += (cash_denominations[option - 1] * 1000)
        return True
    
    def calculate_coin_denomination(self):
        coin_denominations = [1, 2, 5, 10]
        count = 0
        print("Choose the coin denomination: ", end=" ")
        for denom in coin_denominations:
            if count % 2 == 0:
                print() 
            print(f"{count + 1}. Rp{denom}00\t", end=" ")
            count += 1

        try:
            option = int(input("\nOption: "))
        except:
            print("\nSomething went wrong. Please only enter a valid integer.")
            return False
        
        if option < 1 or option > 4:
            print("\nInvalid coin denomination.")
            return False

        self.inserted_money += (coin_denominations[option - 1] * 100)

        return True

    def calculate_change(self, coffee_price):
        print(f"\nCoffee price: Rp{coffee_price}")
        print(f"Total money inserted: Rp{self.inserted_money}")

        coin_denominations = [100, 200, 500, 1000]
        coin_denominations.sort(reverse=True)
        coin_map = [0 for i in range(len(coin_denominations))]
        
        self.change = self.inserted_money - coffee_price
        change = self.inserted_money - coffee_price
        isChange = False

        for i in range(len(coin_denominations)):
            while change - coin_denominations[i] >= 0:
                change -= coin_denominations[i]
                coin_map[i] += 1
                isChange = True

        if not isChange:
            print("\nNo change.")
            return
        
        print("\nChange")
        for i in range(len(coin_map)):
            if coin_map[i] != 0:
                print(f"- {coin_map[i]} coin(s) of Rp{coin_denominations[i]}")
        print()

    def handle_payment(self, method, coffee_type):
        print("-" * 25)
        if method == 1:
            while self.inserted_money < self.options[coffee_type]["price"]:
                coffee_price = self.options[coffee_type]["price"]
                print(f"\nCoffee price: Rp{coffee_price}")
                print(f"Total money inserted: Rp{self.inserted_money}")

                option = int(input("\n1. Insert coin\n2. Insert cash\nOption: "))
                print()

                if option == 1:
                    if not self.calculate_coin_denomination():
                        continue
                elif option == 2:
                    if not self.calculate_cash_denomination():
                        continue
            self.calculate_change(self.options[coffee_type]["price"])
        elif method == 2:
            if self.options[coffee_type]["price"] > self.account_balance:
                print("Insufficient Balance. Please use another payment method.")
                return False
            else:
                self.account_balance -= self.options[coffee_type]["price"]
        
        print("Payment Successful.")
        print("-" * 25)
        return True
    
    def dispense_order(self, coffee_type, coffee_size):
        # Generate receipt details
        coffee_name = coffee_type.capitalize()
        size = coffee_size.capitalize()
        price = self.options[coffee_type]["price"]

        # Print receipt
        print("=" * 30)
        print("|        COFFEEMAKER         |")
        print("=" * 30)
        print(f"| Name: {self.name:<21}|")
        print(f"| Order: {coffee_name:<20}|")
        print(f"| Size: {size:<21}|")
        print(f"| Price: Rp{price:<18}|")
        print(f"| Change: Rp{self.change:<17}|")
        print("=" * 30)
        print("Thank you for your order! Enjoy your coffee!\n")

    def run(self):
        while(True):
            self.inserted_money = 0
            self.change = 0
            print("=" * (len("COFFEE VENDING MACHINE") + 4))
            print("| COFFEE VENDING MACHINE |")
            print("=" * (len("COFFEE VENDING MACHINE") + 4))

            self.name = input("Name: ")
            coffee_type = input("Coffee Types\n- Espresso\n- Americano\n- Latte\n- Cappuccino\nOption: ").lower()

            if coffee_type not in self.coffee_options:
                print("\nERROR: Invalid coffee type.\n")
                continue

            print("-" * 25)
            coffee_size = input("Size\n- Small\n- Medium\n- Large\nOption: ").lower()
            
            if coffee_size not in self.size_options:
                print("\nERROR: Invalid size.\n")
                continue

            self.set_multiplier(coffee_type, coffee_size)

            if self.check_stock(coffee_type):
                print("-" * 25)

                try:
                    payment_option = int(input("Payment Options\n1. Cash & coins\n2. Cards\nOption (1 or 2): "))
                except:
                    print("\nSomething went wrong. Please only enter a valid integer.")
                    continue
                
                if payment_option != 1 and payment_option != 2:
                    print("\nInvalid payment option.\n")
                    continue

                if self.handle_payment(payment_option, coffee_type):
                    print("\nPREPARING ORDER")
                    time.sleep(5)
                    self.dispense_order(coffee_type, coffee_size)
                
            else:
                print("RESTOCKING, PLEASE WAIT 5 SECS")
                self.refill()
                print("RESTOCKING COMPLETED.\n")
                continue
            
            multiple_order = input("Would you like to make another order? (Y/n): ").lower()

            if multiple_order == 'n':
                break
        
coffeeMachine = CoffeeMachine()
coffeeMachine.run()