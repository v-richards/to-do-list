income = int(input())

if income <= 15527:
    rate = 0
elif 15528 <= income <= 42707:
    rate = 0.15
elif 42708 <= income <= 132406:
    rate = 0.25
else:
    rate = 0.28

print(f"The tax for {income} is {int(rate * 100)}%. That is {round(income * rate)} dollars!")
