from plotly import tools
import plotly.offline as ply
import plotly.graph_objs as go


def maak_grafiek(temp,licht,afstand):

    xass_temp = []
    tijd = 1
    for i in range(len(temp)):
        xass_temp.append(i * tijd)

    xass_licht = []
    for i in range(len(licht)):
        xass_licht.append(i * tijd)

    xass_afstand = []
    for i in range(len(afstand)):
        xass_afstand.append(i * tijd)

    temperatuur = go.Scatter(
        x=xass_temp,
        y=temp,
        name = 'Temperatuur'
    )

    licht = go.Scatter(
        x=xass_licht,
        y=licht,
        name = 'Licht'
    )
    afstand = go.Scatter(
        x=xass_afstand,
        y=afstand,
        name = 'Afstand'
    )

    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('Temperatuur', 'licht', 'afstand'))

    fig.append_trace(temperatuur, 1, 1)
    fig.append_trace(licht, 2, 1)
    fig.append_trace(afstand, 3, 1)

    fig['layout'].update(height=600, width=600, title='Gegevens zonnescherm:')

    ply.plot(fig, filename='grafiek.html')
