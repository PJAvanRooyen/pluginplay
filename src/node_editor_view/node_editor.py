from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line

from src.node_editor_view.node import Node


class NodeEditor(FloatLayout):
    def __init__(self, **kwargs):
        super(NodeEditor, self).__init__(**kwargs)

        self.nodes = []
        self.line_start_node_interface = None

    def node_touched(self, touch):
        for node in self.nodes:
            if node.touched(touch):
                return node

    def on_touch_down(self, touch):
        super(NodeEditor, self).on_touch_down(touch)

        touched_node = self.node_touched(touch)
        if touched_node is not None:
            touched_node_interface = touched_node.interface_touched(touch)
            if touched_node_interface is not None:
                if 'line' not in touch.ud:
                    with self.canvas:
                        touch.ud['line'] = Line(points=[touched_node_interface.center_x, touched_node_interface.center_y, touched_node_interface.center_x, touched_node_interface.center_y], width=2)
                    self.line_start_node_interface = touched_node_interface
        else:
            self.nodes.append(Node(pos=(touch.x, touch.y)))
            self.add_widget(self.nodes[-1])
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
            touched_node = self.node_touched(touch)
            if touched_node is not None:
                touched_node_interface = touched_node.interface_touched(touch)
                if touched_node_interface is not None and touched_node_interface is not self.line_start_node_interface:
                    is_new_interface = True
                    line_points = touch.ud['line'].points
                    with self.canvas:
                        touch.ud['line'].points = [line_points[0], line_points[1], touched_node_interface.center_x, touched_node_interface.center_y]

            if not is_new_interface:
                self.canvas.remove(touch.ud['line'])

        self.line_start_node_interface = None
        return True

    def on_double_tap(self):
        super(NodeEditor, self).on_double_tap()
        return True


class NodeEditorApp(App):
    def build(self):
        return NodeEditor()