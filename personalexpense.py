expenses = []
while True:
    print("-------- Personal Expense Tracker ------")
    print("press 1 to Add expenses")
    print("press 2 to view expenses")
    print("press 3 to view total spending ")
    print("press 4 category wise spending")
    print("press 5 to exit")

    choice = int(input("enter your choice: "))

    if choice == 1:
            #add expenses
            Date = input("enter the date: ")
            Amount = float(input("enter the amount: "))
            category = input("enter the category: ")
            rec = {"Date": Date,
                "Amount": Amount,
                "Category" : category}
            
            expenses.append(rec)

    elif choice == 2 :
            #view expenses
            if len(expenses) == 0:
                print("no expenses. ")
            for rec in expenses:
                result =print("Date", rec["Date"] , "Amount", rec["Amount"] , "Category" , rec["Category"])

    elif choice == 3 :
            #view total spending
            total = 0

            for rec in expenses:
                total += rec["Amount"]
            
            result = print("total: " , total)

    elif choice == 4:
            #display category wise spending
            d = {"c1" : 0, "c2" : 0, "c3" : 0 }

            for rec in expenses :
                d[rec["Category"]] += rec["Amount"]
            
            print("Category" , "Amount")

            for k , v in d.items():
                print(k , v)
            
    else: 
            result = print("THANK YOU!! ")
            break


    
    
