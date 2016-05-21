while(1):
    try:
        x=int (input('enter your age'))
    except ValueError:
        print('try again')
    else:
        break
print(x)
