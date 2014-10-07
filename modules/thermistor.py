#!/usr/bin/env python
#
#
#
"""
This file contains useful calculations for thermistors.
"""
# import modules
import math

def calcSteinhartHartConstants(data):
    """
    Calculates the Steinhart-Hart Equation constants based upon 3 temperature/resistance test points.
    The temperature is in Celcius and the resistance is in ohms.
    The function arguments are contained within a dictionary.
    The Steinhart-Hart constants are returned in a dictionary.

    Example:
    thermistor_data = { 'temp_c_low': 10, 'temp_r_low': 58750,
                        'temp_c_mid': 25, 'temp_r_mid': 30000,
                        'temp_c_high': 40, 'temp_r_high': 16150}

    thermistor_steinhart_constants = calcSteinhartHartConstants(thermistor_data)
    """

    data['temp_k_low'] = data['temp_c_low'] + 273.15
    data['temp_k_mid'] = data['temp_c_mid'] + 273.15
    data['temp_k_high'] = data['temp_c_high'] + 273.15

    diff_log_low_med = math.log(data['temp_r_low']) - math.log(data['temp_r_mid'])
    diff_log_low_high = math.log(data['temp_r_low']) - math.log(data['temp_r_high'])
    diff_temp_low_mid = (1 / data['temp_k_low']) - (1 / data['temp_k_mid'])
    diff_temp_low_high = (1 / data['temp_k_low']) - (1 / data['temp_k_high'])

    # print diff_temp_low_mid, diff_temp_low_high
    # print diff_log_low_med, diff_log_low_high

    sh_c = ((diff_temp_low_mid - (diff_log_low_med * (diff_temp_low_high/diff_log_low_high))) /
            ((math.log(data['temp_r_low'])**3 - math.log(data['temp_r_mid'])**3) -
            (diff_log_low_med * (math.log(data['temp_r_low'])**3 - math.log(data['temp_r_high'])**3) / diff_log_low_high)))

    sh_b = (diff_temp_low_mid - (sh_c * (math.log(data['temp_r_low'])**3 - math.log(data['temp_r_mid'])**3))) / diff_log_low_med

    sh_a = (1 / data['temp_k_low']) - (sh_c * math.log(data['temp_r_low'])**3) - (sh_b * math.log(data['temp_r_low']))

    # print "A = ", sh_a, "; B =", sh_b,"; C =", sh_c
    return {'sh_a': sh_a, 'sh_b': sh_b, 'sh_c': sh_c}




def calcThermistorTemp(resistance, sh_a, sh_b, sh_c):
    """
    Calculates the temperature (in Degrees C) measured by the thermistor.

    Example:
        temp = calcThermistorTemp(resistance, A, B, C)
    """
    # offset = -273.15

    # T1 = sh_a + (sh_b * math.log(resistance)) + (sh_c * (math.log(resistance))**3)
    # T1 = (1 / T1) + offset
    # return T1

    return (1 / (sh_a + (sh_b * math.log(float(resistance))) + (sh_c * math.log(float(resistance))**3))) - 273.15




def calcThermistorRes(temperature, sh_a, sh_b, sh_c):
    """
    Calculates the resistance of a thermistor for a specific temperature

    Example:
        resistance = calcThermistorRes(temperature, A, B, C)
    """

    temperature += 273.15
    alpha = (sh_a - (1 / temperature)) / sh_c
    beta = math.sqrt(((sh_b / (3 * sh_c))**3) + ((alpha**2)/4))

    # print 'alpha:', alpha, 'beta:', beta

    resistance = math.exp(((beta - (alpha/2))**(1.0/3)) - ((beta + (alpha/2))**(1.0/3)))
    return resistance


def calcThermistorBridge(voltage_measured, voltage_excitation, bridge_resistor, sh_a, sh_b, sh_c):
    """
    Calculates the temperature of alpha thermistor when used in a half bridge circuit.
    Measured Voltage and Excitation Voltage need to have the same units.

    Example:
        temp = calcThermistorBridge(voltage_measured, voltage_excitation, bridge_resistor, A, B, C)
    """
    therm_resistance = (bridge_resistor * (voltage_measured / voltage_excitation)) / (1 - (voltage_measured / voltage_excitation))

    return calcThermistorTemp(therm_resistance, sh_a, sh_b, sh_c)




if __name__ == '__main__':
    # thermistor_data = { 'temp_c_low': -40, 'temp_r_low': 884600,
    #                     'temp_c_mid': 25, 'temp_r_mid': 30000,
    #                     'temp_c_high': 150, 'temp_r_high': 550200}


    # A = 9.26e-04, B = 2.22e-04, C = 1.23e-07
    thermistor_data = { 'temp_c_low': 10, 'temp_r_low': 58750,
                        'temp_c_mid': 25, 'temp_r_mid': 30000,
                        'temp_c_high': 40, 'temp_r_high': 16150}

    thermistor_steinhart_constants = calcSteinhartHartConstants(thermistor_data)

    print 'The Steinhart-Hart constants are: ',thermistor_steinhart_constants

    # calc_temp = calcThermistorTemp(30000, .0009376, .0002208, .0000001276)
    calc_temp = calcThermistorTemp(30000, 9.376e-4, 2.208e-4, 1.276e-7)
    print 'Temperature for Omega Thermistor @ 30kOhms is 25 Deg C, Calculated Temp is:', calc_temp

    # calc_res = calcThermistorRes(25, .0009376, .0002208, .0000001276)
    calc_res = calcThermistorRes(25, 9.376e-4, 2.208e-4, 1.276e-7)
    print 'Resistance for Omega Thermistor @ 25 Deg C is 30k, Calculated Res is:', calc_res

    # brige_temp = calcThermistorBridge(2.31858, 5, 24900, .0009376, .0002208, .0000001276)
    brige_temp = calcThermistorBridge(2.31858, 5, 24900, 9.376e-4, 2.208e-4, 1.276e-7)
    print 'Expected Temperature: 32.91281, Calculated Temperature is:', brige_temp
