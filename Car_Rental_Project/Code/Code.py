from tkinter import *
from tkinter import messagebox
import sqlite3

#create tkinter window
root = Tk()

root.title("Car Rental")

root.geometry("305x250")
root['background'] = '#23272A'

#connect to the DB
conn = sqlite3.connect("CarRental.db")
print("Connected to DB successfully")

#create a cursor
add_book_c = conn.cursor()


def customers(Name, Phone):
	insertconn = sqlite3.connect("CarRental.db")
	insert_cur = insertconn.cursor()
	
	insert_cur.execute("INSERT INTO CUSTOMERS(Name, Phone) VALUES(:Name, :Phone)",
						{
							"Name": Name,
							"Phone": Phone
						})
	#commits any changes to the DB if any other connections are open					
	insertconn.commit()
	insertconn.close()

#define input query
def vehicles(VehicleID, Description, Year, Type, Category):
    insertconn = sqlite3.connect("CarRental.db")

    insert_cur = insertconn.cursor()

    insert_cur.execute("INSERT INTO VEHICLE VALUES(:VehicleID, :Description, :Year, :Type, :Category)",
                       {
                           "VehicleID": VehicleID,
                           "Description": Description,
                           "Year": Year,
                           "Type": Type,
                           "Category": Category,
                       })

    # commits any changes to the DB if any other connections are open
    insertconn.commit()
    insertconn.close()
	
def rentals(CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, Returned):
	insertconn = sqlite3.connect("CarRental.db")
	insert_cur = insertconn.cursor()
	
	#iq_cur.execute("SELECT * FROM RENTAL JOIN VEHICLE ON (VehicleID) WHERE CustID = ?", (CustID.get(),))
	insert_cur.execute("SELECT DISTINCT RENTAL.VehicleID FROM RENTAL WHERE Returned = 0 AND PaymentDate = 'NULL'")
	
	Unavailable = insert_cur.fetchall()
		
	for i in range(0, len(Unavailable)):
		result = Unavailable[i][0]
		if(result == VehicleID):
			print("Vehicle is currently unavailable.")
			return
			
	insert_cur.execute("INSERT INTO RENTAL VALUES(:CustID, :VehicleID, :StartDate, :OrderDate, :RentalType, :Qty, :ReturnDate, :TotalAmount, :PaymentDate, :Returned)",
						{
							"CustID": CustID,
							"VehicleID": VehicleID,
							"StartDate": StartDate,
							"OrderDate": OrderDate,
							"RentalType": RentalType,
							"Qty": Qty,
							"ReturnDate": ReturnDate,
							"TotalAmount": TotalAmount,
							"PaymentDate": PaymentDate,
							"Returned": Returned
						})
	#commits any changes to the DB if any other connections are open					
	insertconn.commit()
	insertconn.close()
	
