from h2o_wave import main, app, Q, ui


@app('/')
async def serve(q: Q):
    """This function will route the user based on how they have interacted with the application."""

    # called the first time this browser comes to this app, including refreshes
    if not q.client.initialized:
        initialize_app_for_new_client(q)

    # called any time one of the tabs is clicked
    elif q.args.header_tabs:
        q.client.tab = q.args.header_tabs  # remember which tab was clicked by this browser

    # called any time the counter button is clicked
    elif q.args.button:
        q.client.count += 1
        q.user.count += 1
        q.app.count += 1

    render_content_changes(q)
    await q.page.save()


def initialize_app_for_new_client(q):
    """Setup this Wave application for each browser tab by creating a page layout and setting any needed variables"""

    if not q.user.initialized:
        initialize_app_for_new_user(q)

    # Default settings for new browsers
    q.client.tab = 'home'
    q.client.count = 0

    # Adding ui elements
    q.page['header'] = ui.header_card(
        box='1 1 11 1',
        title='Exploring Routing',
        subtitle='This application uses tabs and buttons.',
    )

    q.client.initialized = True


def initialize_app_for_new_user(q):
    if not q.app.initialized:
        initialize_app(q)

    q.user.count = 0
    q.user.initialized = True


def initialize_app(q):
    q.app.count = 0
    q.app.initialized = True


def render_content_changes(q: Q):

    q.page['sidebar'] = ui.form_card(
        box='1 2 2 8',
        items=[
            ui.separator('Button Counting'),
            ui.text(f'This button has been **clicked in this browser session {q.client.count}** times!'),
            ui.text(f'This button has been **clicked by you {q.user.count}** times!'),
            ui.text(f'This button has been **clicked {q.app.count}** times!'),
            ui.buttons([ui.button(name='button', label='Click Me!')], justify='center')
        ]
    )

    q.page['content'] = ui.form_card(
        box='3 2 9 8',
        items=[
            ui.tabs(
                name='header_tabs',
                value=q.client.tab,
                items=[ui.tab(name=t.lower(), label=t) for t in ['Home', 'Learn More', 'Contact Us']]
            ),
            ui.frame(content=f'This is the {q.client.tab} section, it is still in development.')
        ]
    )