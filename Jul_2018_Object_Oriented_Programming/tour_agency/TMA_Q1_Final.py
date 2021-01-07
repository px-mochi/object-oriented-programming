from _datetime import datetime
from abc import ABC, abstractmethod
# date and time values are added to objects using datetime

class Tour:
    # Question 1ai)
    def __init__ (self,tourCode,tourName,numDays,numNights,cost=0):
        self._tourCode = tourCode
        self._tourName = tourName
        self._daysNights = "{0}D/{1}N".format(numDays,numNights)
        self._cost = cost
    
    # Question 1aii)    
    @property
    def tourCode(self):
        return self._tourCode
    
    @property
    def tourName(self):
        return self._tourName
    
    @property
    def tourCost(self):
        return self._cost
    
    @tourCost.setter
    def tourCost(self,cost):
        self._cost = cost
        
    def __str__(self):
        return "Code: {0:<7} Name: {1:<30} {2:>7}  Base Cost: ${3:<8}"\
                .format(self._tourCode,self._tourName,self._daysNights,self._cost)

# Question 1bi)
class ScheduledTour:
    handlingFee = 120
    def __init__(self,tour,schCode,language,depDateTime,capacity,availSeat,isOpen=True):
        self._tour = tour
        self._schCode = schCode
        self._language = language
        self._depDateTime = datetime.strptime(depDateTime,"%d %b %Y %I.%M %p")
        self._capacity = capacity
        self._availSeat = availSeat
        self._isOpen = isOpen

    
    @property
    def code(self):
        return "{}-{}".format(self._tour._tourCode,self._schCode)
    
    @property
    def cost(self):
        return self._tour.tourCost
    
    @property
    def tourDetail(self):
        if self._isOpen:
            Open = 'Yes'
        
        else:
            Open = 'No'
        
        return "Departure: {:%#d %b %Y %H:%M} Capacity: {:^4} Available: {:>3} Open: {}"\
            .format(self._depDateTime,self._capacity,self._availSeat,Open)
    
    @property
    def tour(self):
        return self._tour
    
    @tour.setter
    def tour(self,tour):
        self._tour = tour
    
    def bookSeats(self,booking):
        if booking > 0 and booking <= self._availSeat:
            self._availSeat -= booking
            return True
        else:
            return False
    
    def cancelSeats(self,cancel):
        if cancel > 0 and cancel + self._availSeat <= self._capacity:
            self._availSeat += cancel
            return True
        else:
            return False
        

    def getPenaltyRate(self, cancelDate = datetime.today()):
        daysTillTour = (self._depDateTime - cancelDate).days
        if daysTillTour <= 7:
            penalty = 1.00
        elif daysTillTour <=20:
            penalty = 0.50
        elif daysTillTour <= 45:
            penalty = 0.25
        else:
            penalty = 0.10
        
        return penalty
    
    @classmethod
    def getHandlingFee(cls):
        cls.__handlingFee = cls.handlingFee
        return cls.__handlingFee

    
    
    def changeOpenStatus(self):
        if self._isOpen:
            self._isOpen = False
        
        else:
            self._isOpen = True
        
        return self._isOpen
        
    def __str__(self):
        return "{}\nSchedule Code: {:8} Language: {:<10} {}"\
            .format(self.tour,self.code,self._language,self.tourDetail)

class PeakScheduledTour(ScheduledTour):
    peakSurchage = 0.25
    handlingFee = 200
    
    # Question 1bii)
    # This constructor can be removed as it just inherits from ScheduledTour
    def __init__(self,tour, schCode, language, depDateTime, capacity, availSeat, isOpen = True):
        super().__init__(tour, schCode, language, depDateTime, capacity, availSeat, isOpen)
        
    @property
    def cost(self):
        return self._tour._cost * (1 + self.peakSurchage)
    
    @property
    def surcharge(self):
        return self._tour.tourCost * self.peakSurchage

    
    def getPenaltyRate(self,cancelDate = datetime.today()):
        daysTillTour = (self._depDateTime - cancelDate).days
        if daysTillTour <= 7:
            penalty = 1.00
        elif daysTillTour <=20:
            penalty = 0.50 + 0.1
        elif daysTillTour <= 45:
            penalty = 0.25 + 0.1
        else:
            penalty = 0.10 + 0.1
        
        return penalty    



    def __str__(self):        
        return super().__str__() + " Cost: {:.2f} (${:.2f} peak surcharge applies)"\
            .format(self.cost,self.surcharge)

