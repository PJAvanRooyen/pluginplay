from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line
import os
import shutil

from src.node_editor_view.node import Node


class NodeEditor(FloatLayout):
    def __init__(self, **kwargs):
        super(NodeEditor, self).__init__(**kwargs)

        self.nodes = []
        self.line_start_node_interface = None

    def on_drop_file(self, window, file_path, x, y):
        file_path = file_path.decode("utf-8")
        filename = os.path.basename(file_path)
        scripts_dir = os.path.join(os.getcwd(), "scripts")
        destination = os.path.join(scripts_dir, filename)
        try:
            if filename.endswith(".py"):
                if not os.path.exists(destination):
                    shutil.copy(file_path, destination)
                name, suffix = os.path.splitext(filename)

                node = self.create_node((x, y))
                node.get_components()
                node.configure(name)

                print(f"File saved to: {destination}")
            else:
                print("Invalid file")

        except Exception as e:
            print(f"Error: {e}")

    def touched_node(self, touch):
        for node in self.nodes:
            if node.touched(touch):
                return node

    def on_touch_down(self, touch):
        super(NodeEditor, self).on_touch_down(touch)

        touched_node = self.touched_node(touch)
        if touched_node is not None:
            touched_node_method = touched_node.touched_method(touch)
            if touched_node_method is not None:
                touched_node_interface = touched_node_method.touched_interface(touch)
                if touched_node_interface is not None:
                    if 'line' not in touch.ud:
                        with self.canvas:
                            touch.ud['line'] = Line(points=[touched_node_interface.center_x, touched_node_interface.center_y, touched_node_interface.center_x, touched_node_interface.center_y], width=2)
                        self.line_start_node_interface = touched_node_interface
        else:
            self.create_node((touch.x, touch.y))
        return True

    def on_touch_move(self, touch):
        super(NodeEditor, self).on_touch_move(touch)

        if 'line' in touch.ud:
            line_points = touch.ud['line'].points
            with self.canvas:
                touch.ud['line'].points = [line_points[0], line_points[1], touch.pos[0], touch.pos[1]]
        return True

    def on_touch_up(self, touch):
        super(NodeEditor, self).on_touch_up(touch)

        if 'line' in touch.ud:
            is_new_interface = False
            touched_node = self.touched_node(touch)
            if touched_node is not None:
                touched_node_method = touched_node.touched_method(touch)
                if touched_node_method is not None:
                    touched_node_interface = touched_node_method.touched_interface(touch)
                    if touched_node_interface is not None:
                        if touched_node_interface is not None and touched_node_interface is not self.line_start_node_interface:
                            is_new_interface = True
                            self.line_start_node_interface.add_connected_interface(touched_node_interface)
                            touched_node_interface.add_connected_interface(self.line_start_node_interface)

                            line_points = touch.ud['line'].points
                            with self.canvas:
                                touch.ud['line'].points = [line_points[0], line_points[1], touched_node_interface.center_x, touched_node_interface.center_y]

            if not is_new_interface:
                self.canvas.remove(touch.ud['line'])

        self.line_start_node_interface = None
        return True

    def create_node(self, pos):
        self.nodes.append(Node(pos=pos))
        self.add_widget(self.nodes[-1])
        return self.nodes[-1]


class NodeEditorApp(App):
    def build(self):
        layout = NodeEditor()
        Window.bind(on_drop_file=layout.on_drop_file)
        return layout