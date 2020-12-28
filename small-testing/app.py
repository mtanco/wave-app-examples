from h2o_wave import ui, app, Q, main, data
import pandas as pd
import numpy as np


@app('/')
async def serve(q: Q):
    # make_table(q)
    # show_another_website(q)
    # plot_card(q)
    # plotting_data(q)
    missing_value_plots(q)
    await q.page.save()


def make_table(q: Q):
    n = 10
    q.client.df = pd.DataFrame({'length': np.random.rand(n),
                                'width': np.random.rand(n),
                                'data_type': np.random.choice(a=['Train', 'Test'], size=n, p=[0.8, 0.2])
                                })

    table = ui.table(
        name='my_table',
        columns=[ui.table_column(name=x, label=x) for x in q.client.df.columns.tolist()],
        rows=[ui.table_row(name=i, cells=q.client.df.values[i].tolist()) for i in range(n)]
    )

    q.page['show_table'] = ui.form_card(box='1 1 6 6', items=[table])


def show_another_website(q: Q):

    q.page['show_table'] = ui.form_card(box='1 1 -1 -1', items=[
        ui.frame(path='https://example.com', height='100%')
    ])


def plotting_data(q: Q):
    n = 100
    df = pd.DataFrame({'length': np.random.rand(n),
                       'width': np.random.rand(n),
                       'data_type': np.random.choice(a=['Train', 'Test'], size=n, p=[0.8, 0.2])
                       })

    plot_marks = [ui.mark(type='point', x='=length', x_title='Length (cm)', y='=width', y_title='Width (cm)',
                          color='=data_type', shape='circle')]

    q.page['scatter_plot_card'] = ui.plot_card(
        box='1 1 4 4',
        title='Scatter Plot from Dataframe',
        data=data(
            fields=df.columns.tolist(),
            rows=df.values.tolist(),
            pack=True  # Not required
        ),
        plot=ui.plot(marks=plot_marks)
    )

    q.page['scatter_viz_form_card'] = ui.form_card(
        box='1 5 4 4',
        items=[ui.visualization(
                plot=ui.plot(marks=plot_marks
                             ),
                data=data(
                    fields=df.columns.tolist(),
                    rows=df.values.tolist(),
                    pack=True  # required
                ),
        )]
    )


def missing_value_plots(q: Q):
    plot1 = ui.visualization(
        ui.plot(marks=[ui.mark(type='point', x=f'=col1', y=f'=col1', color='red', shape='circle', size=10)]),
        data(fields=['col1'], rows=[[1], [2], [3]], pack=True),
        height='20%', width='90%',
    )

    # This works
    plot2 = ui.visualization(
        ui.plot(marks=[ui.mark(type='point', x=f'=col1', y=f'=col1', color='red', shape='circle', size=10)]),
        data(fields=['col1'], rows=[[None], [2], [3]], pack=True),
        height='20%', width='90%',
    )

    # This fails
    # plot3 = ui.visualization(
    #     ui.plot(marks=[ui.mark(type='point', x=f'=col1', y=f'=col1', color='red', shape='circle', size=10)]),
    #     data(fields=['col1'], rows=[[np.nan], [2], [3]], pack=True),
    #     height='20%', width='90%',
    # )

    q.page['plots'] = ui.form_card(
        box='1 1 5 -1',
        items=[plot1, plot2]
    )
