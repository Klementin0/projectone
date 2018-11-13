import plotly.graph_objs as go
import plotly.offline as ply
#from control import Return_lis



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