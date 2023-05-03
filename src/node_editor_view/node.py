from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
import os
import importlib
import inspect
import sys


class ConnectionInterface(Widget):
    def __init__(self, member_name, member, pos, size):
        super(ConnectionInterface, self).__init__()
        self.member_name = member_name
        self.member = member
        self.pos = pos
        self.size_hint = (None, None)
        self.size = size
        self.corner_radius = 5

        with self.canvas:
            Color(0, 0.8, 0)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])

        self.label = Label(text=member_name, pos=self.pos, size_hint=(None, None), size=(0,0))
        self.add_widget(self.label)

    def touched(self, touch):
        if self.collide_point(*touch.pos):
            return True


class Node(Widget):
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (40, 40)
        self.corner_radius = 10
        self.edge_length = self.size[1] - 2*self.corner_radius
        self.interface_size = 20
        self.component = None
        self.interfaces = []

        with self.canvas:
            Color(0, 1, 0)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])

        self.label = Label(text="Node", pos=(self.x, self.y - 25), size_hint=(None, None), size=(self.size[0], 25))
        self.add_widget(self.label)

    def set_size(self, size):
        self.size = size
        self.background.size = size

    def touched(self, touch):
        if self.collide_point(*touch.pos):
            return True
        elif self.interface_touched(touch) is not None:
            return True

    def interface_touched(self, touch):
        for interface in self.interfaces:
            if interface.touched(touch):
                return interface
        return None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.component:
                self.set_component()

    def set_component(self):
        scripts_dir = os.path.join(sys.path[0], "scripts")
        scripts = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]

        for script in scripts:
            module_name = os.path.splitext(script)[0]
            module_path = os.path.join(scripts_dir, script)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, cls in module.__dict__.items():
                if isinstance(cls, type):
                    self.label.text = name
                    self.component = cls()
                    class_type = type(self.component)
                    class_members = [member for member in inspect.getmembers(class_type) if not member[0].startswith("_")]
                    member_count = len(class_members)
                    member_idx = 0
                    for member_name, member_value in class_members:
                        self.interfaces.append(ConnectionInterface(member_name=member_name, member=member_value, pos=[self.x - self.interface_size/2, self.y + self.corner_radius + member_idx*self.interface_size], size=[self.interface_size, self.interface_size]))
                        self.add_widget(self.interfaces[-1])
                        member_idx += 1

                        if callable(member_value):
                            try:
                                res = member_value(self.component)
                                self.label.text = res
                            except:
                                pass

                    self.set_size((self.size[0], member_count*self.interface_size + 2*self.corner_radius))
                    return
