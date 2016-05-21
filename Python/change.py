c = float(input("Change Calculator\nCost: $"))
p = float(input("\nReceived: $"))
v = p - c

amount = round(v * 100)

valueList = (10000, 5000, 2000, 1000, 500, 100, 25, 10, 5, 1)
labelList = (" $100 Bills", " $50 Bills", " $20 Bills", " $10 Bills",
             " $5 Bills", " $1 Bills", " Quarters", " Dimes", " Nickels", " Pennies")
labelListSing = (" $100 Bill", " $50 Bill", " $20 Bill", " $10 Bill",
                 " $5 Bill", " $1 Bill", " Quarter", " Dime", " Nickel", " Penny")
for i, value in enumerate(valueList):
    count = int(amount / value)
    amount = (amount - count * value)
    if count == 1:
        print(count, labelListSing[i])
    if count > 1:
        print(count, labelList[i])
