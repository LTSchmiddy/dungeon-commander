import sys
import multiprocessing
import settings.paths

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()

    import std_handler
    std_handler.init()

    settings.load_settings()

    # import generate_py_api
    # generate_py_api.rebuild_api()

    import game
    game.start()

    import interface_flask
    import viewport
    import db
    db.init()
    if settings.current['game']["reload-db-on-start"]:
        db.load_db.load_all()



    interface_flask.init()
    viewport.create_main_window(False)
    interface_flask.start_server()

    # launches the main GUI loop:
    viewport.start_viewport()

    # Shuts down the application:
    print("CLOSED")
    game.current.save_campaign()

    interface_flask.stop_server()
    settings.save_settings()

    sys.exit(0)