def returns(Name, VehicleID, ReturnDate, RentalType, Qty, PaymentDate):	
	insertconn = sqlite3.connect("CarRental.db")
	insert_cur = insertconn.cursor()
	
	#iq_cur.execute("SELECT * FROM RENTAL JOIN VEHICLE ON (VehicleID) WHERE CustID = ?", (CustID.get(),))
	insert_cur.execute("SELECT DISTINCT RENTAL.VehicleID FROM RENTAL WHERE Returned = 0 AND PaymentDate = 'NULL'")
	
	Unavailable = insert_cur.fetchall()
	
	Vehicles = []
	
	if(len(Unavailable) == 0):
		print("No vehicles are currently being rented.")
		return
	
	for i in range(0, len(Unavailable)):
		result = Unavailable[i][0]
		Vehicles.append(result)
		
	if VehicleID not in Vehicles:
		print("Information is not correct, please try again.")
		return
		
	insert_cur.execute("SELECT DISTINCT RENTAL.CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, Returned FROM RENTAL JOIN CUSTOMERS ON (RENTAL.CustID) WHERE CUSTOMERS.Name = ? AND VehicleID = ? AND ReturnDate = ? AND RentalType = ? AND Qty = ?", (Name, VehicleID, ReturnDate, RentalType, Qty))
		
	Results = insert_cur.fetchall()
	
	if(PaymentDate == ''):
		print("Please enter a valid Payment Date")
		return
		
	if(len(Results) == 0):
		print("Information is not correct, please try again.")
		return
	elif(Results[0][8] != 'NULL' and Results[0][9] != 0):
		print("Information is not correct, please try again.")
		return
		
	CustID = Results[0][0]	
	TotalAmount = Results[0][7]
	
	#print(Results)
	#print(f"CustID: {CustID} VehicleID: {VehicleID} ReturnDate: {ReturnDate} RentalType: {RentalType} Qty: {Qty} TotalAmount: {TotalAmount}")
	
	insert_cur.execute("UPDATE RENTAL SET Returned = 1, PaymentDate = ? WHERE CustID = ? AND VehicleID = ? AND ReturnDate = ? AND RentalType = ? AND Qty = ? AND TotalAmount = ?", (PaymentDate, CustID, VehicleID, ReturnDate, RentalType, Qty, TotalAmount))
	text = "Total Amount: " + str(TotalAmount)
	messagebox.showinfo("Total Amount", text)
	insertconn.commit()
	insertconn.close()
	
def customer_search(CustID, Name):
	insertconn = sqlite3.connect("CarRental.db")
	insert_cur = insertconn.cursor()
	
	output = ''
	if(CustID == '' and Name == ''):
		insert_cur.execute('''SELECT CustomerID AS 'Customer ID', CustomerName, SUM(RentalBalance) AS 'Remaining Balance'
							  FROM vRentalInfo
							  GROUP BY CustomerID
							  ORDER BY CustomerID Asc''')	
		Results = insert_cur.fetchall()

		for i in range(0, len(Results)):
			output += f'Customer ID: {Results[i][0]} | Name: {Results[i][1]}\nTotal Amount Owed: ${Results[i][2]}.00\n\n'	
			
		messagebox.showinfo("Search Results", output)
		
	elif (Name == ''):
		insert_cur.execute('''SELECT CustomerID AS 'Customer ID', CustomerName, SUM(RentalBalance) AS 'Remaining Balance'
							  FROM vRentalInfo
							  WHERE CustomerID = ?
							  GROUP BY CustomerID
							  ORDER BY CustomerID Asc''',(CustID,))
		Results = insert_cur.fetchall()
		if len(Results) == 0:
			messagebox.showinfo("Search Results", 'Nothing was found, please check your information and try again.')
		else:
			output += f'Customer ID: {Results[0][0]} | Name: {Results[0][1]}\nTotal Amount Owed: ${Results[0][2]}.00'
			messagebox.showinfo("Search Results", output)
	
	else:
		insert_cur.execute('''SELECT CustomerID AS 'Customer ID', CustomerName, SUM(RentalBalance) AS 'Remaining Balance'
							  FROM vRentalInfo
							  GROUP BY CustomerID
							  ORDER BY CustomerID Asc''')
		Results = insert_cur.fetchall()
		Names = []
		
		for i in range(0, len(Results)):
			Names.append(Results[i][1])
		matching = [s for s in Names if Name in s]
		
		if len(matching) == 0:
			messagebox.showinfo("Search Results", 'Nothing was found, please check your information and try again.')
		else:
			insert_cur.execute('''SELECT CustomerID AS 'Customer ID', CustomerName, SUM(RentalBalance) AS 'Remaining Balance'
								  FROM vRentalInfo
								  WHERE CustomerName = ?
								  GROUP BY CustomerID
								  ORDER BY CustomerID Asc''',(matching[0],))
								  
			Results = insert_cur.fetchall()
			output += f'Customer ID: {Results[0][0]} | Name: {Results[0][1]}\nTotal Amount Owed: ${Results[0][2]}.00'
			messagebox.showinfo("Search Results", output)
		  
		
	insertconn.close()

