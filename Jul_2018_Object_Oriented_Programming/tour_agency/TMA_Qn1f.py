from TMA_Q1_Final import * # Source code and methods used in 1e are imported

class TourApplication:    
    def __init__(self,tourData):
        # Initializing tour agency collection inside this class for menu use
        self._tourData = tourData 
    
    # Prints menu options
    def menu(self):
        print("Menu:")
        print("1. Add Booking")
        print("2. Cancel Booking")
        print("3. Add Seats to Booking")
        print("4. Remove Seats from Booking")
        print("5. Display Booking")
        print("0. Exit")
        
        
        optionSelect = input("Enter option: ")
        try:
            if optionSelect[0] == "1":
                self.opt1()
            
            elif optionSelect[0] == "2":
                self.opt2()
            
            elif optionSelect[0] == "3":
                self.opt3()
                
            elif optionSelect[0] == "4":
                self.opt4()
                
            elif optionSelect[0] == "5":
                self.opt5()
                
            elif optionSelect[0] == "0":
                print("Exiting application.")
                exit()
            
            else:
                print("Please input a valid option")
            
        except IndexError:
            print("No input was detected. Input '0' if trying to exit program.")        
        
    # 1. Add Booking, via passportNum
    def opt1(self):
        passportNum = input("Enter passport number: ")
        if self._tourData.searchCustomer(passportNum) is not None:
            selectedCustomer = self._tourData.searchCustomer(passportNum)
                    
            # Display list of open scheduled tours
            self._tourData.displayOpenScheduledTours()
            
            schCode = input("Enter schedule code of tour: ")
            if self._tourData.searchSchTour(schCode) is not None:
                selectedSchTour = self._tourData.searchSchTour(schCode)
                        
                print("1. Individual Booking")
                print("2. Group Booking")
            
                                        
                bookingChoice = input("Enter choice of booking: ")
                if bookingChoice[0] == "1":
                    print("1. Single")
                    print("2. Sharing")
                    
                    while True:
                        roomChoice = input("Enter choice of room: ")
                        if roomChoice[0] == "1":
                            newBooking = IndividualBooking(selectedSchTour,selectedCustomer,1,True)
                            break
                        elif roomChoice[0] == "2":
                            newBooking = IndividualBooking(selectedSchTour,selectedCustomer,1,False)
                            break
                        else:
                            print("Please input a valid choice.")
                
                elif bookingChoice[0] == "2":
                    while True:
                        numSeatsChoice = int(input("Enter number of seats to book (max {}): ".format(selectedSchTour._availSeat)))
                        if numSeatsChoice <= selectedSchTour._availSeat and numSeatsChoice > 0:
                            break
                        
                        if numSeatsChoice > selectedSchTour._availSeat:
                            print("Please input a valid number of seats.")
                            break
                                                    
                    newBooking = GroupBooking(selectedSchTour,selectedCustomer,numSeatsChoice)
                
                self._tourData.addBooking(newBooking) # Adds new booking to list of bookings
                print("Booking is added",newBooking) # Print new booking object __str__
            
            else:
                print("Schedule code not found in Scheduled tour list.")
        else:
            print("Passport number not found in customer list.")
            
            
            
            
        
        
    # 2. Cancel Booking
    def opt2(self):
        try:
            bookingNum = int(input("Enter booking number: "))
        except ValueError:
            print("Please input a valid booking number.")
        
        else:
            dateInput = input("Enter date (d/m/y): ")
            
            if self._tourData.searchBooking(bookingNum) is not None:
                selectedBooking = self._tourData.searchBooking(bookingNum)
            
                try:
                    penaltyAmount = selectedBooking.getPenaltyAmount(dateInput)
                except ValueError as e:
                        print("Please input a valid date. ({})".format(e))
                
                else:
                    print(selectedBooking)
                    print("Penalty of ${:.2f} per seat removed applies".format(penaltyAmount))
                    self._tourData.cancelBooking(bookingNum)
                    print("Cancel booking is successful")
                
            else:
                print("Booking ID not found in list of bookings.")    
            
        

        
        
    # 3. Add Seats to Booking
    def opt3(self):
        try:
            bookingNum = int(input("Enter booking number: "))
        except ValueError:
            print("Please input a valid booking number.")
        
        else:
            if self._tourData.searchBooking(bookingNum) is not None:
                selectedBooking = self._tourData.searchBooking(bookingNum)        
                print(selectedBooking,"\n")
                prevPricePerPax = selectedBooking.tourCost # Obtain previous cost per seat
                
                try:
                    # This input prompt is placed after as it makes more sense to
                    # separate the before and after booking details.
                    addSeatsInput = int(input("Enter number of seats to add: "))
                    if self._tourData.addSeats(bookingNum,addSeatsInput):
                        print(selectedBooking)
                        print("Please pay ${:.2f} per seat.".format(selectedBooking.tourCost))
                        discount = prevPricePerPax - selectedBooking.tourCost # Calculate discount per seat
                        if discount > 0:
                            print("Discount of ${:.2f} per existing seat.".format(discount))
                        print("Add seats is successful")
                except ValueError:
                    print("Invalid seat input value.")
                        
            else:
                print("Booking ID not found in list of bookings")
        
    
    # 4. Remove Seats from Booking
    def opt4(self):
        try:
            bookingNum = int(input("Enter booking number: "))
        except ValueError:
            print("Please input a valid booking number.")
        
        else:
            if self._tourData.searchBooking(bookingNum) is not None:
                selectedBooking = self._tourData.searchBooking(bookingNum)        
                print(selectedBooking,"\n")
                prevPricePerPax = selectedBooking.tourCost # Obtain previous cost per seat
                
                try:
                    # This input prompt is placed after as it makes more sense to
                    # separate the before and after booking details.        
                    removeSeatsInput = int(input("Enter number of seats to remove: "))
                    dateInput = input("Enter date (d/m/y): ")
                    if self._tourData.removeSeats(bookingNum,removeSeatsInput):
                        try:
                            penaltyAmount = selectedBooking.getPenaltyAmount(dateInput)
                        
                        except ValueError as e:
                            print("Please input a valid date. ({})".format(e))   
                
                        else:
                            print(selectedBooking)
                            print("Penalty of ${:.2f} per seat removed applies".format(penaltyAmount))
                            refundAmt = prevPricePerPax - penaltyAmount # Calculate refund per seat
                            if refundAmt < 0:
                                refundAmt = 0.00
                            print("Refund amount ${:.2f} per seat".format(refundAmt))
                            topupAmt = selectedBooking.tourCost - prevPricePerPax # Calculate top up per seat
                            if topupAmt < 0:
                                topupAmt = 0.00
                            print("Require top up  of ${:.2f} per seat".format(topupAmt))
                            print("Remove seats is successful")       
                    
                    else:
                        print("Please input a valid number of seats to remove.")
                except ValueError:
                    print("Value Error: Please input a number.")
                
            else:
                print("Booking ID not found in list of bookings.")
            
            
    # 5. Display Booking
    def opt5(self):
        self._tourData.displayBookings()

    

