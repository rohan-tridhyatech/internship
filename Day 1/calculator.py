class MathamaticalOperations:

    def __init__(self, num1, num2):
        self.__num1 = num1
        self. __num2 = num2
    
    def addition(self):
        return self.__num1 + self.__num2
    
    def subtraction(self):
        return self.__num1 - self.__num2
    
    def multiplication(self):
        return self.__num1 * self.__num2
    
    def division(self):
        try:
            return self.__num1 / self.__num2
        except ZeroDivisionError:
            print("Error: Division by zero")
            return None  
            


class Calculator(MathamaticalOperations):
    
    def __init__(self, num1, num2):
        super().__init__(num1=num1, num2=num2)



