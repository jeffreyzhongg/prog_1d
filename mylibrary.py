## Business Logic ---------------------------------------------------------------------
## This file stores functions that implement the business logic.
## 1) calculate_total: Takes in the number of adults and children and returns the total price. 
## Currently, it returns 0,0. Modify the code so that it returns the total price of the tickets. 
##
## 2) audio_guides: Takes in the number of items and return the total price.
## Currently, it returns 0. Modify the code so that it returns the total price according to the number of items. 
## ------------------------------------------------------------------------------------

def calculate_total(adults, children):
    ADULT_PRICE = 10
    CHILD_PRICE = 5
    
    total_adults = adults * ADULT_PRICE
    total_children = children * CHILD_PRICE
    
    return total_adults, total_children

def audio_guides(items): 
    PRICE_PER_ITEM = 3
    
    total_guides = items * PRICE_PER_ITEM
    
    return total_guides


## Make It Yours ---------------------------------------------------------------------
## You are now ready to design your own ticketing scheme 
## And modify the code so that the web application works according to your design. 
## ------------------------------------------------------------------------------------
