# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 23:21:31 2014

@author: robert.w.smith08@gmail.com
"""

import bubbles

URL = "https://raw.github.com/Stiivi/cubes/master/examples/hello_world/data.csv"

bubbles.Pipeline()

p = bubbles.Pipeline()
p.source(bubbles.data_object("csv_source", URL, infer_fields=True))
p.aggregate("Category", "Amount (US$, Millions)")
p.pretty_print()

