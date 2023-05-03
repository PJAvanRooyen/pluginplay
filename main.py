import threading

from src.node_editor_view.node_editor import NodeEditorApp


def start_app():
    app = NodeEditorApp()
    app.run()


if __name__ == '__main__':
    thread = threading.Thread(target=start_app())
    thread.start()