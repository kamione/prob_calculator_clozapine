import tkinter
import customtkinter as ctk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pickle
import numpy as np
from pathlib import Path


class App(ttk.Window):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title(
            'Individualized Probability Calculator for Future Clozapine Use'
        )
        self.geometry('1000x600')
        self.resizable(False, False)

        # notebook with tabs
        self.notebook = ttk.Notebook(master=self, bootstyle='dark')
        self.notebook.grid(row=0, column=0, rowspan=7, sticky=NSEW)

        tab1 = ttk.Frame(self.notebook, width=400, height=400)
        tab1.pack(fill=Y, expand=Y)
        self.notebook.add(tab1, text='Baseline')
        self.build_tab1(tab1)

        tab2 = ttk.Frame(self.notebook)
        tab2.pack(fill=Y, expand=Y)
        self.notebook.add(tab2, text='12-month')
        self.build_tab2(tab2)

        tab3 = ttk.Frame(self.notebook)
        tab3.pack(fill=Y, expand=Y)
        self.notebook.add(tab3, text='24-month')
        self.build_tab3(tab3)

        tab4 = ttk.Frame(self.notebook)
        tab4.pack(fill=Y, expand=Y)
        self.notebook.add(tab4, text='36-month')
        self.build_tab4(tab4)

        # ====
        action_frame = ttk.Frame(self)
        action_frame.grid(row=7, column=0)

        press_label = ttk.Label(
            master=action_frame,
            text='Please press the buttom to calculate',
            font=('Helvetica bold', 16),
            width=35
        )
        press_label.grid(row=0, column=0, pady=(15, 0))
        press_label2 = ctk.CTkButton(
            master=action_frame,
            width=50,
            text='Calculate',
            command=self.calculate_prob
        )

        press_label2.grid(row=0, column=1, padx=(
            15, 15), pady=(15, 0), sticky='EW')

        self.meter = ttk.Meter(
            metersize=500,
            padding=5,
            amounttotal=60,
            amountused=0,
            stepsize=0.5,
            metertype='semi',
            subtext='Predicted Probability',
            textright='%',
            meterthickness=30,
            interactive=FALSE,
            textfont='-size 36',
            subtextfont='-size 18',
            bootstyle='danger'
        )
        self.meter.grid(row=0, column=1, rowspan=3,
                        sticky=NSEW, padx=(80, 0), pady=50)

    def build_tab1(self, tab):
        # define the input
        lb1 = ttk.Label(
            master=tab,
            text='1. Is schizophrenia diagnosis?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb1.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb1_options = ttk.StringVar(tab)
        self.lb1_options.set('Yes')  # default value
        lb1_om = ttk.OptionMenu(
            tab, self.lb1_options, self.lb1_options.get(), 'Yes', 'No')
        lb1_om.grid(row=0, column=1, padx=5, pady=5,
                    ipadx=5, ipady=5, sticky='EW')

        lb2 = ttk.Label(
            master=tab,
            text='2. Age at 1st presentation',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb2.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb2_input = ttk.Entry(tab, width=10)
        self.lb2_input.grid(row=1, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb3 = ttk.Label(
            master=tab,
            text='3. Number of days of untreated psychosis',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb3.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb3_input = ttk.Entry(tab, width=10)
        self.lb3_input.grid(row=2, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb4 = ttk.Label(
            master=tab,
            text='4. Number of hospitalized days during 1st episode',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb4.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb4_input = ttk.Entry(tab, width=10)
        self.lb4_input.grid(row=3, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb5 = ttk.Label(
            master=tab,
            text='5. Defined daily dose',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb5.grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb5_input = ttk.Entry(tab, width=10)
        self.lb5_input.grid(row=4, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb6 = ttk.Label(
            master=tab,
            text='6. Age of onset',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb6.grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb6_input = ttk.Entry(tab, width=10)
        self.lb6_input.grid(row=5, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb7 = ttk.Label(
            master=tab,
            text='7. Number of days of 1st episode',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb7.grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb7_input = ttk.Entry(tab, width=10)
        self.lb7_input.grid(row=6, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb8 = ttk.Label(
            master=tab,
            text='8. CGI depression score',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb8.grid(row=7, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb8_input = ttk.Entry(tab, width=10)
        self.lb8_input.grid(row=7, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb9 = ttk.Label(
            master=tab,
            text='9. Years of education',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb9.grid(row=8, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        self.lb9_input = ttk.Entry(tab, width=10)
        self.lb9_input.grid(row=8, column=1, padx=5, pady=5,
                            ipadx=5, ipady=5, sticky='EW')

        lb10 = ttk.Label(
            master=tab,
            text='10. SOFAS',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb10.grid(row=9, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb10_input = ttk.Entry(tab, width=10)
        self.lb10_input.grid(row=9, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

    def build_tab2(self, tab):
        # define the input
        lb11 = ttk.Label(
            master=tab,
            text='1. Is schizophrenia diagnosis?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb11.grid(row=0, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb11_options = ttk.StringVar(tab)
        self.lb11_options.set('Yes')  # default value
        lb11_om = ttk.OptionMenu(
            tab, self.lb11_options, self.lb11_options.get(), 'Yes', 'No')
        lb11_om.grid(row=0, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb12 = ttk.Label(
            master=tab,
            text='2. Age at 1st presentation',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb12.grid(row=1, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb12_input = ttk.Entry(tab, width=10)
        self.lb12_input.grid(row=1, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb13 = ttk.Label(
            master=tab,
            text='3. Number of months of relapses',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb13.grid(row=2, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb13_input = ttk.Entry(tab, width=10)
        self.lb13_input.grid(row=2, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb14 = ttk.Label(
            master=tab,
            text='4. Mean of SOFAS',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb14.grid(row=3, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb14_input = ttk.Entry(tab, width=10)
        self.lb14_input.grid(row=3, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb15 = ttk.Label(
            master=tab,
            text='5. Age of onset',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb15.grid(row=4, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb15_input = ttk.Entry(tab, width=10)
        self.lb15_input.grid(row=4, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb16 = ttk.Label(
            master=tab,
            text='6. Months of anticholinergic',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb16.grid(row=5, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb16_input = ttk.Entry(tab, width=10)
        self.lb16_input.grid(row=5, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb17 = ttk.Label(
            master=tab,
            text='7. Mean of CGI positive symptoms',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb17.grid(row=6, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb17_input = ttk.Entry(tab, width=10)
        self.lb17_input.grid(row=6, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb18 = ttk.Label(
            master=tab,
            text='8. Receiving early intervention service?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb18.grid(row=7, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb18_options = ttk.StringVar(tab)
        self.lb18_options.set('Yes')  # default value
        lb18_om = ttk.OptionMenu(
            tab, self.lb18_options, self.lb18_options.get(), 'Yes', 'No')
        lb18_om.grid(row=7, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb19 = ttk.Label(
            master=tab,
            text='9. Is affective type?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb19.grid(row=8, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb19_options = ttk.StringVar(tab)
        self.lb19_options.set('Yes')  # default value
        lb19_om = ttk.OptionMenu(
            tab, self.lb19_options, self.lb19_options.get(), 'Yes', 'No')
        lb19_om.grid(row=8, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb20 = ttk.Label(
            master=tab,
            text='10. Mean of defined daily dose',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb20.grid(row=9, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb20_input = ttk.Entry(tab, width=10)
        self.lb20_input.grid(row=9, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

    def build_tab3(self, tab):
        # define the input
        lb21 = ttk.Label(
            master=tab,
            text='1. Is schizophrenia diagnosis?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb21.grid(row=0, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb21_options = ttk.StringVar(tab)
        self.lb21_options.set('Yes')  # default value
        lb21_om = ttk.OptionMenu(
            tab, self.lb21_options, self.lb21_options.get(), 'Yes', 'No')
        lb21_om.grid(row=0, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb22 = ttk.Label(
            master=tab,
            text='2. Number of months of relapses',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb22.grid(row=1, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb22_input = ttk.Entry(tab, width=10)
        self.lb22_input.grid(row=1, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb23 = ttk.Label(
            master=tab,
            text='3. Number of months of anticholinergic',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb23.grid(row=2, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb23_input = ttk.Entry(tab, width=10)
        self.lb23_input.grid(row=2, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb24 = ttk.Label(
            master=tab,
            text='4. Age at 1st presentation',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb24.grid(row=3, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb24_input = ttk.Entry(tab, width=10)
        self.lb24_input.grid(row=3, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb25 = ttk.Label(
            master=tab,
            text='5. Mean of CGI positive symptom',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb25.grid(row=4, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb25_input = ttk.Entry(tab, width=10)
        self.lb25_input.grid(row=4, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb26 = ttk.Label(
            master=tab,
            text='6. Mean of defined daily dose',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb26.grid(row=5, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb26_input = ttk.Entry(tab, width=10)
        self.lb26_input.grid(row=5, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb27 = ttk.Label(
            master=tab,
            text='7. Number of months of poly drug uses',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb27.grid(row=6, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb27_input = ttk.Entry(tab, width=10)
        self.lb27_input.grid(row=6, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb28 = ttk.Label(
            master=tab,
            text='8. Is affective type?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb28.grid(row=7, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb28_options = ttk.StringVar(tab)
        self.lb28_options.set('Yes')  # default value
        lb28_om = ttk.OptionMenu(
            tab, self.lb28_options, self.lb28_options.get(), 'Yes', 'No')
        lb28_om.grid(row=7, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb29 = ttk.Label(
            master=tab,
            text='9. Mean of SOFAS',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb29.grid(row=8, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb29_input = ttk.Entry(tab, width=10)
        self.lb29_input.grid(row=8, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb30 = ttk.Label(
            master=tab,
            text='10. Age of onset',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb30.grid(row=9, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb30_input = ttk.Entry(tab, width=10)
        self.lb30_input.grid(row=9, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

    def build_tab4(self, tab):
        # define the input
        lb31 = ttk.Label(
            master=tab,
            text='1. Is schizophrenia diagnosis?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb31.grid(row=0, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb31_options = ttk.StringVar(tab)
        self.lb31_options.set('Yes')  # default value
        lb31_om = ttk.OptionMenu(
            tab, self.lb31_options, self.lb31_options.get(), 'Yes', 'No')
        lb31_om.grid(row=0, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb32 = ttk.Label(
            master=tab,
            text='2. Number of months of anticholinergic',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb32.grid(row=1, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb32_input = ttk.Entry(tab, width=10)
        self.lb32_input.grid(row=1, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb33 = ttk.Label(
            master=tab,
            text='3. Number of months of relapses',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb33.grid(row=2, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb33_input = ttk.Entry(tab, width=10)
        self.lb33_input.grid(row=2, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb34 = ttk.Label(
            master=tab,
            text='4. Mean of CGI postive symptoms',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb34.grid(row=3, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb34_input = ttk.Entry(tab, width=10)
        self.lb34_input.grid(row=3, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb35 = ttk.Label(
            master=tab,
            text='5. Mean of defined daily dose',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb35.grid(row=4, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb35_input = ttk.Entry(tab, width=10)
        self.lb35_input.grid(row=4, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb36 = ttk.Label(
            master=tab,
            text='6. MSSD of CGI positive symptom',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb36.grid(row=5, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb36_input = ttk.Entry(tab, width=10)
        self.lb36_input.grid(row=5, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb37 = ttk.Label(
            master=tab,
            text='7. Months of poly drug uses',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb37.grid(row=6, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb37_input = ttk.Entry(tab, width=10)
        self.lb37_input.grid(row=6, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb38 = ttk.Label(
            tab,
            text='8. Is affective type?',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb38.grid(row=7, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb38_options = ttk.StringVar(tab)
        self.lb38_options.set('Yes')  # default value
        lb38_om = ttk.OptionMenu(
            tab, self.lb38_options, self.lb38_options.get(), 'Yes', 'No')
        lb38_om.grid(row=7, column=1, padx=5, pady=5,
                     ipadx=5, ipady=5, sticky='EW')

        lb39 = ttk.Label(
            master=tab,
            text='9. Age at 1st presentation',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb39.grid(row=8, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb39_input = ttk.Entry(tab, width=10)
        self.lb39_input.grid(row=8, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

        lb40 = ttk.Label(
            master=tab,
            text='10. Mean of SOFAS',
            font=('Helvetica Neuw', 14),
            width=35
        )
        lb40.grid(row=9, column=0, padx=5, pady=5,
                  ipadx=5, ipady=5, sticky='W')
        self.lb40_input = ttk.Entry(tab, width=10)
        self.lb40_input.grid(row=9, column=1, padx=5, pady=5,
                             ipadx=5, ipady=5, sticky='EW')

    def calculate_prob(self):

        output = self.save_data()
        output_transformed = self.binary2dummy(output)
        output_digits = self.check_digits(output_transformed)

        if output_digits == FALSE:
            self.meter.configure(amountused=0)
            self.meter2.configure(amountused=0)
        else:
            prob = self.get_prob(output_digits)
            self.meter.configure(amountused=prob)

    def save_data(self):
        selected_page = self.notebook.index(self.notebook.select())
        nb1_output = [
            self.lb1_options.get(),
            self.lb2_input.get(),
            self.lb3_input.get(),
            self.lb4_input.get(),
            self.lb5_input.get(),
            self.lb6_input.get(),
            self.lb7_input.get(),
            self.lb8_input.get(),
            self.lb9_input.get(),
            self.lb10_input.get()
        ]
        nb2_output = [
            self.lb11_options.get(),
            self.lb12_input.get(),
            self.lb13_input.get(),
            self.lb14_input.get(),
            self.lb15_input.get(),
            self.lb16_input.get(),
            self.lb17_input.get(),
            self.lb18_options.get(),
            self.lb19_options.get(),
            self.lb20_input.get()
        ]
        nb3_output = [
            self.lb21_options.get(),
            self.lb22_input.get(),
            self.lb23_input.get(),
            self.lb24_input.get(),
            self.lb25_input.get(),
            self.lb26_input.get(),
            self.lb27_input.get(),
            self.lb28_options.get(),
            self.lb29_input.get(),
            self.lb30_input.get()
        ]
        nb4_output = [
            self.lb31_options.get(),
            self.lb32_input.get(),
            self.lb33_input.get(),
            self.lb34_input.get(),
            self.lb35_input.get(),
            self.lb36_input.get(),
            self.lb37_input.get(),
            self.lb38_options.get(),
            self.lb39_input.get(),
            self.lb40_input.get()
        ]
        if selected_page == 0:
            output = nb1_output
        elif selected_page == 1:
            output = nb2_output
        elif selected_page == 2:
            output = nb3_output
        elif selected_page == 3:
            output = nb4_output

        return output

    def binary2dummy(self, a_list):
        new_list = a_list
        for i in range(len(a_list)):
            # replace hardik with shardul
            if a_list[i] == 'Yes':
                new_list[i] = '1'
            if a_list[i] == 'No':
                new_list[i] = '0'
        return new_list

    def check_digits(self, a_list):
        new_list = list()

        for i in range(len(a_list)):
            if a_list[i] == '':
                self.warning_empty()
                new_list = FALSE
                break
            elif self.isfloat(a_list[i]):
                new_list.append(float(a_list[i]))
            else:
                self.warning_nonnumeric()
                new_list = FALSE
                break

        return new_list

    def warning_nonnumeric(self):
        top = tkinter.Toplevel(self)
        top.geometry('400x100')
        top.title('Warning')
        ttk.Label(
            master=top,
            text='Please make sure that all inputs are numeric!',
            font=('Helvetica bold', 16)
        ).place(relx=0.5, rely=0.5, anchor='center')

    def warning_empty(self):
        top = tkinter.Toplevel(self)
        top.geometry('400x100')
        top.title('Warning')
        ttk.Label(
            master=top,
            text='Please make sure that all inputs are filled!',
            font=('Helvetica bold', 16)
        ).place(relx=0.5, rely=0.5, anchor='center')

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def get_prob(self, te_x):
        selected_page = self.notebook.index(self.notebook.select())

        transformed_te_x = te_x

        if selected_page == 0:
            filename = Path(
                'models', 'baseline_allsubjs_top10_finalized_model.sav')
            # log transform DUP days
            if transformed_te_x[2] > 0:
                transformed_te_x[2] = np.log(transformed_te_x[2])
        elif selected_page == 1:
            filename = Path(
                'models', '12m_allsubjs_top10_finalized_model.sav')
        elif selected_page == 2:
            filename = Path(
                'models', '24m_allsubjs_top10_finalized_model.sav')
        elif selected_page == 3:
            filename = Path(
                'models', '36m_allsubjs_top10_finalized_model.sav')

        model = pickle.load(open(filename, 'rb'))

        prob = model.predict_proba(np.array([transformed_te_x]))[:, 1]
        print(transformed_te_x)
        print(prob)
        prob_percent = round(prob.item() * 100, 1)

        if prob_percent >= 60:
            prob_percent = 60

        return prob_percent


if __name__ == '__main__':
    app = App()
    app.mainloop()