def vehicle_search(VehicleID, Description):
	insertconn = sqlite3.connect("CarRental.db")
	insert_cur = insertconn.cursor()
	
	output = ''
	if(VehicleID == '' and Description == ''):
		insert_cur.execute('''SELECT VIN, Vehicle AS Description, AVG(OrderAmount/TotalDays) AS 'Average Daily Price'
							  FROM vRentalInfo
							  GROUP BY VIN
							  ORDER BY "Average Daily Price" Asc''')	
		Rentals = insert_cur.fetchall()
		RentalID = []
		RentalAvg = []
		
		for i in range(0, len(Rentals)):
			RentalID.append(Rentals[i][0])
			RentalAvg.append(int(Rentals[i][2])) 
		
		insert_cur.execute('''SELECT VehicleID, Description
							  FROM VEHICLE''')
							  
		Results = insert_cur.fetchall()
		Vehicles = []
		Desc = []
		
		for i in range(0, len(Results)):
			if Results[i][0] not in Vehicles:
				Vehicles.append(Results[i][0])
				Desc.append(Results[i][1])
		
		for i in range(0, len(RentalID)):
			if RentalID[i] in Vehicles:
				output += f'VIN: {Rentals[i][0]} | Description: {Rentals[i][1]} | Average Daily Price: ${RentalAvg[i]}.00\n'	
				
		for i in range(0, len(Vehicles)):
			output += f'VIN: {Vehicles[i]} | Description: {Desc[i]} | Average Daily Price: Non-Applicable\n'
		
		messagebox.showinfo("Search Results", output)
	elif(VehicleID == ''):
		insert_cur.execute(f'''SELECT VIN, Vehicle, AVG(OrderAmount/(TotalDays)) AS DailyPrice 
							  FROM vRentalInfo 
							  WHERE Vehicle 
							  LIKE '%{Description}%' ''')
							  
		Results = insert_cur.fetchall()
		
		if Results[0][0] == None:
			messagebox.showinfo("Search Results", 'No search results found, check your information and try again.')	
			return
		
		number = int(Results[0][2])
		output += f'VIN: {Results[0][0]} | Description: {Results[0][1]} | Average Daily Price: ${number}.00\n'
		messagebox.showinfo("Search Results", output)
	elif(Description == ''):
		insert_cur.execute('''SELECT VIN, Vehicle, AVG(OrderAmount/(TotalDays)) AS DailyPrice 
							  FROM vRentalInfo 
							  WHERE VIN = ? ''', (VehicleID,))
							  
		Results = insert_cur.fetchall()
		if Results[0][0] == None:
			messagebox.showinfo("Search Results", 'No search results found, check your information and try again.')	
			return
		
		number = int(Results[0][2])
		output += f'VIN: {Results[0][0]} | Description: {Results[0][1]} | Average Daily Price: ${number}.00\n'
		messagebox.showinfo("Search Results", output)  
							  
		Results = insert_cur.fetchall()
	if (VehicleID != '' and Description != ''):
		insert_cur.execute('''SELECT VIN, Vehicle, AVG(OrderAmount/(TotalDays)) AS DailyPrice 
						FROM vRentalInfo 
						WHERE VIN = ? AND Vehicle = ?''',
						(VehicleID, Description,))
				  
		Results = insert_cur.fetchall()
		if Results[0][0] == None:
			messagebox.showinfo("Search Results", 'No search results found, check your information and try again.')	
			return
		
		number = int(Results[0][2])
		output += f'VIN: {Results[0][0]} | Description: {Results[0][1]} | Average Daily Price: ${number}.00\n'
		messagebox.showinfo("Search Results", output)
		
	insertconn.close()
	
def clear_text(text_boxes):
	for box in text_boxes:
		box.delete(0, END)

