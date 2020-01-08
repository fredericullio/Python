from random import shuffle

class Card:
    """
    name type -> string
    suit type -> string
    value -> integer
    index -> integer
    """
    def __init__(self, name, suit, value, index):
        self.value = value
        self.suit = suit
        self.name = name
        self.index = index

class Deck:
    """
    contents type -> list of card objects

    """
    def __init__(self):  
        self.contents = []
    
    def construct(self, lim=1):
        
        spades = ['Spades']*13
        hearts = ['Hearts']*13
        diamonds = ['Diamonds']*13
        clubs = ['Clubs']*13
        values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        names = ['Two','Three','Four', 'Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
        for index in range(1, lim+1):         
            spade_list = [Card(a, b, c, d) for a, b, c, d in zip(names, spades, values, [index]*13)]
            heart_list = [Card(a, b, c, d) for a, b, c, d in zip(names, hearts, values, [index]*13)]
            diamond_list = [Card(a, b, c, d) for a, b, c, d in zip(names, diamonds, values, [index]*13)]
            club_list = [Card(a, b, c, d) for a, b, c, d in zip(names, clubs, values, [index]*13)]
            deck = spade_list + heart_list + diamond_list + club_list
            self.contents += deck
            shuffle(self.contents)

class Hand:
    """
    contents type -> list of card objects
    bet type -> integer
    total type -> integer
    """
    def __init__(self, contents, bet, total = 0, active = True): 
        self.contents = contents
        self.bet = bet
        self.total = total
        self.active = active
        
    def add_card(self, *args):
        checking = True
        for i in args:
            self.contents.append(i)
        while checking:
            self.total = 0
            for i in self.contents:
                self.total += i.value
            if self.total>21:
                for i in self.contents:
                    if i.value == 11:
                        i.value = 1
                        break
                else:
                    checking=False
            else:
                checking=False
                
    def betting(self, name, account):
        while True:
            try:
                self.bet = int(input(f"{name}, please, place your bet"))
            except:
                print("This probably wasn't a number. Please, try again.")
                continue
            if self.bet > account:
                print("Your bet excedes your account balance. Please, try lowering it.")
            else:
                account -= self.bet
                return account
    
    def show(self, name, index=""):
        print(f"{name}'s hand nr {index}:\n")
        for card in self.contents:
            print(f"{card.name} of {card.suit}")
        if name == "Dealer":
            print(f"\nTotal: {self.total}\n")
        else:  
            print(f"\nTotal: {self.total}\n\nBet: {self.bet}")

class Player:
    """
    name type -> string
    hands -> list of hand objects
    account - integer
    insurance - integer
    """
    def __init__(self, name = "Bob", hands = [], account = 0, insurance = 0):
        self.name = name
        self.hands = hands
        self.account = account
        self.insurance = insurance
        
        
    def add(self, amount):
        self.account = self.account + amount
        
    def subtract(self, amount):
        self.account = self.account - amount
        
    def acc_show(self):
        print(f"{self.name}'s account balance: {self.account}\n")
    
    def who_are_you(self):
        self.name = input("Please, enter your player's name.")
        self.account = 500
        hand = Hand([], 0)
        self.hands.append(hand)
        return self
    
    def splitting(self, card1, card2):
        checking = True
        while checking:
                for hand in self.hands:
                    if self.account >= hand.bet:
                        if hand.contents[0].value == hand.contents[1].value:
                            while True:
                                answer = input(f"{self.name}, would you like to split your hand nr \
{self.hands.index(hand)+1}? Y/N").upper()
                                if answer == "Y":
                                    split = Hand([], bet = hand.bet)
                                    split.add_card(hand.contents.pop(), card1)  
                                    self.hands.append(split)                                 
                                    hand.add_card(card2) 
                                    self.subtract(hand.bet)
                                    break

                                elif answer == "N":
                                    break
                                else:
                                    print("Please, answer Y or N")
                                    continue
                                    break
                else:
                    checking = False
                        
    def ensuring(self, dealer):
        if dealer.contents[0].value == 11 and self.hands[0].total < 21:
            ens = True
            while ens:
                answer = input(f"{self.name}, would you like to place an insurance bet? Y/N").upper()
                if answer == "Y":  
                    while True:
                        try:
                            self.insurance = int(input(f"{self.name}, how much would you like to bet?"))
                        except:
                            print("Please, enter a number.")
                            continue     
                        if self.insurance > self.account:
                            print("Your bet excedes your account balance. Try lowering it.")
                            continue
                        elif self.insurance > self.hands[0].bet/2:
                            print("Your insurance cannot excede half of your original bet.")
                        else:
                            self.account = self.account - self.insurance
                            ens = False
                            break
                elif answer == "N":
                    ens = False
                else:
                    print("Please, answer Y or N.")
                    continue

class BlackJack:
    """
    dealer type = Hand object
    players type = list of Player objects
    deck type - Deck object
    statement type - string
    dont_show type - boolean
    """
    def __init__(self, dealer = Hand([], None, 0), players = [], deck = Deck(), statement = "", dont_show = True):
        self.dealer = dealer
        self.players = players
        self.deck = deck
        self.statement = statement
        self.dont_show = dont_show
    
    def players_list(self):
        print("Players' list:")
        for index, player in enumerate(self.players, 1):
            if player.hands[0].bet == 0:
                print(f"{index}. {player.name}")
            else:
                print(f"{index}. {player.name}, bet {player.hands[0].bet}")
    
    def create_players(self):
        adding = True
        while adding:
            player = Player(None, [])
            self.players.append(player.who_are_you())
            while True:
                answer = input("Another player Y/N?").upper()
                self.players_list()
                
                if answer == "Y":
                    break
                elif answer == "N":
                    adding = False
                    break
                else:
                    print("Please, answer Y or N.")
    
    def bj_check(self):
        if self.dealer.total == 21:
            self.statement += "DEALER'S BLACKJACK!\n"
            self.dont_show = False
            for player in self.players:    
                for hand in player.hands:
                    if hand.total == 21:
                        self.statement += f"\n{player.name.upper()}'S BLACKJACK!"
                        player.add(hand.bet)         
                    elif player.insurance > 0:
                            player.account += player.insurance
                            self.statement += f"\n{player.name}, your insurance has been paid!"
            return True
        else:
            for player in self.players:
                for hand in player.hands:
                    if hand.total == 21:
                        self.statement += f"\n{player.name.upper()}'S BLACKJACK!"
                        player.add(3*hand.bet)
                        self.display()
                        hand.active = False
            return False
    
    def display(self):
 
        print(f"GAME INFO:\n{self.statement}\n\n####################################\n")
        if self.dont_show:
            print(f"DEALER'S FIRST CARD: {self.dealer.contents[0].name} of {self.dealer.contents[0].suit}\n")
        else:
            self.dealer.show("Dealer", 1)
       
        for player in self.players:
            print("####################################\n")
            for hand in player.hands: 
                hand.show(player.name, player.hands.index(hand)+1)
            player.acc_show()
            print("####################################")
    
    def players_turn(self, player):
        
        for hand in player.hands:
            if hand.active == True:
                choosing = True
                while choosing:

                    self.display()
                    choice = input(f"{player.name}, press H to hit, S to stand, \
D to double down or X to surrender for your hand nr {player.hands.index(hand)+1}").upper()

                    if choice == "H":

                        hand.add_card(self.deck.contents.pop())
                        while hand.total < 21:
                            self.display()
                            answer = input(f"{player.name}, hit or stand? H/S").upper()

                            if answer == "H":
                                hand.add_card(self.deck.contents.pop())

                            elif answer == "S":
                                choosing = False
                                break

                            else:
                                print("Please, answer H or S.")
                        else:       
                            if hand.total > 21:
                                self.statement += f"\n{player.name.upper()}'S HAND NR \
{player.hands.index(hand)+1} HAS GONE BUST!"

                                self.display()
                                hand.active = False
                                choosing = False

                            else:
                                self.display()
                                choosing = False

                    elif choice == "S":
                        choosing = False

                    elif choice == "D":
                        if player.account>=hand.bet:
                            player.subtract(hand.bet)
                            hand.bet = 2*hand.bet
                            hand.add_card(self.deck.contents.pop())

                            if hand.total > 21:
                                self.statement += f"\n{player.name.upper()}'S \
HAND NR {player.hands.index(hand)+1} HAS GONE BUST!"

                                self.display()
                                hand.active = False
                                choosing = False

                            else:
                                self.display()
                                choosing = False
                        else:
                            print(f"{player.name}, sorry, your account balance doesn't allow to double down.")

                    elif choice == "X":
                        player.add(hand.bet/2)
                        hand.active = False
                        self.display()
                        choosing = False

                    else:
                        print("Please, enter valid input.")

            
    def dealers_turn(self):
        self.dont_show = False
        
        while self.dealer.total < 17:
            self.dealer.add_card(self.deck.contents.pop())
        if self.dealer.total > 21:
            self.statement += "\nTHE HOUSE HAS GONE BUST!"
            for player in self.players:
                for hand in player.hands:
                    player.account += 2*hand.bet
        
    def comparisons(self, player):
        if self.dealer.total<=21:
            for hand in player.hands:
                if hand.active == True:
                    if self.dealer.total < hand.total:
                        self.statement += f"\n{player.name.upper()}'S HAND NR \
{player.hands.index(hand)+1} HAS WON!"

                        player.account += 2*hand.bet
                    elif self.dealer.total == hand.total:
                        self.statement += f"\n{player.name.upper()}'S HAND NR \
{player.hands.index(hand)+1} - TIE!"

                        player.account += hand.bet
                    else:
                        self.statement += f"\n{player.name.upper()}'S HAND NR \
{player.hands.index(hand)+1} HAS LOST!"
            
    def gameplay(self):
        game_on = True
        print("Welcome to BlackJack Ultimate Experience!")
        self.create_players()
        
        
        while game_on:
            self.deck.construct()
            self.dealer.add_card(self.deck.contents.pop(), self.deck.contents.pop())
            for player in self.players:
                for hand in player.hands:
                    hand.add_card(self.deck.contents.pop(), self.deck.contents.pop())

            while True:
                for player in self.players:
                    for hand in player.hands:
                        player.account = hand.betting(player.name, player.account)
                        self.players_list()
                
                self.display()
                
                for player in self.players:
                    player.ensuring(self.dealer)
                    player.splitting(self.deck.contents.pop(), self.deck.contents.pop())
                if self.bj_check():
                    break

                for player in self.players:
                    self.players_turn(player)

                self.dont_show = False
                self.dealers_turn()
                for player in self.players:
                    self.comparisons(player)
                break
            
            self.display()
            input("Press enter to continue")
            
            for player in self.players:
                if player.account>0:
                    player.acc_show()
                    while True:
                        answer = input(f"{player.name}, would you like to continue playing? Y/N").upper()
                        if answer == "Y":
                            player.hands, player.insurance = [Hand([], 0)], 0
                            break
                        elif answer == "N":
                            print(f"Thanks for playing, {player.name}!")
                            self.players.remove(player)
                            break
                        else:
                            print("Please, answer Y or N.")
                else:
                    print("Sorry, your account balance reached 0. Thanks for playing!")
                    self.players.remove(player)
                            
            
            if self.players == []:
                print("Thanks for playing!")
                game_on = False
            else:
                self.dealer = Hand([], None, 0)
                self.statement = ""
                self.dont_show = True

bj  = BlackJack()
bj.gameplay()
