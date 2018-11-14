from plotly import tools
import plotly.offline as ply
import plotly.graph_objs as go

temp = [20,30,20,10,29]

xass = []
for i in range(len(temp)):
    xass.append(i * 3)

temperatuur = go.Scatter(
    x= xass,
    y= temp)

licht = go.Scatter(
    x= xass,
    y=[50, 60, 70])

afstand = go.Scatter(
    x= xass,
    y=[600, 700, 800])


fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('Temperatuur', 'licht', 'afstand'))

fig.append_trace(temperatuur, 1, 1)
fig.append_trace(licht, 2, 1)
fig.append_trace(afstand, 3, 1)


fig['layout'].update(height=600, width=600, title='multi.html')

ply.plot(fig, filename='multi.html')