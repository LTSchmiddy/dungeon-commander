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

    import interface_flask
    import viewport

    interface_flask.init()
    viewport.create_window(False)
    interface_flask.start_server()

    # launches the main GUI loop:
    viewport.start_window()

    # Shuts down the application:
    print("CLOSED")

    interface_flask.stop_server()
    settings.save_settings()

    sys.exit(0)
