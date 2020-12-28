import os
import time
import logging

from h2o_wave import main, app, Q, ui, data
import pandas as pd
import numpy as np


@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        initialize_app_for_new_client(q)

    if q.args.file_upload:
        await handle_uploaded_data(q)

    await q.page.save()


def initialize_app_for_new_client(q):
    """Setup this Wave application for each browser tab by creating a page layout and setting any needed variables"""

    q.page['header'] = ui.header_card(
        box='1 1 11 1',
        title='Using Data',
        subtitle='How to ask the user for datasets and display this data',
    )

    render_upload_view(q)
    render_table_view(q)
    render_plot_view(q)

    # Create a place to hold datasets where you are running wave
    q.client.data_path = './data'
    if not os.path.exists(q.client.data_path):
        os.mkdir(q.client.data_path)

    # Flag that this browser has been prepped
    q.client.initialized = True


def render_upload_view(q: Q):
    """Sets up the upload-dataset card"""
    q.page['upload'] = ui.form_card(
        box='1 2 3 -1',
        items=[
            ui.separator(label='Step 1: Choose a Dataset'),
            ui.message_bar(
                type='info',
                text='This application requires a .csv file with any type of data within it',
            ),
            ui.file_upload(name='file_upload', label='Upload Data', multiple=False, file_extensions=['csv']),
        ]
    )


def render_table_view(q: Q):
    """Sets up the view a file as ui.table card"""

    items = [ui.separator(label='Step 2: View the Dataset')]

    if q.client.working_file_path is None:
        items.append(ui.message_bar(type='warning', text='Please upload a dataset!'))
    else:
        items.append(ui.text_xl(os.path.basename(q.client.working_file_path)))
        items.append(make_ui_table(file_path=q.client.working_file_path, n_rows=10, name='head_of_table'))

    q.page['table'] = ui.form_card(box='4 2 8 4', items=items)


def render_plot_view(q: Q):
    """Sets up the view a file as ui.table card"""

    items = [ui.separator(label='Step 3: Visualize the Dataset')]

    if q.client.working_file_path is None:
        items.append(ui.message_bar(type='warning', text='Please upload a dataset!'))
    else:
        items.append(make_ui_plot(file_path=q.client.working_file_path))

    q.page['plot'] = ui.form_card(box='4 6 8 -1', items=items)


async def handle_uploaded_data(q: Q):
    """Saves a file uploaded by a user from the UI"""
    data_path = q.client.data_path

    # Download new dataset to data directory
    q.client.working_file_path = await q.site.download(url=q.args.file_upload[0], path=data_path)

    # Update views to end user
    render_table_view(q)
    time.sleep(1)  # show the Upload Success for 1 second before refreshing this view
    render_upload_view(q)
    render_plot_view(q)


def make_ui_table(file_path: str, n_rows: int, name: str):
    """Creates a ui.table object from a csv file"""

    df = pd.read_csv(file_path)
    n_rows = min(n_rows, df.shape[0])

    table = ui.table(
        name=name,
        columns=[ui.table_column(name=str(x), label=str(x), sortable=True) for x in df.columns.values],
        rows=[ui.table_row(name=str(i), cells=[str(df[col].values[i]) for col in df.columns.values])
              for i in range(n_rows)]
    )
    return table


def make_ui_plot(file_path: str):
    """Creates a scatter plot from two random columns in the csv file"""
    df = pd.read_csv(file_path)

    col1 = df.columns.tolist()[np.random.randint(0, df.shape[1])]
    col2 = df.columns.tolist()[np.random.randint(0, df.shape[1])]

    df = df.where(pd.notnull(df), None)

    plot = ui.visualization(
        ui.plot(marks=[ui.mark(type='point', x=f'={col1}', y=f'={col2}', x_title=col1, y_title=col2)]),
        data(fields=df.columns.tolist(), rows=df.values.tolist(), pack=True),
    )

    return plot
