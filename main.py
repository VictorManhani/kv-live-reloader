from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock

from kivy.core.window import Window
Window.size = (600, 500)

class Editor(Factory.BoxLayout):
    evt = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down = self._keydown)

    def reloader(self, texto):
        self.ids.container.clear_widgets()
        try:
            wids = Builder.load_string(texto)
            self.ids.container.add_widget(wids)
        except Exception as e:
            info = Factory.Label(text = str(e))
            self.ids.container.add_widget(info)

    def _keydown(self, window, keycode, key, char, modifiers):
        if 'ctrl' in modifiers and char == 's':
            self.reloader(self.ids.code.text)

    def start_rendering(self):
        render = lambda evt: self.reloader(self.ids.code.text)
        self.evt = Clock.schedule_interval(render, 1)

    def stop_rendering(self):
        Clock.unschedule(self.evt)

class MainApp(App):
    def build(self):
        return Builder.load_string("""
#:import KivyLexer kivy.extras.highlight.KivyLexer

Editor:
    orientation: "vertical"
    BoxLayout:
        orientation: "horizontal"
        size_hint: [1,.1]
        Label:
            text: "reloader?"
            size_hint: [.3,1]
        CheckBox:
            size_hint: [.7,1]
            on_active:
                root.start_rendering() if self.active else root.stop_rendering()
    BoxLayout:
        orientation: "horizontal"
        size_hint: [1,.9]
        CodeInput:
            id: code
            text: "Button:"
            style: "monokai"
            background_color: [.2,.2,.2,1]
            lexer: KivyLexer()
            size_hint: [.6, 1]
            # on_text:
            #     root.reloader(self.text)
        BoxLayout:
            id: container
            orientation: "vertical"
            size_hint: [.4, 1]
""")

MainApp().run()