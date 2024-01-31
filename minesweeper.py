import random as r
FancyGrid=0

def gen_empty_field(b: int, h: int)->list: #breedte en hoogte
    return [[0]*b for _ in range(h)]
    
def print_field(f: list):
    for i in range(len(f)):
        for j in f[i]:
            print(j, end=" ")
        print()

def print_field_fancy(f: list):
    for i in range(len(f)):
        for j in f[i]:
            if j ==0:
                print(chr(9450), end="")
            else:
                print(chr(9311+j), end="")
        print()
            
#print_field(gen_empty_field(breedte, hoogte))

def place_mine(f: list): #places one mine in the field
    x , y = r.randint(0,hoogte-1) , r.randint(0,breedte-1)
    if f[x][y]==9:
        return place_mine(f)
    f[x][y]=9
    coords=[]#all coords around placed mine
    for i in range(-1,2):
        for j in range(-1,2):
            if 0<=x+i<=hoogte-1 and 0<=y+j<=breedte-1:
                coords+=[(x+i,y+j)]
    coords.remove((x,y))
    for i in coords:
        if f[i[0]][i[1]] !=9: #Check if no mine in pos
            f[i[0]][i[1]]=f[ i[0] ][ i[1] ]+1
    return f


def return_value(c: tuple,f: list[list[int]]):#hulpfunc print_hidden
    global gaming
    if FancyGrid:
        if c in discovered:
            if f[ c[0] ][ c[1] ] ==9:
                gaming=False
                return "☠"
            elif f[ c[0] ][ c[1] ] ==0:
                return "⓪"
            else:
                return f'\033[{30+f[ c[0] ][ c[1] ]}m' + chr(9311+f[ c[0] ][ c[1] ]) + "\033[39m"
        else: return "Ⓧ"
    else:
        if f[ c[0] ][ c[1] ] ==9:
            gaming=False
        return f'\033[{30+f[ c[0] ][ c[1] ]}m' + str(f[ c[0] ][ c[1] ]) + "\033[39m" if c in discovered else "X" #colored


def print_hidden(f: list[list[int]]): #met g de lijst coordinaten die al gevonden zijn
    for i in range(len(f)):
        for j in range(len(f[i])):
            print(return_value( (i,j) ,f),end="")
        if FancyGrid:
            print(" "+chr(9398+i))
        else:
            print(" "+chr(65+i))
    if FancyGrid:
        print("{}".format([chr(9424+x) for x in range(len(f[0]))]).replace("', '","")[2:-2])
    else:
        print("{}".format([chr(97+x) for x in range(len(f[0]))]).replace("', '","")[2:-2])

def ask_mine():
    global discovered
    a=input("Mine:")
    if a[0].isupper() and a[1].islower():
        discovered.add((ord(a[0])-65,ord(a[1])-97))
    elif a[1].isupper() and a[0].islower():
        discovered.add((ord(a[1])-65,ord(a[0])-97))
    else:
        print("Wrong coordinate format, needs to be a capital and a lowercase letter")
        return ask_mine()

def main(): #check of aantal mines kleiner is dan h*b
    global breedte
    global hoogte
    global mines
    global discovered
    global gaming
    gaming=True
    breedte=int(input("Breedte:"))
    hoogte=int(input("Hoogte:"))
    mines=int(input("Mines:"))
    if 0<mines<breedte*hoogte-1:
        discovered=set()
    else:
        print("Too few/many mines for the field")
        quit()
    field=gen_empty_field(breedte,hoogte)
    for _ in range(mines):
        field=place_mine(field)
    while gaming: #Break om uit loop te gaan bij complete of als mine gemined wordt
        print_hidden(field)
        ask_mine()
        if len(discovered)==breedte*hoogte-mines:
            print_hidden(field)
            print("You won!")
            quit()
    print("Heh, you lost")
        





main()
