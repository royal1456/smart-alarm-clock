from func_timeout import *
read_inp=True
def input_with_timeout():
     print("perfectly..Listening")
     inp=input()
     print("runn signal,",inp)
     return inp
while read_inp:
    print(read_inp, " was")
    from inputimeout import inputimeout, TimeoutOccurred
    try:
        something = inputimeout(prompt='>>', timeout=5)
    except TimeoutOccurred:
        something = 'something'
    print("entered value", something, type(something))