def customers_menu():

	top = Toplevel()
	top.geometry("400x150")
	top['background'] = '#23272A'
	top.title("Customer Menu")
	
	#Text Boxes
	Name = Entry(top, width = 30)
	Name.grid(row = 1, column = 1, padx = 20)

	Phone = Entry(top, width = 30)
	Phone.grid(row = 2, column = 1, padx = 20)

	#Labels
	Name_label = Label(top, text = "Name: ")
	Name_label.grid(row = 1, column = 0)
	Name_label.config(bg = '#23272A', fg = 'white')

	Phone_label = Label(top, text = "Phone: ")
	Phone_label.grid(row = 2, column = 0)
	Phone_label.config(bg = '#23272A', fg = 'white')
	#lamba is used to pass arguments
	cust_btn = Button(top, text = "Add Record into the DB", command = lambda: [customers(Name.get(), Phone.get()), clear_text([Name, Phone])], bg = '#4E5D94', fg = 'white', bd = 0)
	cust_btn.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)

def vehicles_menu():

	top = Toplevel()
	top.geometry("400x150")
	top['background'] = '#23272A'
	top.title("Vehicles Menu")
	
	#Text Boxes
	VehicleID = Entry(top, width = 30)
	VehicleID.grid(row = 1, column = 1, padx = 20)

	Description = Entry(top, width = 30)
	Description.grid(row = 2, column = 1, padx = 20)
	
	Year = Entry(top, width = 30)
	Year.grid(row = 3, column = 1, padx = 20)
	
	Type = Entry(top, width = 30)
	Type.grid(row = 4, column = 1, padx = 20)
	
	Category = Entry(top, width = 30)
	Category.grid(row = 5, column = 1, padx = 20)

	#Labels
	VehicleID_label = Label(top, text = "VehicleID: ")
	VehicleID_label.grid(row = 1, column = 0)
	VehicleID_label.config(bg = '#23272A', fg = 'white')

	Description_label = Label(top, text = "Description: ")
	Description_label.grid(row = 2, column = 0)
	Description_label.config(bg = '#23272A', fg = 'white')
	
	Year_label = Label(top, text = "Year: ")
	Year_label.grid(row = 3, column = 0)
	Year_label.config(bg = '#23272A', fg = 'white')
	
	Type_label = Label(top, text = "Type: ")
	Type_label.grid(row = 4, column = 0)
	Type_label.config(bg = '#23272A', fg = 'white')
	
	Category_label = Label(top, text = "Category: ")
	Category_label.grid(row = 5, column = 0)
	Category_label.config(bg = '#23272A', fg = 'white')
	
	#lamba is used to pass arguments
	cust_btn = Button(top, text = "Add Record into the DB", command = lambda: [vehicles(VehicleID.get(), Description.get(), Year.get(), Type.get(), Category.get()), clear_text([VehicleID, Description, Year, Type, Category])], bg = '#4E5D94', fg = 'white', bd = 0)
	cust_btn.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)
	
