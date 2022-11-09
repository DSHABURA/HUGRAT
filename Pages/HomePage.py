from Page import Page

def create(app):
    home_page = Page(app.root, "HUGRAT")

    home_page.add_button(
        text="Create Model"
        , callback=lambda: app.show_page(app.new_model_page)
        , row=0
        , column=0)
    
    home_page.add_button(
        text="Start Translation"
        , callback=lambda: app.show_page(app.choose_translation_model_page)
        , row=0
        , column=1)


    return home_page

