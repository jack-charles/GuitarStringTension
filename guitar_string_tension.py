"""
@author: Jack Charles   https://jackcharlesconsulting.com/
"""

import math
import numpy as np
import plotly.graph_objects as go
from nicegui import app, ui

class StringData():
    def __init__(self, tuning:str, scale:float, string:str, tension:float):
        self.tuning = tuning
        self.scale = scale
        self.string = string
        self.tension = tension

class GuitarData():
    def __init__(self, string:StringData, total_tension:float, average_tension:float):
        string = string
        self.total_tension = total_tension
        self.average_tension = average_tension

notes_frequency_dictionary = {
    'A0': 27.50, 'A#0': 29.14, 'B0': 30.87, 'C1': 32.70, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.20, 'F1': 43.65, 'F#1': 46.25, 'G1': 49.00, 'G#1': 51.91, 
    'A1': 55.00, 'A#1': 58.27, 'B1': 61.74, 'C2': 65.41, 'C#2': 69.30, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2': 92.50, 'G2': 98.00, 'G#2': 103.83, 
    'A2': 110.00, 'A#2': 116.54, 'B2': 123.47, 'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 
    'A3': 220.00, 'A#3': 233.08, 'B3': 246.94, 'C4': 261.62, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.12, 'E4': 329.62, 'F4': 349.22, 'F#4': 370.00, 'G4': 392.00, 'G#4': 415.30,
    'None':0
        }
scale_length_dictionary = {'Mustang':24, 'Les Paul':24.75, 'PRS':25, 'Strat':25.5, 'Baritone 26.5"': 26.5, 'Baritone 27"': 27, 'Multi-Scale':0}

