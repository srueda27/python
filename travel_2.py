from datetime import datetime, timedelta

# Calculate the number of days from Monday to Friday (weekdays) and the number of days on the weekends
def count_weekdays_and_weekends(checkin, checkout):
    current_date = checkin
    weekdays = 0
    weekends = 0
    while current_date <= checkout:
        if current_date.weekday() < 5:  # Monday to Friday (0 to 4)
            weekdays += 1
        else:
            weekends += 1
        current_date += timedelta(days=1)
    return [weekdays, weekends]
  
def calculate_travel_package_cost(num_people, checkin, checkout, meals=[], tours=[], accommodation='normal'):
    # Base costs per item and base meal discounts
    meal_cost_per_person = 10
    luxury_meal_cost_per_person = 20
    meal_discount_rate_weekends = 0.05
    meal_discount_rate_weekdays = 0.1
    tour_referrals_discount = 0.25
    our_tour_costs = {'trail_running': 15, 'cycling': 15, 'sightseeing': 15}
    referrals_tour_costs = {'paragliding': 50, 'scuba_diving': 50}
    accommodation_costs = {'normal': 15, 'luxury': 100}
    
    # Get the check-in and check-out dates from the parameters
    checkin_year, checkin_month, checkin_day = checkin.split('-')
    checkin_date = datetime(int(checkin_year), int(checkin_month), int(checkin_day))
    checkout_year, checkout_month, checkout_day = checkout.split('-')
    checkout_date = datetime(int(checkout_year), int(checkout_month), int(checkout_day))
    
    # Calculate the weekday days and the weekend days
    weekdays, weekends = count_weekdays_and_weekends(checkin_date, checkout_date)

    # Calculate meal cost
    if(accommodation == 'luxury'):
        total_meal_cost = len(meals) * luxury_meal_cost_per_person * num_people
    else:
        total_meal_cost = len(meals) * meal_cost_per_person * num_people * (weekdays + weekends)
        if len(meals) > 1: # Calculate the meals discount if more than 1 meal is added to the package
            # Calculate how much a meal costs during weekdays applying the discount
            meal_cost_per_person_weekdays = meal_cost_per_person * meal_discount_rate_weekdays * len(meals)
            
            # Calculate how much would be the total discount during weekdays
            total_meals_discount_weekdays = meal_cost_per_person_weekdays * num_people * len(meals) * weekdays
            
            # Calculate how much a meal costs during weekends applying the discount
            meal_cost_per_person_weekends = meal_cost_per_person * meal_discount_rate_weekends * len(meals)
            
            # Calculate how much would be the total discount during weekdays
            total_meals_discount_weekdends = meal_cost_per_person_weekends * num_people * len(meals) * weekends
            
            # Calculate the total cost by subtracting the discounts
            total_meal_cost -= (total_meals_discount_weekdends + total_meals_discount_weekdays)
    print(f'The total meals cost is: {total_meal_cost}')
    
    # Calculate tour cost
    total_our_tour_cost = sum(our_tour_costs[tour] * num_people for tour in tours if tour in our_tour_costs)
    total_referral_tour_cost = sum(referrals_tour_costs[tour] * num_people for tour in tours if tour in referrals_tour_costs)
    
    # Calculate the qty of discounts to the referrals tours, every 3 people a discount is added for one tour.
    qty_referrals_discounts = num_people // 3 
    
    # Count how many tours are from the referrals
    num_referrals_tours = sum(1 for tour in tours if tour in referrals_tour_costs)
    
    # Calculate the total cost for the referrals tours
    referrals_tour_discount = qty_referrals_discounts * next(iter(referrals_tour_costs.values())) * tour_referrals_discount 
    total_referral_tour_cost -= referrals_tour_discount
    
    print(f'The total tours cost is: {total_our_tour_cost + total_referral_tour_cost}')
    
    # Calculate accommodation cost
    if num_people <= 2 and accommodation == 'luxury':
        accommodation_cost = accommodation_costs['luxury'] * (weekdays + weekends)
    else:
        accommodation_cost = num_people * accommodation_costs['normal'] * (weekdays + weekends)
    print(f'The total accommodation cost is: {accommodation_cost}')
    
    # Calculate the total cost
    total_cost = total_meal_cost + total_our_tour_cost + total_referral_tour_cost + accommodation_cost

    return total_cost


# Example usage
num_people = 7
meals = []
tours = ['scuba_diving']
total_cost = calculate_travel_package_cost(num_people, '2024-03-28', '2024-04-01', meals, tours)
print("Total cost for the travel package:", total_cost) # Should be $1305