def main():
    # INITIALIZING TOUR AGENCY COLLECTION
    #Tours available (tourCode,tourName,numDays,numNights,cost=0)
    t1 = Tour('JA312','Food Trail in Tokyo',7,6,1999.14)
    t2 = Tour('KO111','Discover Korea',8,7,1449.36)
    t3 = Tour('VI102','Vietnam Highlights',5,4,999.75)
            
    #Different dates available in string format based on TMA tables (used in depDateTIme)
    date1 = '5 Nov 2018 3.30 pm'
    date2 = '15 Jan 2019 10.45 am'
    date3 = '24 Feb 2019 3.15 pm'
    peakdate1 = '15 Dec 2018 1.30 am'
    peakdate2 = '15 Dec 2018 3.15 pm'
            
    #Creating ScheduledTour objects (tour,schCode,Language,depDateTime,capacity,availSeat,isOpen=True)
    sch1 = ScheduledTour(t1,1,"English",date1,35,9,False)
    sch2 = ScheduledTour(t1,2,"Mandarin",date2,25,25,True)
    sch3 = ScheduledTour(t3,5,"English",date3,35,35,True)
            
    #Creating PeakScheduledTour objects (tour, schCode, language, depDateTime, capacity, availSeat, isOpen = True)
    peak1 = PeakScheduledTour(t2,6,"Mandarin",peakdate1,50,45,True)
    peak2 = PeakScheduledTour(t2,2,"English",peakdate2,35,10,True)
            
    #Creating Customer objects (passportNum,name,contact,address)
    cust1 = Customer('E1234567X','Alice Lee',98989898,'27F Sea Avenue')
    cust2 = Customer('E7777777X','Peter Tam',97777777,'8A Gray Lane')
    cust3 = Customer('E2323232Y','Joy Seetoh',89898989,'15 Sandy Lane')
    cust4 = Customer('E1111111Y','Mary Tham',85858585,'16 Jalan Mydi')
    cust5 = Customer('E9999999Y','Sally Koh',87878787,'1 Joo Heng Road')
            
    #Creating IndividualBooking (tour,customer,numSeats,singleRoom) 
    #and GroupBooking (tour,customer,numSeats) objects
    indibook1 = IndividualBooking(sch2,cust1,1,True)    # id 1
    indibook2 = IndividualBooking(sch2,cust2,1,False)   # id 2
    groupBook1 = GroupBooking(sch2,cust3,9)     # id 3
    indibook3 = IndividualBooking(peak1,cust1,1,True)   # id 4
    indibook4 = IndividualBooking(peak1,cust2,1,False) # id 5        
    groupBook2 = GroupBooking(peak1,cust2,5)    # id 6
    groupBook3 = GroupBooking(peak1,cust3,6)    # id 7
    groupBook4 = GroupBooking(peak1,cust4,10)   # id 8 
            
    # Tour Agency (cTours = [],cSchTours = [],cCustomers = [],cBookings = [])
    tourData = tourAgency([t1,t2,t3],[sch1,sch2,sch3,peak1,peak2],\
                [cust1,cust2,cust3,cust4,cust5],\
                [indibook1,indibook2,groupBook1,indibook3,indibook4,\
                 groupBook2,groupBook3,groupBook4])  
    
    #####################################
    #        END OF INITIALIZING        #
    #####################################
    
    menu = TourApplication(tourData)    # Creating menu object
    
    # Running application
    while True:
        menu.menu()
        print()
    
    

if __name__ == '__main__':
    main()
    