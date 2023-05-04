from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
import os
import importlib
import inspect
import sys


class Interface(Widget):
    def __init__(self, param_name, param_type, pos):
        super(Interface, self).__init__()
        self.param_name = param_name
        self.param_type = param_type
        self.init_value = self.default_value_for_type(param_type)
        self.pos = pos
        self.size_hint = (None, None)
        self.size = (20, 20)
        self.corner_radius = 5

        with self.canvas:
            Color(0, 0.6, 0)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])

        self.label = Label(text=param_name, pos=(self.pos[0], self.pos[1] - 10), size_hint=(None, None), size=self.size)
        self.add_widget(self.label)

    def default_value_for_type(self, param_type):
        if param_type is inspect.Parameter.empty:
            return 0
        elif param_type is int:
            return 0
        elif param_type is str:
            return ''
        elif param_type is list:
            return []
        else:
            return None

    def touched(self, touch):
        if self.collide_point(*touch.pos):
            return True


class Method(Widget):
    def __init__(self, pos):
        super(Method, self).__init__()
        self.name = "Method"
        self.method = None
        self.input_interfaces = []
        self.output_interfaces = []
        self.pos = pos
        self.size_hint = (None, None)
        self.size = (30, 30)
        self.return_param = None
        self.corner_radius = 5
        self.interface_x_offset = 5

        with self.canvas:
            Color(0, 0.8, 0)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius])

        self.label = Label(text="Method", pos=(self.pos[0] + self.size[0], self.pos[1] + self.size[1]/2), size_hint=(None, None), size=(0,0))
        self.add_widget(self.label)

    def set_method(self, name, method, parameters, return_param):
        for interface in self.input_interfaces:
            self.remove_widget(interface)
        for interface in self.output_interfaces:
            self.remove_widget(interface)

        self.name = name
        self.label.text = self.name
        self.method = method
        self.return_param = None
        self.size[0] = self.parent.size[0] + 2*self.parent.method_x_offset

        input_height = 0
        input_idx = 0
        for parameter in parameters:
            input_interface_pos = [self.x - self.interface_x_offset, self.y + self.corner_radius + input_height]
            param_type = parameter.annotation
            param = Interface(param_name=parameter.name, param_type=param_type, pos=input_interface_pos)
            self.input_interfaces.append(param)
            self.add_widget(param)

            input_height += param.size[1]
            input_idx += 1

        output_height = 0
        output_idx = 0
        if return_param is not inspect.Parameter.empty:
            output_interface_pos = [self.x + self.size[0] - self.interface_x_offset, self.y + self.corner_radius + output_height]
            self.return_param = Interface(param_name=param_type.__name__, param_type=param_type, pos=output_interface_pos)
            self.output_interfaces.append(self.return_param)
            self.add_widget(self.return_param)

            output_height += self.return_param.size[1]
            output_idx += 1

        self.set_size((self.size[0], max(input_height, output_height) + 2*self.corner_radius))

    def set_size(self, size):
        self.size = size
        self.background.size = size
        self.label.pos = (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2)

    def touched(self, touch):
        if self.collide_point(*touch.pos):
            return True
        elif self.touched_interface(touch) is not None:
            return True
        
    def touched_interface(self, touch):
        for interface in self.input_interfaces:
            if interface.touched(touch):
                return interface
        for interface in self.output_interfaces:
            if interface.touched(touch):
                return interface
        return None

    def run(self):
        if callable(self.method):
            try:
                # Default construct a value for each parameter type found
                args = []
                for parameter in self.input_interfaces:
                    args.append(parameter.init_value)

                res = self.method(self.parent.component, *args)
                self.label.text = str(res)
            except:
                pass


class Node(Widget):
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 40)
        self.corner_radius = 10
        self.edge_length = self.size[1] - 2*self.corner_radius
        self.component = None
        self.methods = []

        self.method_x_offset = 10

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
        elif self.touched_method(touch) is not None:
            return True
        else:
            for method in self.methods:
                if method.touched_interface(touch) is not None:
                    return True

    def touched_method(self, touch):
        for method in self.methods:
            if method.touched(touch):
                return method
        return None

    def on_touch_down(self, touch):
        super(Node, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.set_component()
            else:
                self.run()

    def run(self):
        for interface in self.methods:
            interface.run()

    def set_component(self):
        # reset
        self.component = None
        for interface in self.methods:
            self.remove_widget(interface)
        self.methods = []

        # set component
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

                    member_idx = 0
                    height = 0
                    for member_name, method in class_members:
                        signature = inspect.signature(method)
                        parameters = [param for param in signature.parameters.values() if param.name is not "self"]
                        return_param = signature.return_annotation

                        interface_pos = [self.x - self.method_x_offset, self.y + self.corner_radius + height]
                        interface = Method(pos=interface_pos)
                        self.methods.append(interface)
                        self.add_widget(interface)
                        interface.set_method(name=member_name, method=method, parameters=parameters, return_param=return_param)

                        height += interface.size[1]
                        member_idx += 1

                    self.set_size((self.size[0], height + 2*self.corner_radius))
                    return
