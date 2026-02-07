from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.core.clipboard import Clipboard

from gematria_engine import gematria_full


# =========================
# COLORES
# =========================
COLOR_SINGLE = (0.18, 0.45, 0.85, 1)
COLOR_EVENTO = (0.55, 0.25, 0.7, 1)
COLOR_MULTI  = (0.16, 0.65, 0.45, 1)
COLOR_LIGHT  = (0.96, 0.96, 0.96, 1)


# =========================
# CARD
# =========================
class Card(BoxLayout):
    def __init__(self, bg_color, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=18,
            spacing=12,
            size_hint_y=None,
            **kwargs
        )
        self.bind(minimum_height=self.setter("height"))
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(radius=[22])
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size


# =========================
# APP
# =========================
class GematriaApp(App):

    def build(self):
        Window.clearcolor = (0.12, 0.12, 0.12, 1)

        self.tabs = TabbedPanel(do_default_tab=False, tab_height=0)

        # 👉 Crear tabs primero
        self.tab_single = self.single_tab()
        self.tab_evento = self.evento_tab()
        self.tab_multi  = self.multi_tab()
        self.tab_home   = self.home_tab()

        # 👉 Agregar tabs
        for t in [
            self.tab_home,
            self.tab_single,
            self.tab_evento,
            self.tab_multi
        ]:
            self.tabs.add_widget(t)

        self.tabs.switch_to(self.tab_home)
        return self.tabs

    # =========================
    # HOME
    # =========================
    def home_tab(self):
        tab = TabbedPanelItem(text="Home")
        scroll = ScrollView()

        root = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=24,
            size_hint_y=None
        )
        root.bind(minimum_height=root.setter("height"))
        scroll.add_widget(root)

        root.add_widget(Label(
            text="Gematria",
            font_size=28,
            bold=True,
            color=(1,1,1,1)
        ))

        root.add_widget(Label(
            text="Análisis numérico avanzado",
            font_size=15,
            color=(0.8,0.8,0.8,1)
        ))

        # Cards navegación
        for title, color, target in [
            ("Single", COLOR_SINGLE, self.tab_single),
            ("Evento", COLOR_EVENTO, self.tab_evento),
            ("Multi",  COLOR_MULTI,  self.tab_multi),
        ]:
            card = Card(color)
            card.add_widget(Label(text=title, font_size=22, bold=True, color=(1,1,1,1)))
            card.add_widget(Label(text="Entrar", font_size=14, color=(1,1,1,0.9)))
            card.bind(
                on_touch_down=lambda w, t, trg=target:
                self.tabs.switch_to(trg) if w.collide_point(*t.pos) else None
            )
            root.add_widget(card)

        tab.add_widget(scroll)
        return tab

    # =========================
    # SINGLE
    # =========================
    def single_tab(self):
        tab = TabbedPanelItem(text="Single")
        scroll = ScrollView()

        root = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=24,
            size_hint_y=None
        )
        root.bind(minimum_height=root.setter("height"))
        scroll.add_widget(root)

        header = Card(COLOR_SINGLE)
        header.add_widget(Label(text="Single", font_size=22, bold=True, color=(1,1,1,1)))
        root.add_widget(header)

        inp = TextInput(
            hint_text="Texto a analizar",
            multiline=True,
            size_hint_y=None,
            height=140,
            font_size=18
        )

        out = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=None,
            height=260,
            font_size=16
        )

        btn_calc = Button(text="Analizar", size_hint_y=None, height=48)
        btn_copy = Button(text="Copiar resultado", size_hint_y=None, height=44)

        btn_calc.bind(on_press=lambda *_: self.calc_single(inp, out))
        btn_copy.bind(on_press=lambda *_: Clipboard.copy(out.text) if out.text else None)

        root.add_widget(inp)
        root.add_widget(btn_calc)
        root.add_widget(btn_copy)
        root.add_widget(out)

        tab.add_widget(scroll)
        return tab

    def calc_single(self, inp, out):
        text = inp.text.strip()
        if not text:
            out.text = "Ingresa texto."
            return
        out.text = self.format_simple(gematria_full(text))

    # =========================
    # MULTI (hasta 5)
    # =========================
    def multi_tab(self):
        tab = TabbedPanelItem(text="Multi")
        scroll = ScrollView()

        root = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=24,
            size_hint_y=None
        )
        root.bind(minimum_height=root.setter("height"))
        scroll.add_widget(root)

        header = Card(COLOR_MULTI)
        header.add_widget(Label(
            text="Multi (hasta 5 jugadores)",
            font_size=22,
            bold=True,
            color=(1,1,1,1)
        ))
        root.add_widget(header)

        self.multi_input = TextInput(
            hint_text="Una línea por jugador",
            multiline=True,
            size_hint_y=None,
            height=180,
            font_size=18
        )
        root.add_widget(self.multi_input)

        btn = Button(text="Analizar", size_hint_y=None, height=48)
        root.add_widget(btn)

        self.multi_results = BoxLayout(
            orientation="vertical",
            spacing=16,
            size_hint_y=None
        )
        self.multi_results.bind(minimum_height=self.multi_results.setter("height"))
        root.add_widget(self.multi_results)

        btn.bind(on_press=self.calc_multi)

        tab.add_widget(scroll)
        return tab

    def calc_multi(self, *_):
        self.multi_results.clear_widgets()

        players = [
            p.strip()
            for p in self.multi_input.text.replace(",", "\n").splitlines()
            if p.strip()
        ][:5]

        for p in players:
            g = gematria_full(p)

            card = Card(COLOR_LIGHT)
            card.add_widget(Label(text=p.upper(), bold=True, font_size=18, color=(0,0,0,1)))

            out = TextInput(
                text=self.format_simple(g),
                readonly=True,
                multiline=True,
                size_hint_y=None,
                height=160,
                font_size=16
            )

            btn = Button(text="Copiar", size_hint_y=None, height=40)
            btn.bind(on_press=lambda _, t=out.text: Clipboard.copy(t))

            card.add_widget(out)
            card.add_widget(btn)
            self.multi_results.add_widget(card)

    # =========================
    # EVENTO
    # =========================
    def evento_tab(self):
        tab = TabbedPanelItem(text="Evento")
        scroll = ScrollView()

        root = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=24,
            size_hint_y=None
        )
        root.bind(minimum_height=root.setter("height"))
        scroll.add_widget(root)

        header = Card(COLOR_EVENTO)
        header.add_widget(Label(text="Evento", font_size=22, bold=True, color=(1,1,1,1)))
        root.add_widget(header)

        inputs = []
        for h in ["Equipo Local", "Equipo Visitante", "Sede"]:
            ti = TextInput(hint_text=h, size_hint_y=None, height=60, font_size=18)
            inputs.append(ti)
            root.add_widget(ti)

        out = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=None,
            height=260,
            font_size=16
        )

        btn_calc = Button(text="Analizar", size_hint_y=None, height=48)
        btn_copy = Button(text="Copiar resultado", size_hint_y=None, height=44)

        btn_calc.bind(on_press=lambda *_: self.calc_evento(inputs, out))
        btn_copy.bind(on_press=lambda *_: Clipboard.copy(out.text) if out.text else None)

        root.add_widget(btn_calc)
        root.add_widget(btn_copy)
        root.add_widget(out)

        tab.add_widget(scroll)
        return tab

    def calc_evento(self, inputs, out):
        if not all(i.text.strip() for i in inputs):
            out.text = "Completa todos los campos."
            return

        out.text = self.format_comparativo(
            gematria_full(inputs[0].text),
            gematria_full(inputs[1].text),
            gematria_full(inputs[2].text)
        )

    # =========================
    # FORMATOS
    # =========================
    def format_simple(self, g):
        return (
            f"O   : {g['O']}\n"
            f"DR  : {g['DR']}\n"
            f"LR  : {g['LR']}\n"
            f"REV : {g['REV']}\n"
            f"RR  : {g['RR']}\n"
            f"RLR : {g['RLR']}"
        )

    def format_comparativo(self, h, a, v):
        txt = "VALOR | LOCAL | VISITA | SEDE\n"
        txt += "-" * 34 + "\n"
        for k in ["O","DR","LR","REV","RR","RLR"]:
            txt += f"{k:<4} | {h[k]} | {a[k]} | {v[k]}\n"
        return txt


if __name__ == "__main__":
    GematriaApp().run()