def rentals_menu():

	top = Toplevel()
	top.geometry("355x300")
	top['background'] = '#23272A'
	top.title("Rentals Menu")
	
	#Text Boxes
	CustID = Entry(top, width = 30)
	CustID.grid(row = 1, column = 1, padx = 20)

	VehicleID = Entry(top, width = 30)
	VehicleID.grid(row = 2, column = 1, padx = 20)
	
	StartDate = Entry(top, width = 30)
	StartDate.grid(row = 3, column = 1, padx = 20)
	
	OrderDate = Entry(top, width = 30)
	OrderDate.grid(row = 4, column = 1, padx = 20)
	
	RentalType = Entry(top, width = 30)
	RentalType.grid(row = 5, column = 1, padx = 20)
	
	Qty = Entry(top, width = 30)
	Qty.grid(row = 6, column = 1, padx = 20)
	
	ReturnDate = Entry(top, width = 30)
	ReturnDate.grid(row = 7, column = 1, padx = 20)
	
	TotalAmount = Entry(top, width = 30)
	TotalAmount.grid(row = 8, column = 1, padx = 20)
	
	PaymentDate = Entry(top, width = 30)
	PaymentDate.grid(row = 9, column = 1, padx = 20)

	#Labels
	CustID_label = Label(top, text = "CustID: ")
	CustID_label.grid(row = 1, column = 0)
	CustID_label.config(bg = '#23272A', fg = 'white')

	VehicleID_label = Label(top, text = "Vehicle ID: ")
	VehicleID_label.grid(row = 2, column = 0)
	VehicleID_label.config(bg = '#23272A', fg = 'white')
	
	StartDate_label = Label(top, text = "Start Date: ")
	StartDate_label.grid(row = 3, column = 0)
	StartDate_label.config(bg = '#23272A', fg = 'white')
	
	OrderDate_label = Label(top, text = "Order Date: ")
	OrderDate_label.grid(row = 4, column = 0)
	OrderDate_label.config(bg = '#23272A', fg = 'white')
	
	RentalType_label = Label(top, text = "Rental Type: ")
	RentalType_label.grid(row = 5, column = 0)
	RentalType_label.config(bg = '#23272A', fg = 'white')
	
	Qty_label = Label(top, text = "Qty: ")
	Qty_label.grid(row = 6, column = 0)
	Qty_label.config(bg = '#23272A', fg = 'white')
	
	ReturnDate_label = Label(top, text = "Return Date: ")
	ReturnDate_label.grid(row = 7, column = 0)
	ReturnDate_label.config(bg = '#23272A', fg = 'white')
	
	TotalAmount_label = Label(top, text = "Total Amount: ")
	TotalAmount_label.grid(row = 8, column = 0)
	TotalAmount_label.config(bg = '#23272A', fg = 'white')
	
	PaymentDate_label = Label(top, text = "Payment Date: ")
	PaymentDate_label.grid(row = 9, column = 0)
	PaymentDate_label.config(bg = '#23272A', fg = 'white')
	

	return_btn = Button(top, text = "Add Record into DB", command = lambda: [rentals(CustID.get(), VehicleID.get(), StartDate.get(), OrderDate.get(), RentalType.get(), Qty.get(), ReturnDate.get(), TotalAmount.get(), PaymentDate.get(), 0), clear_text([CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate])], bg = '#4E5D94', fg = 'white', bd = 0)
	return_btn.grid(row = 11, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)
	
def returns_menu():

	top = Toplevel()
	top.geometry("380x200")
	top['background'] = '#23272A'
	top.title("Returns Menu")
	
	#Text Boxes
	Name = Entry(top, width = 30)
	Name.grid(row = 1, column = 1, padx = 20)

	VehicleID = Entry(top, width = 30)
	VehicleID.grid(row = 2, column = 1, padx = 20)
	
	ReturnDate = Entry(top, width = 30)
	ReturnDate.grid(row = 3, column = 1, padx = 20)
	
	RentalType = Entry(top, width = 30)
	RentalType.grid(row = 4, column = 1, padx = 20)
	
	Qty = Entry(top, width = 30)
	Qty.grid(row = 5, column = 1, padx = 20)
	
	PaymentDate = Entry(top, width = 30)
	PaymentDate.grid(row = 6, column = 1, padx = 20)

	#Labels
	Name_label = Label(top, text = "Name: ")
	Name_label.grid(row = 1, column = 0)
	Name_label.config(bg = '#23272A', fg = 'white')
	
	VehicleID_label = Label(top, text = "Vehicle ID: ")
	VehicleID_label.grid(row = 2, column = 0)	
	VehicleID_label.config(bg = '#23272A', fg = 'white')

	ReturnDate_label = Label(top, text = "Return Date: ")
	ReturnDate_label.grid(row = 3, column = 0)
	ReturnDate_label.config(bg = '#23272A', fg = 'white')
	
	RentalType_label = Label(top, text = "Rental Type: ")
	RentalType_label.grid(row = 4, column = 0)
	RentalType_label.config(bg = '#23272A', fg = 'white')
	
	Qty_label = Label(top, text = "Qty: ")
	Qty_label.grid(row = 5, column = 0)
	Qty_label.config(bg = '#23272A', fg = 'white')
	
	PaymentDate_label = Label(top, text = "Payment Date: ")
	PaymentDate_label.grid(row = 6, column = 0)
	PaymentDate_label.config(bg = '#23272A', fg = 'white')
	
	#lamba is used to pass arguments
	cust_btn = Button(top, text = "Update Record in DB", command = lambda: [returns(Name.get(), VehicleID.get(), ReturnDate.get(), RentalType.get(), Qty.get(), PaymentDate.get()), clear_text([Name, VehicleID, ReturnDate, RentalType, Qty, PaymentDate])], bg = '#4E5D94', fg = 'white', bd = 0)
	cust_btn.grid(row = 7, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)
	
