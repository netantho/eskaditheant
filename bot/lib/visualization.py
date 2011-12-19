import sys
import os
sys.path.append(os.path.abspath('../'))

import variables
import logging

# https://github.com/j-h-a/aichallenge/blob/vis_overlay/VIS_OVERLAY.md

class Visualization():
	def __init__(self, ants):
		self.ants = ants
	
	def set_fill_color(self, r, g, b, a=1.0):
		sys.stdout.write('v setFillColor '+str(r)+' '+str(g)+' '+str(b)+' '+str(a)+'\n')
		sys.stdout.flush()
	
	def set_layer(self, layer):
		sys.stdout.write('v setLayer '+str(layer)+'\n')
		sys.stdout.flush()
	
	def set_line_color(self, r, g, b, a=1.0):
		sys.stdout.write('v setLineColor '+str(r)+' '+str(g)+' '+str(b)+' '+str(a)+'\n')
		sys.stdout.flush()
	
	def set_line_width(self, w):
		sys.stdout.write('v setLineWidth '+str(w)+'\n')
		sys.stdout.flush()
	
	def arrow(self, r1, c1, r2, c2):
		sys.stdout.write('v arrow '+str(r1)+' '+str(c1)+' '+str(r2)+' '+str(c2)+'\n')
		sys.stdout.flush()
	
	def circle(self, r, c, radius, fill='false'):
		sys.stdout.write('v circle '+str(r)+' '+str(c)+' '+str(radius)+' '+str(fill)+'\n')
		sys.stdout.flush()
		
	def line(self, r1, c1, r2, c2):
		sys.stdout.write('v line '+str(r1)+' '+str(c1)+' '+str(r2)+' '+str(c2)+'\n')
		sys.stdout.flush()
		
	def rect(self, r, c, width, height, fill='false'):
		sys.stdout.write('v rect '+str(r)+' '+str(c)+' '+str(width)+' '+str(height)+' '+str(fill)+'\n')
		sys.stdout.flush()
	
	def route_plan(r, c, plan_string):
		sys.stdout.write('v routePlan '+str(r)+' '+str(c)+' '+str(plan_string)+'\n')
		sys.stdout.flush()
	
	def star(r, c, inner_radius, outer_radius, points_number='4', fill='false'):
		sys.stdout.write('v star '+str(r)+' '+str(c)+' '+str(inner_radius)+' '+str(outer_radius)+' '+str(points_number)+' '+str(fill)+'\n')
		sys.stdout.flush()
	
	def tile(r, c):
		sys.stdout.write('v tile '+str(r)+' '+str(c)+'\n')
		sys.stdout.flush()
	
	def tile_border(r, c, subtile):
		sys.stdout.write('v tileBorder '+str(r)+' '+str(c)+' '+str(subtile)+'\n')
		sys.stdout.flush()
	
	def tile_subtile(r, c, subtile):
		sys.stdout.write('v tileSubtile '+str(r)+' '+str(c)+' '+str(subtile)+'\n')
		sys.stdout.flush()
	
	def information(r, c, text):
		sys.stdout.write('i '+str(r)+' '+str(c)+' '+str(text)+'\n')
		sys.stdout.flush()