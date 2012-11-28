#Wind Speed Back Calculation
#U = Mx + B
#U = Wind Speed (m/s)

M = [0.8000, 0.7989]
B = [0.447, 0.28]
x = []

#MetOne 014A
#M[0] = 0.8000 m/s/pulse
#B[0] = 0.447 m/s

#MetOne 034B
#M[1] = 0.7989 m/s/pulse
#B[1] = 0.28 m/s


#CAISO Wind Speed must measured with accuracy of 1 m/s
U = 0.11

for counter in range(0, 2):
  x[counter] = (U - B[counter]) / M[counter]
  print x[counter]