def customer_search_menu():

	top = Toplevel()
	top.geometry("300x100")
	top['background'] = '#23272A'
	top.title("Customer Search Menu")
	
	#Text Boxes
	
	CustID = Entry(top, width = 30)
	CustID.grid(row = 1, column = 1, padx = 20)

	Name = Entry(top, width = 30)
	Name.grid(row = 2, column = 1, padx = 20)

	#Labels
	CustID_label = Label(top, text = "Customer ID: ")
	CustID_label.grid(row = 1, column = 0)
	CustID_label.config(bg = '#23272A', fg = 'white')
	
	Name_label = Label(top, text = "Name: ")
	Name_label.grid(row = 2, column = 0)	
	Name_label.config(bg = '#23272A', fg = 'white')
	
	#lamba is used to pass arguments
	cust_btn = Button(top, text = "Search", command = lambda: [customer_search(CustID.get(), Name.get()), clear_text([CustID, Name])], bg = '#4E5D94', fg = 'white', bd = 0)
	cust_btn.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)
	
def vehicle_search_menu():

	top = Toplevel()
	top.geometry("300x100")
	top['background'] = '#23272A'
	top.title("Vehicle Search Menu")
	
	#Text Boxes
	
	VehicleID = Entry(top, width = 30)
	VehicleID.grid(row = 1, column = 1, padx = 20)

	Description = Entry(top, width = 30)
	Description.grid(row = 2, column = 1, padx = 20)

	#Labels
	VehicleID_label = Label(top, text = "VIN: ")
	VehicleID_label.grid(row = 1, column = 0)
	VehicleID_label.config(bg = '#23272A', fg = 'white')
	
	Description_label = Label(top, text = "Description: ")
	Description_label.grid(row = 2, column = 0)
	Description_label.config(bg = '#23272A', fg = 'white')
	
	#lamba is used to pass arguments
	cust_btn = Button(top, text = "Search", command = lambda: [vehicle_search(VehicleID.get(), Description.get()), clear_text([VehicleID, Description])], bg = '#4E5D94', fg = 'white', bd = 0)
	cust_btn.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)
	
#define GUI components for tkinter root window
#Customer Button
customer_menu = Button(root, text="Add Customer", command = customers_menu, bg = '#4E5D94', fg = 'white', bd = 0)
customer_menu.grid(row = 1, column = 0, columnspan = 2, pady = 10, ipadx = 99)

#Vehicle Button
customer_menu = Button(root, text="Add Vehicle", command = vehicles_menu, bg = '#4E5D94', fg = 'white', bd = 0)
customer_menu.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 106)

#Rental Button 
rental_menu = Button(root, text="Add a Rental", command = rentals_menu, bg = '#4E5D94', fg = 'white', bd = 0)
rental_menu.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 104)

#Return Button
rental_menu = Button(root, text="Return a Vehicle", command = returns_menu, bg = '#4E5D94', fg = 'white', bd = 0)
rental_menu.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 95)

#Search Customer Button
rental_menu = Button(root, text="Customer Search", command = customer_search_menu, bg = '#4E5D94', fg = 'white', bd = 0)
rental_menu.grid(row = 5, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 93)

#Search Vehicle Button
rental_menu = Button(root, text="Vehicle Search", command = vehicle_search_menu, bg = '#4E5D94', fg = 'white', bd = 0)
rental_menu.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 93)

#executes my window
root.mainloop()