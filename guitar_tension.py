'''
@author: Jack Charles   https://jackcharlesconsulting.com/
'''

from dataclasses import dataclass, field
import itertools 
from nicegui import app, ui, binding
import plotly.graph_objects as go

ui.label.default_classes('text-xs').default_props('dense').default_style()
ui.input.default_classes('w-20 text-xs').default_props('dense').default_style()
ui.number.default_classes('w-20 text-xs').default_props('dense').default_style()
ui.button.default_classes('text-xs').default_props('rounded').default_style()
ui.select.default_classes('w-20 text-xs').default_props('dense').default_style()

@binding.bindable_dataclass
class GuitarString:
    gauge:str = 'PL009'
    tuning:str = 'E4'
    scale:float = 25.5
    tension:float = 0

    def tension_calc(self, conv_unit:float=0):
        self.tension = (string_mass_dictionary[self.gauge] * (2 * self.scale * notes_frequency_dictionary[self.tuning]) ** 2) / 386.4 * conv_unit

@binding.bindable_dataclass
class GuitarData:
    uid:int
    name:str  = ''
    strings:list = field(default_factory=lambda: [GuitarString() for _ in range(MAX_STRINGS)])
    total_tension:float = 0
    average_tension:float = 0
    label = None
    card = None

    def tension_summary(self, conv_unit:float=0):
        tension_list = []
        for i, string in enumerate(self.strings):
            string.tension_calc(conv_unit)
            if string.tension > 0: tension_list.append(string.tension)
        self.total_tension = sum(tension_list)
        self.average_tension = self.total_tension / len(tension_list)

tension_units = {'lbf': 1, 'kgf': 0.453592, 'N': 4.44822}

MAX_STRINGS = 9

scale_length_dictionary = {'Mustang 24"':24, 'LP 24.75"':24.75, 'PRS 25"':25, 'Strat 25.5"':25.5, 'Baritone 26.5"': 26.5, 'Baritone 27"': 27, 'Multi-Scale':0,
                           'Bass 36"':36, 'Bass 34"':34, 'Bass 32"':32, 'Bass 30"':30}

multiscale_scale_lengths = [25.5, 25.9, 26.3, 26.7, 27.1, 27.5, 27.8, 28.2, 28.6]          

notes_frequency_dictionary = {
    'C0': 16.35, 'C#0': 17.32, 'D0': 18.35, 'D#0': 19.45, 'E0': 20.60, 'F0': 21.83, 'F#0': 23.13, 'G0': 24.50, 'G#0': 25.96, 'A0': 27.50, 'A#0': 29.14, 'B0': 30.87, 
    'C1': 32.70, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.20, 'F1': 43.65, 'F#1': 46.25, 'G1': 49.00, 'G#1': 51.91, 'A1': 55.00, 'A#1': 58.27, 'B1': 61.74, 
    'C2': 65.41, 'C#2': 69.30, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2': 92.50, 'G2': 98.00, 'G#2': 103.83, 'A2': 110.00, 'A#2': 116.54, 'B2': 123.47, 
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'B3': 246.94, 
    'C4': 261.62, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.12, 'E4': 329.62, 'F4': 349.22, 'F#4': 370.00, 'G4': 392.00, 'G#4': 415.30, 'None':0
    }
  
tunings_dictionary = {
    'Standard': ['E4', 'B3', 'G3', 'D3', 'A2', 'E2', 'B1', 'F#1', 'C#1'],
    'Half Step': ['D#4', 'A#3', 'F#3', 'C#3', 'G#2', 'D#2', 'A#1', 'F1', 'C1'],
    'Whole Step': ['D4', 'A3', 'F3', 'C3', 'G2', 'D2', 'A1', 'E1', 'B0'],
    '1.5 Step': ['C#4', 'G#3', 'E3', 'B2', 'F#2', 'C#2', 'G#1', 'D#1', 'A#0'],
    '2 Step': ['C4', 'G3', 'D#3', 'A#2', 'F2', 'C2', 'G1', 'D1', 'A0'],
    '2.5 Step': ['B3', 'G3', 'D3', 'A2', 'E2', 'B1', 'F#1', 'C#1', 'G#0'],
    'Drop Standard': ['E4', 'B3', 'G3', 'D3', 'A2', 'D2', 'A1', 'E1', 'B0'],
    'Drop Half Step': ['D#4', 'A#3', 'F#3', 'C#3', 'G#2', 'C#2', 'G#1', 'D#1', 'A#0'],
    'Drop Whole Step': ['D4', 'A3', 'F3', 'C3', 'G2', 'C2', 'G1', 'D1', 'A0'],
    'Drop 1.5 Step': ['C#4', 'G#3', 'E3', 'B2', 'F#2', 'B1', 'F#1', 'C#1', 'G#0'],
    'Drop 2 Step': ['C4', 'G3', 'D#3', 'A#2', 'F2', 'A#1', 'F1', 'C1', 'G0'],
    'Drop 2.5 Step': ['B3', 'G3', 'D3', 'A2', 'E2', 'A1', 'E1', 'B0', 'F#0'],
    'Custom': ['E4', 'B3', 'G3', 'D3', 'A2', 'E2', 'B1', 'F#1', 'C#1']
    }