class Customer:
    # Question 1ci)
    def __init__(self,passportNum = 'SXXXXXXXZ',name = 'Name',contact = '91234567',address = 'Address'):
        self._passportNum = passportNum
        self._name = name
        self._contact = contact
        self._address = address
        
    # Question 1cii)
    @property
    def passportNum(self):
        return self._passportNum
    
    @property 
    def name(self):
        return self._name
    
    @property
    def contact(self):
        return self._contact
    
    @property
    def address(self):
        return self._address
    
    @contact.setter
    def contact(self,contact):
        self._contact = contact
    
    @address.setter
    def address(self,address):
        self._address = address
    
    def __str__(self):
        return "Passport Number: {}  Name: {:25} Contact: {}  Address: {}".format(self._passportNum,self.name,self._contact,self.address)


class Booking(ABC): # Question 1di)
    _bookingID = 1
    
    def __init__(self,tour,customer,numSeats):
        self._tour = tour     # This should be the scheduledtour/peakscheduled tour object
        self._customer = customer # Customer object
        self._numSeats = numSeats
        self._bookingID = Booking._bookingID
        Booking._bookingID += 1
        self._tour.bookSeats(numSeats)
        
    @property
    def passportNum(self):
        return self._customer.passportNum
    
    @property
    def schTour(self):
        return self._tour.code
    
    @property
    def bookingID(self):
        return self._bookingID
    
    @property
    def numSeats(self):
        return self._numSeats

    @abstractmethod
    def tourCost(self):
        abstracttourCost = self._tour.cost
        return abstracttourCost
    
    def getPenaltyAmount(self,inputCancelDate):
        cancelDate = datetime.strptime(inputCancelDate,"%d/%m/%Y")
        penaltyRate = self._tour.getPenaltyRate(cancelDate)

        penaltyAmount = (self.tourCost * penaltyRate) + self._tour.handlingFee
        if penaltyAmount > self.tourCost:
            penaltyAmount = self.tourCost
        return penaltyAmount
    
    def addSeats(self,seats):
        if seats > self._tour._availSeat:
            return False
        else:
            self._numSeats += int(seats)
            self._tour.bookSeats(seats)
            return True

    
    def removeSeats(self,seats):
        if seats > self._tour._capacity - self._tour._availSeat:
            print("Seats removed must not cause tour to exceed capacity.")
            return False
        
        else:
            self._numSeats -= int(seats)
            self._tour.cancelSeats(seats)
            return True
        
    def __str__(self):
        return "Booking Id: {:0=10} \nPassport Number: {}  Name: {:<20} Contact: {} Address: {}\nBooked {}"\
            .format(self.bookingID,self.passportNum,self._customer.name,self._customer.contact,self._customer.address,\
                    self._tour)
    
class IndividualBooking(Booking): # Question 1dii)
    _surcharge = 0.5
    
    def __init__(self,tour,customer,numSeats,singleRoom):
        super().__init__(tour, customer, numSeats)
        self._singleRoom = singleRoom
        if numSeats > 1:
            print("Individual bookings can only have 1 seat. Seat changed to 1.")
            self._numSeats = 1
        
    
    @property
    def tourCost(self):
        cost = super().tourCost()
        if self._singleRoom:
            tourCost = cost * (1 + self._surcharge)
        else:
            tourCost = cost
        
        return tourCost
    
    
    #addSeats and removeSeats return false as there is only 1 seat in an indi booking.
    def addSeats(self,seats):
        print("Seats cannot be added from an individual booking.")
        return False
    
    def removeSeats(self,seats):
        print("Seats cannot be removed from an individual booking.")
        return False
    
    def __str__(self):
        if self._singleRoom:
            surcharge = "(${:.2f} Single room surcharge)".format(self._tour.cost * self._surcharge)
        
        else: surcharge = "(No single room surcharge)"
            
        return super().__str__() + "\nFinal Cost per pax: ${:.2f} {}".format(self.tourCost,surcharge)

