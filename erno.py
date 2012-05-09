#!/usr/bin/env python
# -*- coding: utf-8

import nxt.locator
from nxt.motor import *

CALIBRATE_AFTER_FLIPPER_TURNDOWN = 10
CALIBRATE_AFTER_ELEVATOR_TURNDOWN = 270
FLIPPER_POWER = 10
FLIPPER_TURN = 80
ELEVATOR_POWER = 50
ELEVATOR_STEPS = [880, 220, 220, 250]
SPINNER_POWER = 100
SPINNER_STEP = 270

class Lego:
	@staticmethod
	def get_default():
		return Lego(nxt.locator.find_one_brick())
	def __init__(self, brick):
		self.brick = brick
		self.elevator = Motor(brick, PORT_A)
		self.elevator_state = 0
		self.spinner = Motor(brick, PORT_C)
		self.flipper = Motor(brick, PORT_B)
		self.flipper_state = 0
	def calibrate(self):
		self.elevator.idle()
		self.spinner.idle()
		self.flipper.idle()
		raw_input("Press ENTER when done")
		self.elevator.brake()
		self.spinner.brake()
		self.flipper.brake()
		self.elevator.turn(-ELEVATOR_POWER, CALIBRATE_AFTER_ELEVATOR_TURNDOWN)
		self.elevator.turn(FLIPPER_POWER, CALIBRATE_AFTER_FLIPPER_TURNDOWN)
		self.elevator_state = 0
		self.flipper_state = 0
	def grab(self, x):
		if x < 0 or x > 4:
			raise Exception()
		power = 50
		if x < self.elevator_state:
			power = -50
		self.elevator.turn(power, sum(ELEVATOR_STEPS[min(self.elevator_state, x) : max(self.elevator_state, x)]))
		self.elevator_state = x
	def flip(self, x):
		x = min(x, 1)
		if x != self.flipper_state:
			self.flipper.turn(FLIPPER_POWER*(x-self.flipper_state), FLIPPER_TURN)
			self.flipper_state = x
	def spin(self, x):
		power = x >= 0 and SPINNER_POWER or -SPINNER_POWER
		self.spinner.turn(power, SPINNER_STEP*abs(x))
		self.spinner.turn(power, 30)
		self.spinner.turn(-power, 30)
	def reload(self):
		return Lego(self.brick)
