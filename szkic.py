# Notation:
#   slices:
#     U -> Top slice
#     u -> Inner top slice (e.g. 2nd slice from the top -- inner means 2nd row in)
#     d -> Inner bottom slice
#     D -> Bottom slice
#     L -> Left slice
#     l -> Inner left slice
#     r -> Inner right slice
#     R -> Right slice
#     F -> Front slice
#     f -> Inner front slice
#     b -> Inner back slice
#     B -> Back slice
#   directions:
#     L -> rotate slice left (applies to U,u,d,D slices)
#     R -> rotate slice right (U,u,d,D slices)
#     U -> rotate slice up (L,l,r,R slices)
#     D -> rotate slice down (L,l,r,R slices)
#     C -> rotate slice clockwise (F,f,b,B slices)
#     A -> rotate slice anticlockwise (F,f,b,B slices)
#   move right / up   / clock.     =  1
#        left  / down / anticlock. = -1 or 0

def rotateGen(Dictionary):
    """ Popraw polecenia po wykonaniu danego obrotu.
    Funkcja przyjmuje słownik, którym tłumaczy się pary
      (Krawędź, IlośćOperacji)
    na nowe, odpowiadające sytuacji po obrocie.
    Zwraca domknięcie. Do użycia wraz z map/2"""
    def rotate((Slice, Ops)):
        lowSlice = Slice.lower()
        if lowSlice not in Dictionary:
            return (Slice, Ops)
        (NSlice, NOps) = Dictionary[lowSlice]
        if Slice.isupper():
            NSlice = NSlice.upper()
        NOps = NOps * Ops
        return (NSlice, NOps)
    return rotate

def pivot_rotateL(List):
    return map(rotateGen( {'f': ('l', -1), 'l': ('b', 1), 'b': ('r', -1), 'r': ('f', 1)} ), List)
def pivot_rotateR(List):
    return map(rotateGen( {'f': ('r', 1), 'r': ('b', -1), 'b': ('l', 1), 'l': ('f', -1)} ), List)
def pivot_rotateU(List):
    return map(rotateGen( {'f': ('u', -1), 'u': ('b', 1), 'b': ('d', -1), 'd': ('f', 1)} ), List)
def pivot_rotateD(List):
    return map(rotateGen( {'f': ('d', 1), 'd': ('b', -1), 'b': ('u', 1), 'u': ('f', -1)} ), List)

# helpers
def pivot_rotateRL(List, Dir):
    if Dir == 1: return pivot_rotateR(List)
    else if Dir == 2: return pivot_rotateR(pivot_rotateR(List)) # a bit of ugliness here...
    else: return pivot_rotateL(List)
def pivot_rotateUD(List, Dir):
    if Dir == 1: return pivot_rotateU(List)
    else if Dir == 2: return pivot_rotateU(pivot_rotateU(List)) # ...and here
    else: return pivot_rotateD(List)

def operate(List, State, Lego): # Elevator, Spinner, Flipper
    # List is the list of operations pending
    # State is the state of "przewracacz". 0 means normal, 1 means "flipped"
    # Lego is robot controlling class
    
    while len(List) > 0:
        (Slice, Ops) = List[0]
        Tail = List[1:]

        if Slice.lower() == 'b': # back
            if State == 0:
                Lego.elevator_grab(4)
                Lego.flipper_flip()
                Lego.elevator_grab(0)
            # State = 1
            Lego.flipper_unflip(); (List, State) = (pivot_rotateD(List), 0)
            continue

        if Slice.lower() == 'f': # front
            if State == 1:
                Lego.elevator_grab(4)
                Lego.flipper_unflip()
                Lego.elevator_grab(0)
            # State = 0
            Lego.flipper_flip(); (List, State) = (pivot_rotateU(List), 1)
            continue

        if Slice.lower() == 'l': # left
            Lego.elevator_grab(4)
            Lego.spinner_rotate(1-State); (List, State) = (pivot_rotateRL(List, 1-State), State)
            Lego.elevator_grab(0)
            Lego.flipper_flip(1-State); (List, State) = (pivot_rotateUD(List, 1-State), 1-State)
            continue

        if Slice.lower() == 'r': # right
            Lego.elevator_grab(4)
            Lego.spinner_rotate(State); (List, State) = (pivot_rotateRL(List, State), State)
            Lego.elevator_grab(0)
            Lego.flipper_flip(1-State); (List, State) = (pivot_rotateUD(List, 1-State), 1-State)
            continue

        if Slice.lower() == 'd': # bottom
            Ops = Ops % 4
            if Ops == 0:
                (List, State) = (Tail, State)
                continue
            Lego.elevator_grab(2 + Slice.isupper())
            Lego.spinner_rotate(-Ops); (List, State) = (pivot_rotateRL(List, -Ops), State)
                # spinner_rotate must accept values in range -3..3 and perform well
            if Slice.islower():
                Lego.elevator_grab(3)
                Lego.spinner_rotate(Ops); (List, State) = (pivot_rotateRL(List, Ops), State)
            continue

        if Slice.lower() == 'u': # up
            Ops = Ops % 4
            if Ops == 0:
                (List, State) = (Tail, State)
                continue
            Lego.elevator_grab(1 + Slice.islower())
            Lego.spinner_rotate(Ops)
            if Slice.islower():
                Lego.elevator_grab(1)
                Lego.spinner_rotate(-Ops)
            continue

        raise UndefinedOperation(Slice, Ops, List, State, Lego)

class UndefinedOperation(Exception):
    def __init__(self, Slice, Ops, List, State, Lego):
        pass
    def __str__(self):
        pass
