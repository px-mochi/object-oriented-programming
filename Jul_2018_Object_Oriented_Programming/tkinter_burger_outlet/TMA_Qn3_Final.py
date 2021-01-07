'''
Created on 15 Oct 2018

@author: Pei Xuan

17 October 2018: Update from previous submission on 16 October - updated button placement,
                updated clear function to reset radio buttons as well
                disabled entry widgets and radio buttons when purchase is confirmed
'''

import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext #ttk is specialized for widgets

# The rest shall be the rest of your program
class CashRegisterGUI:
    # Table Q3.1 - Create dict recording purchase details
    # Example - purchaseDetail = {"B":2,"C":1}
    purchaseDetail = {}    
    
    def __init__(self,burgDetails):
        self.burgDetails = burgDetails
        win = tk.Tk()   # Creating a Tk instance
        win.title("McBurger Pte Ltd")
        win.geometry("500x280")
        win.resizable(False, False)
        
        # Creating frames (top for radio and input, mid for buttons, bottom for scrolltext)
        topFrame = Frame(win)
        topFrame.grid(row=0, column=0, padx=5, pady =5, sticky=NSEW)
        
        
        midFrame = Frame(win)
        midFrame.grid(row=1, column=0, padx=5, sticky=NSEW)
        
        bottomFrame = Frame(win)
        bottomFrame.grid(row=2, column=0, padx=5, pady =5, sticky=NSEW)
        
        # Creating visible widgets
        #-----------START OF TOP FRAME----------
        self._BurgCode_lbl = ttk.Label(topFrame, width=20, text="Burger Code:", foreground='Black')
        self._BurgCode_lbl.grid(row=0, column=0, sticky=W)
        
        self._Qty_lbl = ttk.Label(topFrame, width=20, text="Burger Quantity:", foreground='Black')
        self._Qty_lbl.grid(row=1, column=0, sticky=W)
        
        self.BurgCode_txt = tk.StringVar
        self._BurgCode_ety = ttk.Entry(topFrame, width=60, textvariable=self.BurgCode_txt)
        self._BurgCode_ety.grid(row=0, column=1, sticky=E)
        
        self.Qty_txt = tk.StringVar
        self._Qty_ety = ttk.Entry(topFrame, width=60, textvariable=self.Qty_txt)
        self._Qty_ety.grid(row=1, column=1, sticky=E)
        #-----------END OF TOP FRAME------------
        
        #-----------START OF MIDDLE FRAME----------
        self.radValue = tk.IntVar()
        self.radValue.set(1)    # radValue == 1 is customer
        self._rButton1 = ttk.Radiobutton(midFrame, text="Customer", variable=self.radValue, value=1)
        self._rButton1.grid(row=0, column=2, sticky=W)
        self._rButton2 = ttk.Radiobutton(midFrame, text="Staff", variable=self.radValue, value=0)
        self._rButton2.grid(row=0, column=3, sticky=W)
        
        self._addPurchase_btn = ttk.Button(midFrame, width=16, text="Add to Purchase", command=self.addPurchase)
        self._addPurchase_btn.grid(row=1, column=0, padx=1, sticky=W)
        #Decided not to use bind, as it overrides tk.DISABLED
        
        self._delPurchase_btn = ttk.Button(midFrame, width=20, text="Delete Purchase Item", command=self.delPurchase)
        self._delPurchase_btn.grid(row=1, column=1, padx=1, sticky=W)
        
        self._confirmPurchase_btn = ttk.Button(midFrame, width=18, text="Confirm Purchase", command=self.confirmPurchase)
        self._confirmPurchase_btn.grid(row=1, column=2, padx=1, sticky=W)
        
        self._Clear_btn = ttk.Button(midFrame, width=18, text="Clear", command=self.clearBtn)
        self._Clear_btn.grid(row=1, column=3, padx=1, sticky=W)
        #-----------END OF MID FRAME------------
        
        
        #-----------START OF BOTTOM FRAME----------
        scrol_w, scrol_h = 59, 10
        self._scrolltxt = scrolledtext.ScrolledText(bottomFrame, width=scrol_w, height=scrol_h, wrap=tk.WORD)
        self._scrolltxt.grid(row=0, column=0, sticky=NSEW)
        self._scrolltxt.config(state=tk.DISABLED) # prevent editing of scrolledtext
        #-----------END OF BOTTOM FRAME------------
        
        
        self.startApplication()
        win.mainloop() # Get Tk into a loop
    
    def startApplication(self): # All buttons except addPurchase default as DISABLED
        self._addPurchase_btn.config(state=tk.NORMAL)
        self._delPurchase_btn.config(state=tk.DISABLED)
        self._confirmPurchase_btn.config(state=tk.DISABLED)
        self._Clear_btn.config(state=tk.DISABLED)
        
        # Enable typing in entry widgts
        self._BurgCode_ety.config(state=tk.NORMAL)
        self._Qty_ety.config(state=tk.NORMAL)
        
        # Enable radio buttons
        self._rButton1.config(state=tk.NORMAL)
        self._rButton2.config(state=tk.NORMAL)
    
    def enableButtons(self): # Enables delete, confirm, and clear buttons if there is a purchase
        self._addPurchase_btn.config(state=tk.NORMAL)
        self._delPurchase_btn.config(state=tk.NORMAL)
        self._confirmPurchase_btn.config(state=tk.NORMAL)
    
    def clearEntry(self):   # Disable scrolledtext input, and clear entry boxes
        self._scrolltxt.see(tk.END)     # scrolls to latest update
        self._scrolltxt.config(state=tk.DISABLED)
        self._BurgCode_ety.delete(0,'end')
        self._Qty_ety.delete(0,'end')
        
    def currentPurchase(self): # prints current purchase details to scrolledtext
        # Insert current purchase details into input
            self._scrolltxt.insert(tk.END,"Current purchase:\n")    # Print current purchase
            grandTotal = 0
            for key in sorted(self.purchaseDetail):
                tburgQty = self.purchaseDetail[key]
                tBurgName = self.burgDetails[key]["Name"]
                tBurgPrice = self.burgDetails[key]["Price"]
                ttotalPrice = tburgQty * tBurgPrice
                
                self._scrolltxt.insert(tk.END,\
                                   "{} x {} \t @${:.2f} = ${:.2f}\n"\
                                   .format(tburgQty,tBurgName,tBurgPrice,ttotalPrice))
                
                grandTotal += ttotalPrice
            
            self._scrolltxt.insert(tk.END,"Total = ${:.2f}\n".format(grandTotal))
            
            # Checking for staff discount
            if self.radValue.get() == 0:
                staffGrandTotal = grandTotal * 0.80 # 20% discount for staff
                self._scrolltxt.insert(tk.END,"Adjusted Total @20% (staff) = ${:.2f}\n"\
                                       .format(staffGrandTotal))
                
            self._scrolltxt.see(tk.END)     # scrolls to latest update
    
    def addPurchase(self):
        
        # Enable editing of scrolledtext for program to input data
        self._scrolltxt.config(state=tk.NORMAL)
        
        if self._BurgCode_ety.get().upper() in self.burgDetails:    # Valid burger code and quantity
            codeKey = self._BurgCode_ety.get().upper()
            if self._Qty_ety.get() == "":
                qtyValue = 1
            else:
                try:
                    qtyValue = int(self._Qty_ety.get())
                except ValueError:
                    self._scrolltxt.insert(tk.END,"Invalid burger quantity. Please input an integer.\n")
                    self.clearEntry() # Disable scrolledtext input, and clear entry boxes
                    return
            burgName = self.burgDetails[codeKey]["Name"]
            burgPrice = self.burgDetails[codeKey]["Price"]
            totalPrice = qtyValue * burgPrice
            
            # Insert newest code and quantity into input
            self._scrolltxt.insert(tk.END,\
                                   "Adding {} of {}\t @${:.2f} = ${:.2f}\n"\
                                   .format(qtyValue,burgName,burgPrice,totalPrice))
            
            
            # Collating purchase details in purchaseDetail dict
            if codeKey in self.purchaseDetail:  # If burger is already added, increase the quantity
                self.purchaseDetail[codeKey] += qtyValue
                
            else:
                self.purchaseDetail[codeKey] = qtyValue # If burger is not in current purchase, add it in
        
            
            self.currentPurchase() # prints current purchase details to scrolledtext
            
        
        elif self._BurgCode_ety.get() == "":    # If item code is blank
            self._scrolltxt.insert(tk.END,\
                                   "Please enter item code\n")
                    
        else:   # If input burger code is invalid
            burgKeys = list(self.burgDetails.keys())    # get list of valid burger codes
            self._scrolltxt.insert(tk.END,\
                                   "Please enter valid item code {}\n"\
                                   .format(burgKeys))
            
        
        self.clearEntry() # Disable scrolledtext input, and clear entry boxes
        
        # Enables delete, confirm, and clear buttons if there is a purchase
        if bool(self.purchaseDetail):
            self.enableButtons()
            
    
    def delPurchase(self):
        # Enable editing of scrolledtext for program to input data
        self._scrolltxt.config(state=tk.NORMAL)
        
        if self._BurgCode_ety.get().upper() in self.purchaseDetail:    # Valid code and quantity in current purchase
            codeKey = self._BurgCode_ety.get().upper()
            if self._Qty_ety.get() == "":
                qtyValue = self.purchaseDetail[codeKey] # select entire quantity of selected burger
            else:
                try:
                    qtyValue = int(self._Qty_ety.get())
                except ValueError:
                    self._scrolltxt.insert(tk.END,"Invalid burger quantity. Please input an integer.\n")
                    self.clearEntry() # Disable scrolledtext input, and clear entry boxes
                    return
        
            burgName = self.burgDetails[codeKey]["Name"]
            
            # adding delete info in scrolledtext
            currentBurgQty = self.purchaseDetail[codeKey]   # find out current qty of selected burgers left
            if qtyValue > currentBurgQty:
                qtyValue = currentBurgQty   # Set delete value to all selected burgers if value > qty
                
            self._scrolltxt.insert(tk.END,"Deleting {} {} from purchase\n"\
                                   .format(qtyValue,burgName))

            # Removing selected burger (if valid) and quantity from self.purchaseDetail
            self.purchaseDetail[codeKey] -= qtyValue
            if self.purchaseDetail[codeKey] < 0:
                self.purchaseDetail[codeKey] = 0
                
            
            if self.purchaseDetail[codeKey] == 0:   # Remove entry from dict if qty == 0
                del self.purchaseDetail[codeKey]
            
            # Resets buttons to default if purchase is empty
            if bool(self.purchaseDetail) == False:
                self.startApplication()
            self.currentPurchase() # prints current purchase details to scrolledtext
            
                
        elif self._BurgCode_ety.get() == "":    # If item code is blank
            self._scrolltxt.insert(tk.END,\
                                   "Please enter item code\n")
                    
        else:   # If input burger code is invalid
            burgKeys = list(self.purchaseDetail.keys())    # get list of valid burger codes
            self._scrolltxt.insert(tk.END,\
                                   "Please enter valid item code {}\n"\
                                   .format(burgKeys))
        
        
        self.clearEntry() # Disable scrolledtext input, and clear entry boxes
        
    
    def confirmPurchase(self):
        self._scrolltxt.config(state=tk.NORMAL)
        self._scrolltxt.delete(1.0,tk.END)  # Clear contents of scrolledtext
        self.currentPurchase()  # prints current purchase details to scrolledtext
        self._scrolltxt.insert(tk.END,"Purchase is confirmed\n")
        self.clearEntry() # Disable scrolledtext input, and clear entry boxes
        self._scrolltxt.config(state=tk.DISABLED)
        
        #Disable all buttons except clear button
        self._addPurchase_btn.config(state=tk.DISABLED)
        self._delPurchase_btn.config(state=tk.DISABLED)
        self._confirmPurchase_btn.config(state=tk.DISABLED)
        self._Clear_btn.config(state=tk.NORMAL)
        
        # Disable entry widgets
        self._BurgCode_ety.config(state=tk.DISABLED)
        self._Qty_ety.config(state=tk.DISABLED)
        
        # Disable radio buttons
        self._rButton1.config(state=tk.DISABLED)
        self._rButton2.config(state=tk.DISABLED)
    
    def clearBtn(self):
        # Clear contents of scrolledtext
        self._scrolltxt.config(state=tk.NORMAL)
        self._scrolltxt.delete(1.0,tk.END)
        self._scrolltxt.config(state=tk.DISABLED)
        self._Clear_btn.config(state=tk.DISABLED)   # Disable clear button
        
        # Enable radio buttons
        self._rButton1.config(state=tk.NORMAL)
        self._rButton2.config(state=tk.NORMAL)
        self.radValue.set(1)    # Reset radio button to select Customer option
        
        
        self.purchaseDetail.clear() # clear current purchase record
        
        self.startApplication() # Reset button defaults
        
        
        
def main():
    # Table Q3.1 - Create dict recording burger details
    burgDetails = {"B":{"Name":"Beef Burger","Price":12.95},\
                   "C":{"Name":"Chicken Burger","Price":5.95},\
                   "F":{"Name":"Fish Burger","Price":7.95}}    
    
    CashRegisterGUI(burgDetails)
    

if __name__ == '__main__':
    main()
    