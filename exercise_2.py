import sys


#Donut Function 
def donuts(count):
    if type(count) == int:
        if count < 10:
            return "Number of donuts:"+ str(count) #Converted to str so that it can be added to the result.
        else: 
            return("Number of donuts: many")
    else: 
        return "Please enter an integer" #If the input is not an integer, it will ask the user to do so 



#Vergbing Function
def verbing(s):
    #Need the length top be atleast 3, and should not end with ing
    if len(s) >= 3 & s.endswith("ing") == False: 
        return(s+"ing")
    #Need the length to be atleast 3 but, should be ending with ing 
    elif len(s) >= 3 & s.endswith("ing") == True:
        return(s+"ly") #Adds "ly" if the string already has ing
    else:
        return s # If anything other than the condition happens it will return the input


#Remove Adjacents
def remove_adjacents(nums):
    if len(nums) != 0:   
        #Converts the given list to a set and then convert it back to a list
        #because set does not allow duplicate values so it does the work for us.
        new_list = list(set(nums)) 
        # reutrns a list since we converted it back into a list
        return new_list
    else:
        return None
    # Other wise it reutrns a None, if the length == 0 or there is nothing in nums
    


def main():
    print("Donuts")

    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts("twentyone"))


    print("Verbing")
    print(verbing("hail"))
    print(verbing("swimming"))
    print(verbing("do"))
        
    print("Remove Adjacent")

    print(remove_adjacents([1,2,2,3]))
    print(remove_adjacents([2,2,3,3,3]))
    print(remove_adjacents([]))

if __name__ == "__main__":
    main()