string_mass_dictionary = {
    'PL007': 0.00001085, 'PL008': 0.00001418, 'PL0085': 0.00001601, 'PL009': 0.00001794, 'PL0095': 0.00001999, 'PL010': 0.00002215, 'PL0105': 0.00002442, 'PL011': 0.00002680, 
    'PL0115': 0.00002930, 'PL012': 0.00003190, 'PL013': 0.00003744, 'PL0135': 0.00004037, 'PL014': 0.00004342, 'PL015': 0.00004984, 'PL016': 0.00005671, 'PL017': 0.00006402, 
    'PL018': 0.00007177, 'PL019': 0.00007997, 'PL020': 0.00008861, 'PL022': 0.00010722, 'PL024': 0.00012760, 'PL026': 0.00014975, 
    'NW017': 0.00005524, 'NW018': 0.00006215, 'NW019': 0.00006947, 'NW020': 0.00007495, 'NW021': 0.00008293, 'NW022': 0.00009184, 'NW024': 0.00010857, 'NW025': 0.00011818, 
    'NW026': 0.00012671, 'NW028': 0.00014666, 'NW030': 0.00017236, 'NW032': 0.00019347, 'NW034': 0.00021590, 'NW036': 0.00023964, 'NW037': 0.0002472697, 'NW038': 0.00026471, 
    'NW039': 0.00027932, 'NW040': 0.00028703, 'NW042': 0.00032279, 'NW044': 0.00035182, 'NW046': 0.00038216, 'NW048': 0.00041382, 'NW049': 0.00043014, 'NW050': 0.00042835, 
    'NW052': 0.00048109, 'NW054': 0.00053838, 'NW056': 0.00057598, 'NW059': 0.00064191, 'NW060': 0.00066542, 'NW062': 0.00070697, 'NW064': 0.00074984, 'NW066': 0.00079889, 
    'NW068': 0.00084614, 'NW070': 0.00089304, 'NW072': 0.00094124, 'NW074': 0.00098869, 'NW080': 0.00115011, 
    'XSG018': 0.00006588, 'XSG020': 0.00007919, 'XSG021': 0.00008774, 'XSG022': 0.00009731, 'XSG024': 0.00011501, 'XSG026': 0.00013419, 'XSG028': 0.00015493, 'XSG030': 0.00018203, 
    'XSG032': 0.00020398, 'XSG034': 0.00022729, 'XSG036': 0.00025198, 'XSG038': 0.00027804, 'XSG040': 0.00031044, 'XSG042': 0.00033924, 'XSG046': 0.00040096, 'XSG048': 0.00043387, 
    'XSG050': 0.00046816, 'XSG052': 0.00050382, 'XSG054': 0.00056388, 'XSG056': 0.00060297, 'XSG070': 0.00092592, 
    'CG020': 0.00007812, 'CG022': 0.00009784, 'CG024': 0.00011601, 'CG026': 0.00013574, 'CG028': 0.00014683, 'CG030': 0.00016958, 'CG032': 0.00019233, 'CG035': 0.00024197, 
    'CG038': 0.0002652, 'CG040': 0.00031676, 'CG042': 0.00034377, 'CG045': 0.00040393, 'CG048': 0.00043541, 'CG050': 0.00047042, 'CG052': 0.00049667, 'CG056': 0.00059075, 
    'CG065': 0.00089364, 'None':0
    }

