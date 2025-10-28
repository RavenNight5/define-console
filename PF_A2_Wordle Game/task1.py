#Number Statistics - Isla McLaughlin (29296040) - 08/01/2025

global newList
global evenNumbers
global oddNumbers

stopInputKeywords = ["s", "S", "stop", "Stop"]  #*these will be used as the 'commands' the user can use to stop inputting numbers

def inputAgainQuestion():
    """
    > Prompt the user to either continue with the current list or clear it.
    > If input is valid, call the main function with their decision as a parameter.
    > Otherwise tell the user to input one of the optiond and run inputAgainQuestion() again.

    Next main fn > main()
    """
    
    inputAgain = input("\nWould you like to clear lists and input again or continue with current lists?\n > Clear [1]\n > Continue [2]\n")

    if inputAgain == "1":

        main(True, False)

    elif inputAgain == "2":

        main(True, True)

    else:
        print("\nChoose from one of the numerical options provided. Please try again.")
        
        inputAgainQuestion()


def validateAndAppend(numInput):
    """
    > If the input is in the stop commands list then calculate desired values and print them.
        > After values are printed call inputAgainQuestion()
    > Otherwise checks if the input is numeric:
        > Check if the number is a whole number > 0, 
            > Check if the number is not already in the list, if it is then remove it and append it again,
            > Otherwise appended number to the list.

    > If input is not numeric tell the user to enter a proper command, then run validateAndAppend() again.

    Next main fn > inputAgainQuestion()
    """
    
    #print(numInput, type(numInput))

    if numInput in stopInputKeywords:  #if the input by the user is one of the commands* continue the program
        print("\nStopped inputting.\nCurrent list status:", newList) 
        
        uniqueNumberCount = len(newList)

        productOfListNums = 1

        for i in newList:
            productOfListNums = productOfListNums * i


        meanOfList = sum(newList)/uniqueNumberCount

        iDistFromMean = 0
        iDistFromMeanSquared = 0
        sumOfiDistFromMeanSquared = 0
        varianceOfListNums = 0

        for i in newList:
            iDistFromMean = i - meanOfList
            iDistFromMeanSquared = iDistFromMean ** 2

            sumOfiDistFromMeanSquared += iDistFromMeanSquared
        
        varianceOfListNums = sumOfiDistFromMeanSquared / (uniqueNumberCount - 1)
        varianceOfListNumsFormatted = format(varianceOfListNums, ".2f")

        rangeOfListNums = 0

        largestNum = newList[1]  #initialise from a number in the list
        smallestNum = newList[0]
        carryNum = 0

        for i in newList:
            if i > largestNum:
                largestNum = i
            elif i < smallestNum:
                smallestNum = i
            else:
                carryNum = i
        
        #print(smallestNum, largestNum)
        rangeOfListNums = largestNum - smallestNum

        for i in newList:
            if i % 2 == 0:  #number is even as it's divisible by 2 with no remainder
                evenNumbers.append(i)
            else:
                oddNumbers.append(i)

        print(f"\nNumber of unique numbers in the list: {uniqueNumberCount}",
              f"\nProduct of the numbers in the list: {productOfListNums}",
              f"\nRange of the numbers in the list: {rangeOfListNums}",
              f"\nVariance of the numbers in the list (to 2 decimal places): {varianceOfListNumsFormatted}")
        
        if len(evenNumbers) > 0:
            print(f"\nEven numbers in list: {evenNumbers}")
        else:
            print("\nNo even numbers were provided.")

        if len(oddNumbers) > 0:
            print(f"Odd numbers in list: {oddNumbers}")
        else:
            print("No odd numbers were provided.")
        

        inputAgainQuestion()

    else:
        if numInput.isnumeric():
            if int(numInput) > 0:  #if the input by the user is a positive integer
                
                if int(numInput) in newList:  #if number is already in list
                    print(f"List already contains the integer {numInput}, duplicate has been removed and replaced.")

                    newList.remove(int(numInput))  #remove the duplicate
                    newList.append(int(numInput))  #append the list again with the user's number
                
                else:

                    newList.append(int(numInput))
                
                
                print("List status:", newList, "enter [s] to stop inputs.")
                
                main(False, True) #call the main() function again as the user has not yet prompted to stop their inputs
            
            elif int(numInput) <= 0:  #if the input by the user is a negative number or 0
                print("The number cannot be 0 or negative. Please try again.")

                main(False, True)
            
        else:
            print("Please enter a proper command or a positive integer. Please try again.")

            main(False, True)

   

def main(inputWithInstructions, continueBool):
    """
    > Uses the global list variables.
    > If the user is not continuing to add to their list, set newList as empty.
    > Allows the user to input:
        > If the length of the list is greater than 2, pass the user's input to validateAndAppend()
    
    Next main fn > validateAndAppend()
    """

    global newList
    global evenNumbers
    global oddNumbers

    if continueBool == False:
        newList = []
        evenNumbers = []
        oddNumbers = []
    else:  #even and odd number lists are initialised even if user continues as they are calculated when user stops input
        evenNumbers = []
        oddNumbers = []
    
    ##User input##
    if inputWithInstructions == True:  #used to only prints instructions at the beginning of the program
        strInput = input("Enter a positive integer number, input [s]top to end input:\n")

        if strInput in stopInputKeywords and len(newList) < 2:
            print("List must be of length 2 or greater. Please try again.")

            main(True, True)

        else:
            
            validateAndAppend(strInput)

    elif inputWithInstructions == False:
        strInput = input("")
        
        if strInput in stopInputKeywords and len(newList) < 2:
            print("List must be of length 2 or greater. Please try again.")

            main(True, True)

        else:
            
            validateAndAppend(strInput)



if __name__ == "__main__":
    
    main(True, False)



"""
> Prompts the user to input only positive integer numbers at the
terminal (numbers with decimals, negative numbers or
characters will not be accepted) ###DONE###

> Assign those numbers to a list and removes any duplicate
numbers and informs the user of the removed duplicates ###DONE###

> Counts the number of unique numbers in the list ###DONE###

> Calculates their product, range and variance ###DONE###

> Identifies the even and odd numbers from the list and stores
them in separate lists. If the list of even numbers is empty,
print a message saying "No even numbers were provided." If
the list of odd numbers is empty, print a message saying "No
odd numbers were provided." ###DONE###

> Prints all the above information at the terminal ###DONE###
"""