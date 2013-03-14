def convert_mileage(miles_per_gallon):
    # This function converts miles per gallon to liters per 100 kilometers
    # 1 mile = 1.609344 kilometers
    # 100 kilometers = 62.1371192237334 miles
    # 1 gallon = 3.785411784 liters

    mi_to_km = 1.609344
    gallon_to_liter = 3.785411784

    return 1 / (miles_per_gallon * (1 / gallon_to_liter) * mi_to_km)


def liters_needed(distance_traveled_km, gas_mileage_mpg):
    gas_mileage_lpkm = convert_mileage(gas_mileage_mpg)
    return distance_traveled_km * gas_mileage_lpkm

print liters_needed(100, 30)
