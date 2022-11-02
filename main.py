from UIManager import *
import UIManager as UIM

def main():
    app = UIM.App()

    app.create_page("home", "Home")
    app.pages["home"].create_button("Create New Model", button_name = "create_new_model")
    app.pages["home"].create_button("Start Translation", button_name = "start_translation", row=0, column=1)
    app.pages["home"].set_button_callback("create_new_model", 
    lambda:app.show(app.pages["create_new_model"]))
    app.pages["home"].set_button_callback("start_translation", lambda:print("Start Translation"))

    app.create_page("choose_translation_model", "Choose Translation Model")
    


    app.create_page("translation_webcam", "Gesture Translation")
    #! dunno what goes here

    app.create_page("create_new_model", "Create New Model")
    app.pages["create_new_model"].create_button("Import Dataset", "import_dataset")
    app.pages["create_new_model"].create_button("Create Dataset", "create_dataset", column=1)
    app.pages["create_new_model"].create_button("Return", "return", row=1)
    app.pages["create_new_model"].set_button_callback("import_dataset", lambda:print("Import Dataset"))
    app.pages["create_new_model"].set_button_callback("create_dataset", lambda:print("Create Dataset"))
    app.pages["create_new_model"].set_button_callback("return", lambda:app.show(app.pages["home"]))

    app.create_page("preview_dataset", "Preview Dataset")
    app.create_page("create_dataset", "Create Dataset")

    app.create_page("model_settings", "Model Settings")

    app.show(app.pages["home"])
    #app.show(None)
    app.run()

    

    return None


main()