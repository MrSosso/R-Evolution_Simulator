import tkinter as tk


class BaseFrame(tk.Frame):
    WIDGETS = None

    def __init__(self, father, kwargs):
        super(BaseFrame, self).__init__(father)
        self._widgets_load()
        self.grid(**kwargs)

    def _widgets_load(self):
        self.widgets = dict()
        for i in self.WIDGETS:
            new = self.WIDGETS[i][0](self, **self.WIDGETS[i][1])
            new.pack(**self.WIDGETS[i][2])
            self.widgets[i] = new


class Load(BaseFrame):
    def __init__(self, father, kwargs):
        self.WIDGETS = {'entry': (tk.Entry, {}, {}),
                        'button': (tk.Button, {'text': "Load", 'command': father.simulation_file_load}, {'side': tk.RIGHT}),
                        'label': (tk.Label, {'text': "Insert simulation name"}, {'side': tk.LEFT})}
        super(Load, self).__init__(father, kwargs)


class PlayControl(BaseFrame):
    def __init__(self, father, kwargs):
        self.WIDGETS = {'play': (tk.Button, {'text': "Play", 'command': father.start_play}, {'side': tk.LEFT}),
                        'fps': (tk.Label, {'text': "fps: 00.0"}, {'side': tk.LEFT}),
                        'tick_entry': (tk.Spinbox, {'from_': 1, 'to': father.canvas.max_tick, 'width': 15}, {'side': tk.LEFT}),
                        'tick_button': (tk.Button, {'text': "Set tick", 'command': father.set_tick}, {'side': tk.LEFT}),
                        'tick_label': (tk.Label, {'text': "Tick: 1"}, {'side': tk.LEFT}),
                        'speed_label': (tk.Label, {'text': f"Tick/s: {father.canvas.speed}"}, {'side': tk.LEFT}),
                        'speed_slider': (tk.Scale, {'orient': tk.HORIZONTAL, 'showvalue': False, 'command': father.speed_change}, {'side': tk.LEFT}),
                        'dec_zoom': (tk.Button, {'text': "- 10%", 'command': father.dec_zoom}, {'side': tk.LEFT}),
                        'zoom': (tk.Label, {'text': f"zoom: {father.canvas.zoom}0%"}, {'side': tk.LEFT}),
                        'inc_zoom': (tk.Button, {'text': "+ 10%", 'command': father.inc_zoom}, {'side': tk.LEFT}), }
        super(PlayControl, self).__init__(father, kwargs)


class BaseSetFrame(tk.LabelFrame, BaseFrame):
    def __init__(self, father):
        super(BaseSetFrame, self).__init__(father, text=self.NAME)
        self._widgets_load()


class BaseVariableFrame():
    def __init__(self, father):
        for i in self.WIDGETS:
            if self.WIDGETS[i][0] == tk.RADIOBUTTON:
                self.WIDGETS[i][1]['variable'] = self.father.canvas.shows[self.CODE]
                self.WIDGETS[i][1]['command'] = father.canvas.update()
                self.WIDGETS[i][1]['value'] = i
                self.WIDGETS[i][2] = {'anchor': tk.W}
        super(BaseVariableFrame, self).__init__(father)


class ChunksSet(BaseVariableFrame, BaseSetFrame):
    NAME = "Chunk"
    CODE = 'ch'
    WIDGETS = {'FM': (tk.Radiobutton, {'text': "Food Max"}, {}),
               'T': (tk.Radiobutton, {'text': "Temperature"}, {}),
               'F': (tk.Radiobutton, {'text': "Food"}, {}), }


class CreatureColorSet(BaseVariableFrame, BaseSetFrame):
    NAME = "Color"
    CODE = 'cc'
    WIDGETS = {'N': (tk.Radiobutton, {'text': "None"}, {}),
               'S': (tk.Radiobutton, {'text': "Sex"}, {}),
               'TR': (tk.Radiobutton, {'text': "Temp Resist"}, {}), }


class CreatureDimSet(BaseVariableFrame, BaseSetFrame):
    NAME = "Dimension"
    CODE = 'cd'
    WIDGETS = {'N': (tk.Radiobutton, {'text': "None"}, {}),
               'E': (tk.Radiobutton, {'text': "Energy"}, {}),
               'A': (tk.Radiobutton, {'text': "Agility"}, {}),
               'B': (tk.Radiobutton, {'text': "Bigness"}, {}),
               'EC': (tk.Radiobutton, {'text': "eat Coeff"}, {}),
               'S': (tk.Radiobutton, {'text': "Speed"}, {}),
               'NMG': (tk.Radiobutton, {'text': "Num Control Gene"}, {}), }


class CreatureSet(BaseSetFrame):
    NAME = "Creatures"
    WIDGETS = {'cl': (CreatureColorSet, {}, {'side': tk.LEFT, 'anchor': tk.NW, 'fill': tk.Y}),
               'dim': (CreatureDimSet, {}, {'side': tk.LEFT, 'anchor': tk.NW, 'fill': tk.Y}),
               }


class DiagramSet(tk.Frame):
    CHOICES = ['agility', 'bigness', 'eatCoeff', 'fertility', 'numControlGene', 'speed', 'population', 'foodmax', 'temperature_c', 'temperature_l', 'temperature_N']

    def __init__(self, father):
        super(DiagramSet, self).__init__(father)
        self.father = father
        self.WIDGETS = {'new': (tk.Button, {'text': "New Diagram", 'command': father.father.canvas.graphics_window_create}, {'anchor': tk.W})}
        self.diagram_chioce = tk.StringVar()
        self.diagram_chioce.set('agility')
        self._widgets_load()

    def _widgets_load(self):
        self.widgets = dict()
        self.widgets['menu'] = tk.OptionMenu(self, self.diagram_chioce, *self.CHOICES)
        self.widgets['menu'].pack(anchor=tk.W, fill=tk.X)
        for i in self.WIDGETS:
            new = self.WIDGETS[i][0](self, **self.WIDGETS[i][1])
            new.pack(**self.WIDGETS[i][2])
            self.widgets[i] = new


class SetSuperFrame(BaseFrame):
    WIDGETS = {'ch': (ChunksSet, {}, {'anchor': tk.W, 'fill': tk.X}),
               'cr': (CreatureSet, {}, {'anchor': tk.W, 'fill': tk.X}),
               'dgrm': (DiagramSet, {}, {'anchor': tk.W, 'fill': tk.X})
               }

    def __init__(self, father, kwargs):
        self.father = father
        super(SetSuperFrame, self).__init__(father, kwargs)