string_database_daddario = {
    'NYXL 08-38': ['PL008', 'PL010', 'PL015', 'NW021', 'NW030', 'NW038', 'None', 'None', 'None'],
    'NYXL 09-40 Balanced': ['PL009', 'PL012', 'PL015', 'NW022', 'NW030', 'NW040', 'None', 'None', 'None'],
    'NYXL 09-42': ['PL009', 'PL011', 'PL016', 'NW024', 'NW032', 'NW042', 'None', 'None', 'None'],
    'NYXL 09-46': ['PL009', 'PL011', 'PL016', 'NW026', 'NW036', 'NW046', 'None', 'None', 'None'],
    'NYXL 9.5-44': ['PL0095', 'PL0115', 'PL016', 'NW024', 'NW034', 'NW044', 'None', 'None', 'None'],
    'NYXL 10-46': ['PL010', 'PL013', 'PL017', 'NW026', 'NW036', 'NW046', 'NW059', 'None', 'None'],
    'NYXL 10-46 Balanced': ['PL010', 'PL0135', 'PL017', 'NW025', 'NW034', 'NW046', 'None', 'None', 'None'],
    'NYXL 10-52': ['PL010', 'PL013', 'PL017', 'NW030', 'NW042', 'NW052', 'None', 'None', 'None'],
    'NYXL 11-49': ['PL011', 'PL014', 'PL018', 'NW028', 'NW038', 'NW049', 'NW064', 'None', 'None'],
    'NYXL 11-50 Balanced': ['PL011', 'PL015', 'PL019', 'NW028', 'NW037', 'NW050', 'None', 'None', 'None'],
    'NYXL 11-52': ['PL011', 'PL014', 'PL018', 'NW030', 'NW042', 'NW052', 'None', 'None', 'None'],
    'NYXL 11-56': ['PL011', 'PL014', 'PL019', 'NW032', 'NW044', 'NW056', 'None', 'None', 'None'],
    'NYXL 12-52': ['PL012', 'PL016', 'NW024', 'NW032', 'NW042', 'NW052', 'None', 'None', 'None'],
    'NYXL 12-54': ['PL012', 'PL016', 'PL020', 'NW032', 'NW042', 'NW054', 'None', 'None', 'None'],
    'NYXL 12-60': ['PL012', 'PL016', 'PL020', 'NW034', 'NW046', 'NW060', 'None', 'None', 'None'],
    'NYXL 13-56': ['PL013', 'PL017', 'NW026', 'NW036', 'NW046', 'NW056', 'None', 'None', 'None'],
    }