tunings_dictionary = {
    'Standard': ['E4', 'B3', 'G3', 'D3', 'A2', 'E2', 'B1', 'F#1', 'C#1'],
    'Half Step': ['D#4', 'A#3', 'F#3', 'C#3', 'G#2', 'D#2', 'A#1', 'F1', 'C1'],
    'Whole Step': ['D4', 'A3', 'F3', 'C3', 'G2', 'D2', 'A1', 'E1', 'B0'],
    '1.5 Step': ['C#4', 'G#3', 'E3', 'B2', 'F#2', 'C#2', 'G#1', 'D#1', 'A#0'],
    '2 Step': ['C4', 'G3', 'D#3', 'A#2', 'F2', 'C2', 'G1', 'D1', 'A0'],
    '2.5 Step': ['B3', 'G3', 'D3', 'A2', 'E2', 'B1', 'F#1', 'C#1', 'None'],
    'Drop Standard': ['E4', 'B3', 'G3', 'D3', 'A2', 'D2', 'A1', 'E1', 'B0'],
    'Drop Half Step': ['D#4', 'A#3', 'F#3', 'C#3', 'G#2', 'C#2', 'G#1', 'D#1', 'A#0'],
    'Drop Whole Step': ['D4', 'A3', 'F3', 'C3', 'G2', 'C2', 'G1', 'D1', 'A0'],
    'Drop 1.5 Step': ['C#4', 'G#3', 'E3', 'B2', 'F#2', 'B1', 'F#1', 'C#1', 'None'],
    'Drop 2 Step': ['C4', 'G3', 'D#3', 'A#2', 'F2', 'A#1', 'F1', 'C1', 'None'],
    'Drop 2.5 Step': ['B3', 'G3', 'D3', 'A2', 'E2', 'A1', 'E1', 'B0', 'None'],
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
'NW068': 0.00084614, 'NW070': 0.00089304, 'NW072': 0.00094124, 'NW074': 0.00098869, 'NW080': 0.00115011, 'None':0
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

tension_units = {'lbf': 1, 'kgf': 0.453592, 'N': 4.44822}

@ui.page('/')
def main_page():
    
    tunings_selector = list(tunings_dictionary.keys())    
    scale_length_selector = list(scale_length_dictionary.keys())
    string_database_selector = list(string_database_daddario.keys())
    
    notes_frequency_selector = list(notes_frequency_dictionary.keys())
    string_gauge_selector = list(string_mass_dictionary.keys())
    tension_units_selector = list(tension_units.keys())
    
    single_data = {'Tuning': 'E4', 'Scale Length': 25.5, 'String Gauge': 'PL009', 'Tension': 0}
    string_data = {'String 1': {}, 'String 2': {}, 'String 3': {}, 'String 4': {}, 'String 5': {}, 'String 6': {}, 'String 7': {}, 'String 8': {}, 'String 9': {}, 'Total Tension':0, 'Average Tension':0, 'Guitar Name':''}
    guitar_data = {}
    guitars_list = []

    def add_guitar():
        tension_plot_container.set_visibility(True)  
        with data_container:
            with ui.card() as datacard:
                guitars_list.append(len(data_container.default_slot.children))
                with ui.row(align_items='center'):
                    gtr_lbl = ui.label(f'Guitar {len(data_container.default_slot.children)}').bind_text_to(guitar_data, f'Guitar {len(data_container.default_slot.children)}', forward=lambda x: {'String 1': {}, 'String 2': {}, 'String 3': {}, 'String 4': {}, 'String 5': {}, 'String 6': {}, 'String 7': {}, 'String 8': {}, 'String 9': {}, 'Total Tension':0, 'Average Tension':0, 'Guitar Name':''})
                    gtr_lbl.name = gtr_lbl.text
                    guitar_name = ui.input('Guitar Name').bind_value_to(guitar_data[gtr_lbl.name],'Guitar Name')
                    guitar_name.name = guitar_name.value               
                    ui.button('Delete', on_click=lambda: delete_guitar(datacard, gtr_lbl.name))
                with ui.row(align_items='center'):
                    tuning_lbl = ui.select(tunings_selector, label='Tuning', value=tunings_selector[0], on_change=lambda x: change_tuning(x.value, gtr_lbl.name)).classes('w-32')
                    scale_length_lbl = ui.select(scale_length_selector, label='Scale', value=scale_length_selector[3], on_change=lambda x: change_scale(x.value, gtr_lbl.name)).classes('w-24')
                    string_set_lbl = ui.select(string_database_selector, label='String Sets', value=string_database_selector[0], on_change=lambda x: change_string_gauges(x.value, gtr_lbl.name)).classes('w-36')
                    tuning_lbl.name = tuning_lbl.value
                    scale_length_lbl.name =  scale_length_lbl.value
                    string_set_lbl.name = string_set_lbl.value                
                with ui.row(align_items='baseline'):
                    _x = 0
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label=f'Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                    #ui.label('Tension lbf').bind_text_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: f'{x:.1f} {t_units.value}')
                    #ui.label('').bind_text_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: f'{t_units.value}')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    _x +=1
                    string_lbl = ui.label(f'String {_x+1}')
                    string_lbl.name = f'{string_lbl.text}'
                    ui.select(notes_frequency_selector, label='Note', value=tunings_dictionary[tuning_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Tuning')
                    ui.number(label='Scale Length', min=0, step=0.25, value=scale_length_dictionary[scale_length_lbl.name], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'Scale Length')
                    ui.select(string_gauge_selector, label='Gauge', value=string_database_daddario[string_set_lbl.name][_x], on_change=lambda: calculate_tension()).classes('w-20').bind_value(guitar_data[gtr_lbl.name][string_lbl.name],'String Gauge')
                    ui.number(label='Tension lbf', format='%.1f', suffix=t_units.value).bind_value_from(guitar_data[gtr_lbl.name][string_lbl.name],'Tension', backward=lambda x: x).classes('w-20')
                with ui.row(align_items='center'):
                    ui.label('Total Tension : lbf').bind_text_from(guitar_data[gtr_lbl.name], 'Total Tension',  backward=lambda x: f'Total Tension : {x:.1f} {t_units.value}')
                    ui.label('Average Tension : lbf').bind_text_from(guitar_data[gtr_lbl.name], 'Average Tension',  backward=lambda x: f'Average Tension : {x:.1f} {t_units.value}')  
            calculate_tension()

    def delete_guitar(datacard, guitar):
        del guitar_data[guitar]        
        datacard.delete()
        calculate_tension()

    with ui.row():
        t_units = ui.select(tension_units_selector, label='Units', value=tension_units_selector[0], on_change=lambda: calculate_tension()).classes('w-20')                      
        ui.button("Add guitar", on_click=add_guitar)
    data_container = ui.row()    
    
    tension_plot_container = ui.row().classes('w-full') 
    with tension_plot_container:
        tension_plot_container.set_visibility(False)
        fig = go.Figure()
        plot = ui.plotly(fig).classes('w-1/2 h-800')     

    
    
    
    def calculate_tension():
        fig.data = []
        guitars = list(guitar_data.keys())

        for guitar in guitars:
            gtr_data = guitar_data[guitar]
            strings = [f'String {x}' for x in range(1,10)]
            total_tension = 0
            strings_used = 0        #how many strings were actually calculated based on gauge availability

            for string in strings:
                str_data = guitar_data[guitar][string]
                string_mass_gradient = string_mass_dictionary[str_data['String Gauge']]
                tension = (string_mass_gradient * (2 * str_data['Scale Length'] * notes_frequency_dictionary[str_data['Tuning']]) ** 2) / 386.4 * tension_units[t_units.value]
                str_data.update({'Tuning': str_data['Tuning'], 'Scale Length': str_data['Scale Length'],'String Gauge': str_data['String Gauge'], 'Tension': tension})         
                total_tension = total_tension + str_data['Tension']
                if str_data['String Gauge'] == 'None':
                    str_data.update({'Tension': None}) 
                else:
                    strings_used += 1
                    pass

            guitar_data[guitar]['Total Tension'] = total_tension
            guitar_data[guitar]['Average Tension'] = total_tension / strings_used

            with tension_plot_container:
                x_data, y_data = [], []
                #x_data = [f'{string} - {gtr_data[string]['Tuning']}' for string in strings]
                x_data = [f'{string}' for string in strings]
                y_data = [gtr_data[string]['Tension'] for string in strings]
                #fig = go.Figure(go.Scatter(x = x_data, y = y_data, name=guitar))
                fig.add_trace(go.Scatter(x = x_data, y = y_data, name=gtr_data['Guitar Name']))
                fig.update_layout(legend=dict(orientation='h', xanchor='center', x=0.5, yanchor='bottom', y=-0.2), margin=dict(l=0, r=0, t=0, b=0))
                plot.update()

        guitars = list(guitar_data.keys())
        for gtr in guitars:
            strings = [f'String {x}' for x in range(1,2)]
            for string in strings:
                str_data = guitar_data[gtr][string]
    
    def change_tuning(tuning:str, guitar:str):
        if tuning != 'Custom':
            guitar_data[guitar]['String 1']['Tuning']  = tunings_dictionary[tuning][0]          
            guitar_data[guitar]['String 2']['Tuning']  = tunings_dictionary[tuning][1]
            guitar_data[guitar]['String 3']['Tuning']  = tunings_dictionary[tuning][2]
            guitar_data[guitar]['String 4']['Tuning']  = tunings_dictionary[tuning][3]
            guitar_data[guitar]['String 5']['Tuning']  = tunings_dictionary[tuning][4]
            guitar_data[guitar]['String 6']['Tuning']  = tunings_dictionary[tuning][5]
            guitar_data[guitar]['String 7']['Tuning']  = tunings_dictionary[tuning][6]
            guitar_data[guitar]['String 8']['Tuning']  = tunings_dictionary[tuning][7]
            guitar_data[guitar]['String 9']['Tuning']  = tunings_dictionary[tuning][8]
        else:
            guitar_data[guitar]['String 1']['Tuning']  = 'E4'
            guitar_data[guitar]['String 2']['Tuning']  = 'E4'
            guitar_data[guitar]['String 3']['Tuning']  = 'E4'
            guitar_data[guitar]['String 4']['Tuning']  = 'E4'
            guitar_data[guitar]['String 5']['Tuning']  = 'E4'
            guitar_data[guitar]['String 6']['Tuning']  = 'E4'
            guitar_data[guitar]['String 7']['Tuning']  = 'E4'
            guitar_data[guitar]['String 8']['Tuning']  = 'E4'
            guitar_data[guitar]['String 9']['Tuning']  = 'E4'

    def change_scale(scale_length:str, guitar):
        if scale_length != 'Multi-Scale':
            guitar_data[guitar]['String 1']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 2']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 3']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 4']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 5']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 6']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 7']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 8']['Scale Length'] = scale_length_dictionary[scale_length]
            guitar_data[guitar]['String 9']['Scale Length'] = scale_length_dictionary[scale_length]
        else:
            guitar_data[guitar]['String 1']['Scale Length'] = 25.5
            guitar_data[guitar]['String 2']['Scale Length'] = 25.9
            guitar_data[guitar]['String 3']['Scale Length'] = 26.3
            guitar_data[guitar]['String 4']['Scale Length'] = 26.7
            guitar_data[guitar]['String 5']['Scale Length'] = 27.1
            guitar_data[guitar]['String 6']['Scale Length'] = 27.5
            guitar_data[guitar]['String 7']['Scale Length'] = 27.8
            guitar_data[guitar]['String 8']['Scale Length'] = 28.2
            guitar_data[guitar]['String 9']['Scale Length'] = 28.6

    def change_string_gauges(string_set_name, guitar):
        guitar_data[guitar]['String 1']['String Gauge'] = string_database_daddario[string_set_name][0]
        guitar_data[guitar]['String 2']['String Gauge'] = string_database_daddario[string_set_name][1]
        guitar_data[guitar]['String 3']['String Gauge'] = string_database_daddario[string_set_name][2]
        guitar_data[guitar]['String 4']['String Gauge'] = string_database_daddario[string_set_name][3]
        guitar_data[guitar]['String 5']['String Gauge'] = string_database_daddario[string_set_name][4]
        guitar_data[guitar]['String 6']['String Gauge'] = string_database_daddario[string_set_name][5]
        guitar_data[guitar]['String 7']['String Gauge'] = string_database_daddario[string_set_name][6]
        guitar_data[guitar]['String 8']['String Gauge'] = string_database_daddario[string_set_name][7]
        guitar_data[guitar]['String 9']['String Gauge'] = string_database_daddario[string_set_name][8]

ui.run()
