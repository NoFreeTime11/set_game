import random

"""
Every card has 4 attributes: shape, color, fill, and count.
These 4 attributes will be represented by a tuple with 4 integers
Shape: 0 = Oval, 1 = Diamond, 2 = Squiggle
Color: 0 = Green, 1 = Purple, 2 = Red
Fill: 0 = Empty, 1 = Striped, 2 = Filled
Count: 0 = 3 objects, 1 = 1 object, 2 = 2 objects

A player plays the game by forming SETs, a group of three
cards where for each attribute, each card has either
a) All the same attribute (ex: all the cards are green)
b) All different attributes (ex: one card is green, 
    another is red, and the last is purple)
"""

# Now I need to create a function that checks if a group
# of 3 cards is a SET
def set_check(card1, card2, card3):
    if card1 == card2 or card1 == card3 or card2 == card3:
        print("Duplicate found")
        return
    shape_total = (card1[0] + card2[0] + card3[0]) % 3

    color_total = (card1[1] + card2[1] + card3[1]) % 3

    fill_total = (card1[2] + card2[2] + card3[2]) % 3

    count_total = (card1[3] + card2[3] + card3[3]) % 3

    if ((shape_total, color_total, fill_total,
         count_total) == (0,0,0,0)):
        #"""
        print("This is a set:")
        print(card1)
        print(card2)
        print(card3)
        print()
        #"""
        return True
    else:
        return False

# This function makes a new, ordered deck.
def new_deck():
    deck_standard = list()
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    deck_standard.append([i, j, k, l])
    return deck_standard

# This will take a given group of cards and shuffle them.
def shuffled_deck(deck_standard):
    deck_shuffled = list()
    while len(deck_standard) > 0:
        r = random.randrange(0,len(deck_standard))
        deck_shuffled.append(deck_standard[r])
        deck_standard.pop(r)
    return deck_shuffled

# This function will sort through a group of cards and
# return a SET, if found.
def check_active_cards(current_deck):
    i = 0
    while i < len(current_deck) - 2:
        j = i + 1
        while j < len(current_deck) - 1:
            k = j + 1
            while k < len(current_deck):
                if set_check(current_deck[i], current_deck[j],
                             current_deck[k]):
                    return [current_deck[i],
                            current_deck[j],
                             current_deck[k]]
                k += 1
            j += 1
        i += 1
    return [0,0,0]


# Time to bring it together to simulate the game.
def gameplay():
    deck_standard = new_deck()
    deck_shuffled = shuffled_deck(deck_standard)
    on_table = list()
    found_sets = list()
    all_sets_found = False
    beyond12count = 0
    while not all_sets_found:
        while len(on_table) < 12 and len(deck_shuffled) > 0:
            on_table.append(deck_shuffled[0])
            deck_shuffled.pop(0)
        #"""
        print("On the table:")
        for x in on_table:
            print(x)
        print()
        #"""

        result = check_active_cards(on_table)
        setFlag = False
        if result != [0,0,0]:
            setFlag = True
            for x in range(3):
                found_sets.append(result[x])
                on_table.remove(result[x])

        if not setFlag:
            if len(deck_shuffled) == 0:
                all_sets_found = True
                continue
            for x in range(3):
                if len(deck_shuffled) > 0:
                    on_table.append(deck_shuffled[0])
                    deck_shuffled.pop(0)
            beyond12count += 1
    #"""
    print("^^ This is the remaining deck with no sets",
          end = '\n\n')
    print("Number of times there were more than 12 cards "
          "on the table: ", beyond12count, end='\n\n')
    print("Found sets:")
    for x in range(len(found_sets)):
        if x % 3 == 0:
            print("-------------")
        print(found_sets[x])
    #"""
    return len(on_table)

gameplay()
print()
print()

# This section lets me simulate a million games and keep track of how
# many times a game ends with a certain number of cards.
"""
remaining = [0,0,0,0,0,0,0]
for x in range(1000000):
    i = int(gameplay()/3)
    remaining[i] += 1
print("Percentage of games with leftover cards:")
for y in range(7):
    print((y*3), ":", (remaining[y]*100)/1000000, "%")
"""

# Now I need a function that will take two cards and tell
# me what third card I will need to finish the SET.
def complete_set(card1, card2):
    if card1 == card2:
        print("Given cards are duplicates.")
        return
    card3 = [0,0,0,0]
    for x in range(4):
        card3[x] = (2*(card1[x]+card2[x])) % 3

    print("Given cards:")
    print(card1)
    print(card2)
    print("Card to complete the set: ",card3)
    return card3

example_card1 = [random.randint(0,2),
                 random.randint(0,2),
                 random.randint(0,2),
                 random.randint(0,2)]
example_card2 = [random.randint(0,2),
                 random.randint(0,2),
                 random.randint(0,2),
                 random.randint(0,2)]
complete_set(example_card1, example_card2)

# I need a function that will take a shuffled deck and
# see how many cards it needs before it finds a SET.
def min_for_set():
    deck_standard = new_deck()
    deck_shuffled = shuffled_deck(deck_standard)
    min_hand = list()
    for x in range(3):
        min_hand.append(deck_shuffled[0])
        deck_shuffled.pop(0)

    setFlag = False
    while not setFlag:
        found_set = check_active_cards(min_hand)
        if found_set == [0,0,0]:
            if len(deck_shuffled) > 0:
                min_hand.append(deck_shuffled[0])
                deck_shuffled.pop(0)
                continue
        else:
            setFlag = True
    print("Smallest hand before a set was found:")
    for x in min_hand:
        print(x)
    print()
    return len(min_hand) - 1

# Now to run that a massive number of times to see what
# the most realistic max number of cards to get a SET is.
"""
current_max = 3
for x in range(100000):
    min_size = min_for_set()
    current_max = max(current_max, min_size)
print("Max number of cards needed before a set is "
      "found:", current_max)
"""

def count_sets(current_deck):
    set_count = 0
    i = 0
    while i < len(current_deck) - 2:
        j = i + 1
        while j < len(current_deck) - 1:
            k = j + 1
            while k < len(current_deck):
                if set_check(current_deck[i],
                             current_deck[j],
                             current_deck[k]):
                    set_count += 1
                k += 1
            j += 1
        i += 1
    return set_count

def prob_and_stat(num):

    count_total = 0
    set_total = 0
    for x in range(1000000):
        deck = shuffled_deck(new_deck())
        result = count_sets(deck[:num])
        if result > 0:
            count_total += 1
            set_total += result

    print("Probability of a SET in", num,"cards is",
          count_total/1000000)
    print("Average number of SETs in", num, "cards is",
          set_total/1000000)

# prob_and_stat(17)
