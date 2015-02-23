#!/usr/bin/env python
#
#
#
"""
"""
# import modules
import math

class thermistor:
    """useful calculations for thermistors."""
    def __init__(self, sh_a, sh_b, sh_c):
        # super(ClassName, self).__init__()
        self.sh_a = sh_a
        self.sh_b = sh_b
        self.sh_c = sh_c


    def calcSteinhartHartConstants(self, data):
        """
        Calculates the Steinhart-Hart Equation constants based upon 3 temperature/resistance test points.
        The temperature is in Celcius and the resistance is in ohms.
        The function arguments are contained within a dictionary.
        The Steinhart-Hart constants are returned in a dictionary.

        Example:
        thermistor_data = { 'temp_c_low': 10, 'temp_r_low': 58750,
                            'temp_c_mid': 25, 'temp_r_mid': 30000,
                            'temp_c_high': 40, 'temp_r_high': 16150}

        t1 = Thermistor(9.376e-4, 2.208e-4, 1.276e-7)
        thermistor_steinhart_constants = t1.calcSteinhartHartConstants(thermistor_data)
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

        self.sh_c = ((diff_temp_low_mid - (diff_log_low_med * (diff_temp_low_high/diff_log_low_high))) /
                ((math.log(data['temp_r_low'])**3 - math.log(data['temp_r_mid'])**3) -
                (diff_log_low_med * (math.log(data['temp_r_low'])**3 - math.log(data['temp_r_high'])**3) / diff_log_low_high)))

        self.sh_b = (diff_temp_low_mid - (self.sh_c * (math.log(data['temp_r_low'])**3 - math.log(data['temp_r_mid'])**3))) / diff_log_low_med

        self.sh_a = (1 / data['temp_k_low']) - (self.sh_c * math.log(data['temp_r_low'])**3) - (self.sh_b * math.log(data['temp_r_low']))

        # print "A = ", self.sh_a, "; B =", self.sh_b,"; C =", self.sh_c
        return {'sh_a': self.sh_a, 'sh_b': self.sh_b, 'sh_c': self.sh_c}




    def calcTemp(self, resistance):
        """
        Calculates the temperature (in Degrees C) measured by the thermistor.

        Example:
            temp = calcTemp(resistance)
        """
        # offset = -273.15

        # T1 = self.sh_a + (self.sh_b * math.log(resistance)) + (self.sh_c * (math.log(resistance))**3)
        # T1 = (1 / T1) + offset
        # return T1

        return (1 / (self.sh_a + (self.sh_b * math.log(float(resistance))) + (self.sh_c * math.log(float(resistance))**3))) - 273.15




    def calcResistance(self, temperature):
        """
        Calculates the resistance of a thermistor for a specific temperature

        Example:
            t1 = Thermistor(9.376e-4, 2.208e-4, 1.276e-7)
            resistance = t1.calcResistance(temperature)
        """

        temperature += 273.15
        alpha = (self.sh_a - (1 / temperature)) / self.sh_c
        beta = math.sqrt(((self.sh_b / (3 * self.sh_c))**3) + ((alpha**2)/4))

        # print 'alpha:', alpha, 'beta:', beta

        resistance = math.exp(((beta - (alpha/2))**(1.0/3)) - ((beta + (alpha/2))**(1.0/3)))
        return resistance


    def calcThermistorBridge(self, voltage_measured, voltage_excitation, bridge_resistor):
        """
        Calculates the temperature of alpha thermistor when used in a half bridge circuit.
        Measured Voltage and Excitation Voltage need to have the same units.

        Example:
            t1 = Thermistor(9.376e-4, 2.208e-4, 1.276e-7)
            temp = t1.calcThermistorBridge(voltage_measured, voltage_excitation, bridge_resistor)
        """
        therm_resistance = (bridge_resistor * (voltage_measured / voltage_excitation)) / (1 - (voltage_measured / voltage_excitation))

        return self.calcTemp(therm_resistance)




if __name__ == '__main__':

    t1 = thermistor(9.376e-4, 2.208e-4, 1.276e-7)
    t2 = thermistor(.0009376, .0002208, .0000001276)
    # thermistor_data = { 'temp_c_low': -40, 'temp_r_low': 884600,
    #                     'temp_c_mid': 25, 'temp_r_mid': 30000,
    #                     'temp_c_high': 150, 'temp_r_high': 550200}


    # A = 9.26e-04, B = 2.22e-04, C = 1.23e-07
    thermistor_data = { 'temp_c_low': 10, 'temp_r_low': 58750,
                        'temp_c_mid': 25, 'temp_r_mid': 30000,
                        'temp_c_high': 40, 'temp_r_high': 16150}

    thermistor_steinhart_constants = t1.calcSteinhartHartConstants(thermistor_data)

    print 'The Steinhart-Hart constants are: ', thermistor_steinhart_constants

    calc_temp = t1.calcTemp(30000)
    # calc_temp = t2.calcTemp(30000)
    print 'Temperature for Omega Thermistor @ 30kOhms is 25 Deg C, Calculated Temp is:', calc_temp

    calc_res = t1.calcResistance(25)
    # calc_res = t2.calcResistance(25)
    print 'Resistance for Omega Thermistor @ 25 Deg C is 30k, Calculated Res is:', calc_res

    brige_temp = t1.calcThermistorBridge(2.31858, 5, 24900)
    # brige_temp = t2.calcThermistorBridge(2.31858, 5, 24900)
    print 'Expected Temperature: 32.91281, Calculated Temperature is:', brige_temp
