def get_int(prompt):
    while True:
        try: 
            n = int(input(prompt))
            if n>0 and n<9:
                return n
        except ValueError:
            pass
def main():
    x = get_int("x, a positive integer between 1 and 8: ")
    
    for i in range(x):
        print(" "*(x-i-1), end="")
        print("#"*(i+1))    
main()