@ui.page('/')
def guitar_tension():

    tunings_selector = list(tunings_dictionary.keys())
    scale_length_selector = list(scale_length_dictionary.keys())
    string_database_selector = list(string_database_daddario.keys())
    notes_frequency_selector = list(notes_frequency_dictionary.keys())
    string_mass_selector = list(string_mass_dictionary.keys())
    tension_units_selector = list(tension_units.keys())

    guitars:dict[int, GuitarData] = {}
    uid_counter = itertools.count(1)

    def add_guitar():
        guitar = GuitarData(
            uid=next(uid_counter),
            strings=[GuitarString(gauge=string_database_daddario['NYXL 09-42'][_], tuning=tunings_dictionary['Standard'][_], scale=scale_length_dictionary['Strat 25.5"']) for _ in range(MAX_STRINGS)])
        guitars[guitar.uid] = guitar

        with data_container:
            with ui.card() as card:
                guitar.card = card
                with ui.row():
                #    #ui.input('Guitar Name').bind_value_to(guitar,'name')
                    ui.input(value=f'Guitar {len(guitars)}').bind_value_to(guitar,'name').classes(replace='w-40')
                    ui.button(text='Delete', on_click=lambda: del_guitar(guitar))

                with ui.row(align_items='center'):
                    tuning_selection = ui.select(options=tunings_selector, label='Tuning', value=tunings_selector[0], on_change=lambda x: change_tuning(guitar, x.value, tension_units_selection.value)).classes(replace='w-40')
                    scale_length_selection = ui.select(options=scale_length_selector, label='Scale', value=scale_length_selector[3], on_change=lambda x: change_scale(guitar, x.value, tension_units_selection.value)).classes(replace='w-32')
                    string_set_selection = ui.select(options=string_database_selector, label='String Sets', value=string_database_selector[0], on_change=lambda x: change_string_gauges(guitar, x.value, tension_units_selection.value)).classes(replace='w-32')
                    tuning_selection.name = tuning_selection.value
                    scale_length_selection.name =  scale_length_selection.value
                    string_set_selection.name = string_set_selection.value

                for i, string in enumerate(guitar.strings):
                    with ui.row(align_items='baseline'):
                        ui.label(f'String {i+1}')
                        ui.select(options=notes_frequency_selector, label='Note', value=tunings_dictionary['Standard'][i], on_change=lambda: update_all(guitars, tension_units_selection.value)).bind_value(string,'tuning')
                        ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary['Strat 25.5"'], on_change=lambda: update_all(guitars, tension_units_selection.value)).bind_value(string,'scale')
                        ui.select(options=string_mass_selector, label='Gauge', value=string_database_daddario['NYXL 09-42'][i], on_change=lambda: update_all(guitars, tension_units_selection.value)).bind_value(string,'gauge')
                        ui.input('Tension').bind_value_from(string,'tension', backward=lambda x: f'{x:.1f} {tension_units_selection.value}').classes('w-16')
                    
                with ui.row(align_items='baseline'):
                    ui.label().bind_text_from(guitar, 'total_tension', backward=lambda x: (f'Total Tension : {x:.1f} {tension_units_selection.value}'))
                    ui.label().bind_text_from(guitar, 'average_tension', backward=lambda x: f'Average Tension : {x:.1f} {tension_units_selection.value}')
        update_all(guitars, tension_units_selection.value)

    def del_guitar(guitar:GuitarData):
        guitars.pop(guitar.uid)
        guitar.card.delete()
        update_all(guitars, tension_units_selection.value)

    def change_tuning(guitar: GuitarData, tuning:str, unit:str):
        unit = tension_units_selection.value

        for string, note in zip(guitar.strings, tunings_dictionary[tuning]):
            string.tuning = note
            string.tension_calc(tension_units[unit])
        guitar.tension_summary(tension_units[unit])

    def change_scale(guitar: GuitarData, scale_length:str, unit:str):
        unit = tension_units_selection.value

        if scale_length != 'Multi-Scale':
            for string in guitar.strings:
                string.scale = scale_length_dictionary[scale_length]
                string.tension_calc(tension_units[unit])
        else:
            for string, scale in zip(guitar.strings, multiscale_scale_lengths):
                string.scale = scale
                string.tension_calc(tension_units[unit])
        guitar.tension_summary(tension_units[unit])

    def change_string_gauges(guitar: GuitarData, string_set_name:str, unit:str):
        for string, gauge in zip(guitar.strings, string_database_daddario[string_set_name]):
            string.gauge = gauge
            string.tension_calc(tension_units[unit])
        guitar.tension_summary(tension_units[unit])

    def update_all(guitars:dict[int, GuitarData], unit:str):
        fig.data = []
        for guitar in guitars.values():
            for string in guitar.strings:
                string.tension_calc(tension_units[unit])
            guitar.tension_summary(tension_units[unit])

            x_data = [f"String {s+1}" for s in range(MAX_STRINGS)]
            y_data = [strings.tension for strings in guitar.strings if strings.tension > 0]
            with plot_container:
                plot_container.set_visibility(True)
                #plot_container.clear()
                fig.add_trace(go.Scatter(x=x_data, y=y_data, name=guitar.name))
                fig.update_layout(legend=dict(orientation='h', xanchor='center', x=0.5, yanchor='bottom', y=-0.2), margin=dict(l=0, r=0, t=0, b=0))
                fig.update_yaxes(autorange="max", range=[0, None])
                plot.update()


#MAIN PROGRAM
    with ui.row():
        tension_units_selection = ui.select(options=tension_units_selector, label='Units', value=tension_units_selector[0], on_change=lambda: update_all(guitars, tension_units_selection.value))
        ui.button(text="Add guitar", on_click=add_guitar)
        ui.button(text="Print data", on_click=lambda: print(guitars))
        ui.button(text="Quit", on_click=app.shutdown)
    data_container = ui.row().classes('w-full')
    plot_container = ui.row().classes('w-full')
    with plot_container:
        fig = go.Figure()
        plot = ui.plotly(fig).classes('w-1/2 h-2/3')
    plot_container.set_visibility(False)

ui.run()