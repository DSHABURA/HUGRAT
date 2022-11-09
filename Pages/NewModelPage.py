from Page import Page

def create(app):
    new_model_page = Page(app.root, "New Model Setup")
    new_model_page.add_button(
        text="Import Dataset"
        , callback = lambda:app.show_page(app.model_from_existing_dataset_page)
        , row=0
        , column=0
    )
    new_model_page.add_button(
        text="Create Dataset"
        , callback = lambda:app.show_page(app.model_from_new_dataset_page)
        , row=0
        , column=1
    )
    new_model_page.add_button(
        text="Return"
        , callback=lambda: app.show_page(app.home_page)
        , row=1
        , column=0
    )

    return new_model_page

