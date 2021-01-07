class Product:
    def __init__(self,code,qtyOnHand):
        self._code = code
        self._qtyOnHand = qtyOnHand
    
    @property
    def code(self):
        return self._code
    
    @property
    def qtyOnHand(self):
        return self._qtyOnHand
    
    @qtyOnHand.setter
    def qtyOnHand(self, qtyOnHand):
        self._qtyOnHand = qtyOnHand
        
        
    def __str__(self):
        return 'Code: {:5s} Quantity: {:3d}'.format(self._code,self._qtyOnHand)
    

class ProductException(Exception):  # Question 2a
    ''' User defined Product Exception class '''
    
class DetailProductException(ProductException): # Question 2a
    ''' Exception that returns details of the product that failed. '''
    def __init__(self,failedProduct,message):
        super().__init__(message)
        self._failedProduct = failedProduct
        
    @property
    def failedProduct(self):
        return self._failedProduct
    

class ProductList:  # Question 2b
    _products = {}
    def __init__(self,products = None):
        self._products =  self._products if products is None else products
    
    def searchProduct(self,productCode):
        if productCode in self._products:
            return self._products[productCode]
            
        else:
            return None
        
    def addProduct(self,productCode,qty):
        if self.searchProduct(productCode) == None:
            self._products[productCode] = Product(productCode,qty)
            return self._products[productCode]
            
        else:
            raise ProductException("Product {} already exists in product list.".format(productCode))
        
    def removeProduct(self,productCode):
        if self.searchProduct(productCode) == None:
            raise ProductException("Product {} does not exist in product list!".format(productCode))
        
        elif self._products[productCode].qtyOnHand == 0:
            del self._products[productCode]
            
        else:
            raise DetailProductException(productCode,"There is still some stock of the product!")
                
    def listOfProducts(self):
        for item in self._products.values(): # Product class objects
            print(item)
        
        return self._products
        
    
    def addStock(self,productCollection):
        ErrorList = [] # list of Product objects
        
        for productCode in productCollection:
            if self.searchProduct(productCode) == None: # Does not exist in ProductList
                ErrorList.append(productCollection[productCode])
            
            else:   # item exists in ProductList
                self._products[productCode].qtyOnHand += productCollection[productCode].qtyOnHand
                
        
        if bool(ErrorList):
            raise DetailProductException(ErrorList,"Some updates do not match existing products!")

class ProductListApp:
    def __init__(self,ProductList = ProductList()):
        self._ProductList = ProductList
        
        
    # Prints menu options
    def menu(self):
        print("Menu:")
        print("1. Add")
        print("2. Remove")
        print("3. Update")
        print("4. List")
        print("0. Exit")        

        try:
            optionSelect = input("Enter option: ")
        
            if optionSelect[0] == "1":
                self.opt1()
            
            elif optionSelect[0] == "2":
                self.opt2()
            
            elif optionSelect[0] == "3":
                self.opt3()
                
            elif optionSelect[0] == "4":
                self.opt4()
                
            elif optionSelect[0] == "0":
                print("Exiting application.")
                exit()
                
            else:
                print("Please input a valid menu option (1,2,3,4,0)")
        
        except IndexError:
            print("No input was detected. Input '0' if trying to exit program.")
            
            
        
    # 1. Add a product using product code and qty
    def opt1(self):
        try:
            productCode = input("Enter code of product to add: ")
            productQty = int(input("Enter quantity of product: "))        
            self._ProductList.addProduct(productCode, productQty)
        
        except ProductException as e:
            print(e)
        
        except ValueError as e:
            print("Please input a valid integer value for quantity.")
        
        else:
            print("Product Added. {}".format(self._ProductList.searchProduct(productCode)))
    
    # 2. Removes a product from the product list
    def opt2(self):
        try:
            productCode = input("Enter code of product to remove: ")
            self._ProductList.removeProduct(productCode)
        
        except (ProductException, DetailProductException) as e:
            print(e)
            if type(e) == DetailProductException:
                userOverride = input("Do you want to write off stock (y/n): ")
                if userOverride[0].lower() == "y":
                    del self._ProductList._products[productCode]
                    print("Product is removed.")
                
                elif userOverride[0].lower() == "n":
                    print("Product is not removed. No changes were made.")
                
                else:
                    print("An invalid option was selected. No changes were made.")
            
        else:
            print("Remove is successful.")
                
    
    # 3. Updates current collection of products
    def opt3(self):
        productCollection = {}
        while True:
            productCode = input("Enter code of product to add stock to or enter to end: ")
            if productCode == "":
                break
            try:
                productQty = int(input("Enter quantity of product: "))
                if productCode in productCollection:
                    print("Error, unable to update same product more than once. Returning to menu.")
                    return
                
                else:
                    productCollection[productCode] = Product(productCode,productQty)
            
            except ValueError as e:
                print("Please input a valid integer value for quantity. Product not updated.")

        
        try:
            self._ProductList.addStock(productCollection)
            
        except DetailProductException as e:
            print(e)
            for productObj in e.failedProduct: # e.failedProduct is a list
                userUpdate = input("Do you want to add this product, {} (y/n)? "\
                                   .format(productObj))
                if userUpdate[0].lower() == "y":
                    print("Product added",\
                          self._ProductList.addProduct(productObj.code, productObj.qtyOnHand))
                
                elif userUpdate[0].lower() == "n":
                    pass
                
                else:
                    print("An invalid option was selected. No changes were made.")
            
            print("Failed products are resolved")
        
        else:
            print("Update is complete")             

    
    # 4. List collection of products in ProductList object
    def opt4(self):
        if bool(self._ProductList.listOfProducts()):
            pass
        
        else:
            print("Product list is empty.")
            

def main():
    menu = ProductListApp()
    
    while True:
        menu.menu()
        print()

if __name__ == '__main__':
    main()
    