class GroupBooking(Booking):    # Question 1diii)
    def __init__(self,tour,customer,numSeats):
        super().__init__(tour, customer, numSeats)
        if numSeats < 2:
            print("There must be at least 2 seats booked for a Group Booking.")
            Booking._bookingID -= 1
    
        
    @property
    def tourCost(self):
        cost = super().tourCost()
        if self._numSeats in range(6,10):
            discount = 0.05
        
        elif self._numSeats >= 10:
            discount = 0.1
        
        else:
            discount = 0.0
        
        tourCost = cost * (1- discount)
        return tourCost
    
    def removeSeats(self, seats):
        if self._numSeats - seats < 2:
            print("Unable to remove seats. There must be at least 2 seats booked for a Group Booking.")
            return False
        elif seats > self._tour._capacity - self._tour._availSeat:
            print("Seats removed must not cause tour to exceed capacity.")
            return False
        
        else:
            self._numSeats -= seats
            self._tour.cancelSeats(seats)
            return True
    
    def __str__(self):
        if self.tourCost == self._tour.cost:
            groupDisc = "(No group discount applies)"
        
        if self.tourCost/self._tour.cost == 0.95:
            groupDisc = "(with 5% discount)"
        
        if self.tourCost/self._tour.cost == 0.90:
            groupDisc = "(with 10% discount)"
        
        return super().__str__() + "\nFinal Cost per pax: ${:.2f} for group size of {} {}".format(self.tourCost,self._numSeats,groupDisc)
 
class tourAgency: # Question 1e)
    def __init__(self,cTours = [],cSchTours = [],cCustomers = [],cBookings = []):
        self._cTours = cTours
        self._cSchTours = cSchTours
        self._cCustomers = cCustomers
        self._cBookings = cBookings
    
    
    # 4 add methods
    def addTour(self,tour): # Add a tour to collection of tours
        self._cTours.append(Tour)
        return self._cTours
    
    def addSchTour(self,schTour): # Add a Scheduled Tour to collection of schTours, both peak & normal
        self._cSchTours.append(schTour)
        return self._cSchTours
    
    def addCust(self,customer): # Add a customer to collection of customers
        self._cCustomers.append(customer)
        return self._cCustomers
    
    def addBooking(self,booking): # Add a Booking to collection of bookings
        self._cBookings.append(booking)
        return self._cBookings
    
    
    # 3 search methods
    def searchSchTour(self,schTourCode): # search sch tours given code EG: "JA312-1"
        for i in self._cSchTours:
            if schTourCode == i.code:
                return i
        
        else:
            return None
    
    def searchCustomer(self,passportNum): # Search customer given passport number
        for i in self._cCustomers:
            if passportNum == i.passportNum:
                return i
        
        else:
            return None
        
    def searchBooking(self,booking): # Search bookings given bookingID
        for i in self._cBookings:
            if booking == i.bookingID:
                return i
        
        else:
            return None
    
    # other methods below
    def bookingID(self):
        return self._cBookings[0].bookingID
    
    def displayBookings(self):
        if bool(self._cBookings):
            for i in self._cBookings:
                print(i,"\n")            
        
        else:
            print("There are no bookings in the collection.")

    
    def displayOpenScheduledTours(self):
        OpenScheduledTours = []
        for tours in self._cSchTours:
            if tours._isOpen == True:
                OpenScheduledTours.append(tours)
                
        if bool(OpenScheduledTours):
            for i in OpenScheduledTours:
                print(i,"\n")

        else:
            print("There are no open scheduled tours.")
    
    def cancelBooking(self,bookingid):
        if self.searchBooking(bookingid) == None:
            return False
        
        else:
            selectedBooking = self.searchBooking(bookingid)
            seatsInBooking = selectedBooking._numSeats
            selectedBooking._tour.cancelSeats(seatsInBooking)   # Cancel seats in scheduled tour
            self._cBookings.remove(selectedBooking) # Remove booking from Tour Agency list
            return True
        
    def addSeats(self,bookingid,seats):
        if self.searchBooking(bookingid) == None:
            return False
        
        else:
            selectedBooking = self.searchBooking(bookingid)
            return selectedBooking.addSeats(seats)  #This returns True or False for you
            
        
    def removeSeats(self,bookingid,seats):
        if self.searchBooking(bookingid) == None:
            return False
        
        else:         
            selectedBooking = self.searchBooking(bookingid)
            return selectedBooking.removeSeats(seats) #This returns True or False for you
 
def main():
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
    
    #########################
    # PRINTOUTS FOUND BELOW #
    #########################
    print("- Individial Bookings found below -")
    print(indibook1)
    print(indibook2)
    print(indibook3)
    print(indibook4)
    
    print("- Group Bookings found below -")
    print(groupBook1)
    print(groupBook2)
    print(groupBook3)
    print(groupBook4)
    
    
if __name__ == '__main__':
    main()