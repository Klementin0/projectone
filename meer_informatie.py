import plotly.graph_objs as go
import plotly.offline as ply
import serial_se_re

serialPort = serial_se_re.SerialPort()
serialPort.Open("COM3",19200)

i = 0
while i < 5:
    serialPort.Lees()
    i += 1

lis = serialPort.Return_lis()

temp = [20,21,20,19,20,21,23,55,23,65]

#X-ass maken met intervallen van 3
numbers = []
for i in range(len(temp)):
   numbers.append(i * 3)

# Create a trace
trace = go.Scatter(
    x = numbers,
    y = temp
)
data = [trace]

ply.plot(data, filename='grafiek.html')

print(lis)