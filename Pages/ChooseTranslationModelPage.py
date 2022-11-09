from Page import Page

def create(app):
    choose_translation_model_page = Page(app.root, "Choose Translation Model")
    choose_translation_model_page.add_button(
            text="Return"
            , callback=lambda: app.show_page(app.home_page)
            , row=1
            , column=0
        )
    choose_translation_model_page.add_label(
            text="Directory"
            , row=0
            , column=0
        )
    choose_translation_model_page.add_entry( row=0, column=1)
    choose_translation_model_page.add_button(
            text="Confirm",
            callback = lambda:print("IMPLEMENT")
            , row=1 
            ,column=1
        )

    return choose_translation_model_page
