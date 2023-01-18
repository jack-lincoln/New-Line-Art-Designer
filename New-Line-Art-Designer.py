#! python3
# New-Line-Art-Designer.py - New Line Art Designer is an interactive art design program.
# It allows for the user to view and modify various elements of a moving,
# linear art design in a GUI window that is launched when the program is run.

"""
This art invention allows for the user to adjust certain variables in the design.
When the program is launched, these controls are shown in the bottom left of the window.
CONTROLS:

    Shift               Adjusts the font size of the controls label
    ← / →               Play forwards or backwards (if already playing, this becomes pause)
    ↓ / ↑               - / + Speed
    SPACE               Pause
    BACKSPACE           Soft Reset (Resets starting point and speed)
    DELETE              Hard Reset (Resets all settings)
    1 / 2               - / + Rectangle size
    Q / W               - / + Rectangle count
    A / S               - / + Proximity to center
    Z / X               - / + Line thickness
    3 / 4 / 5 / 6       Cycles through arithmetic functions to be applied to the design equations
    7 / 8 / 9           Cycles through arithmetic functions to be applied to the design equations
    E / R / T / Y       Cycles through trigonometry functions to be applied to the design equations
    D / F / G / H       Cycles through trigonometry functions to be applied to the design equations
    C / V / B / N / M   Cycles through trigonometry functions to be applied to the design equations
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtWidgets
from math import *


class ArtInvention(QWidget):
    """Overall class to create the Invention."""

    # Determine the screen settings
    q_app = QtWidgets.QApplication(sys.argv)
    screen = q_app.primaryScreen()
    screen_size = screen.availableGeometry()

    def __init__(self, parent=None):
        """A method to control image settings, as well as run all class methods."""

        super(ArtInvention, self).__init__(parent)

        # Load gui blueprint
        uic.loadUi("New-Line-Art-Designer_Layout.ui", self)

        # General settings
        self.title = 'Art Invention 06'
        # self.image_width = 1915
        # self.window_height = 1001
        self.image_width = self.screen_size.width()
        self.window_height = self.screen_size.height()
        self.image_half = int(self.image_width / 2)
        self.set_children_focus_policy(Qt.NoFocus)
        self.starting_point = 1
        self.speed = 0.01
        self.design_colors = []

        # Window setup. Window may be set to custom size or opened fullscreen (the default view).
        self.setWindowTitle(self.title)
        # self.setGeometry(0, 0, self.image_width, int(self.window_height))
        self.showMaximized()

        # Create the graphics scene
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.graphicsView.setFrameShape(QFrame.NoFrame)

        # Booleans
        self.allow_image_movement = False
        self.forward_true = False
        self.backward_true = False
        self.last_direction_was_forward = True

        # Design variables adjusted by key presses:
        self.rect_width = 100
        self.rect_count = 13
        self.prox_to_center = 4
        self.line_thickness = 1
        self.bg_stripe_count = 4

        # Create a reset list to return design and speed properties to default settings
        self.reset_list = []
        self.reset_list.append(self.starting_point)
        self.reset_list.append(self.speed)
        self.reset_list.append(self.rect_width)
        self.reset_list.append(self.rect_count)
        self.reset_list.append(self.prox_to_center)
        self.reset_list.append(self.line_thickness)

        # Create a dictionary for the trigonometric functions applied to the design
        self.trig_list = [float, float, float, float,
                          float, float, float, float,
                          float, float, float, float, float]

        # Create a list of possible trigonometric functions to be used for the design equations
        self.trig_options = [float, sin, cos, tan]

        # Create a list of operators to use for the design equation
        self.op_list = ['/', '-', '/', '/', '-', '+', '+']

        # Create a list of possible arithmetic operators to be used for the design equations
        self.op_options = ['+', '-', '*', '/']

        # Create the text label
        self.label = self.findChild(QLabel, "text_label")

        # Create a dictionary to display stats for the label
        self.display_dict = {
            '00_direction': {
                'controls': '← / →',
                'name': 'Direction',
                'state': 'Press to begin!'
            },
            '01_speed': {
                'controls': '↓ / ↑',
                'name': 'Speed',
                'state': str(float("{:.1f}".format(self.speed * 100)))
            },
            '02_rect_width': {
                'controls': '1 / 2',
                'name': 'Rectangle width',
                'state': str("{:.2f}".format(self.rect_width))
            },
            '03_rect_count': {
                'controls': 'Q / W',
                'name': 'Rectangle count',
                'state': str(self.rect_count)
            },
            '04_prox_to_center': {
                'controls': 'A / S',
                'name': 'Proximity to center',
                'state': str(self.prox_to_center)
            },
            '05_line_thickness': {
                'controls': 'Z / X',
                'name': 'Line thickness',
                'state': str(self.line_thickness)
            },
            '06_op_list_00': {
                'controls': '3/4/5/6',
                'name': 'Operators 1-4',
                'state_00': '/',
                'state_01': '-',
                'state_02': '/',
                'state_03': '/'
            },
            '07_op_list_01': {
                'controls': '7/8/9',
                'name': 'Operators 5-7',
                'state_00': '-',
                'state_01': '+',
                'state_02': '+'
            },
            '08_trig_00': {
                'controls': 'E/R/T/Y',
                'name': 'Trig. functions 1-4',
                'state_00': 'None',
                'state_01': 'None',
                'state_02': 'None',
                'state_03': 'None'
            },
            '09_trig_01': {
                'controls': 'D/F/G/H',
                'name': 'Trig. functions 5-8',
                'state_00': 'None',
                'state_01': 'None',
                'state_02': 'None',
                'state_03': 'None'
            },
            '10_trig_02': {
                'controls': 'C/V/B/N/M',
                'name': 'Trig. functions 9-13',
                'state_00': 'None',
                'state_01': 'None',
                'state_02': 'None',
                'state_03': 'None',
                'state_04': 'None'
            }
        }

        self.label_font_size = [[6.5, 200, 150],
                                [9, 250, 200],
                                [12, 350, 325]],

        self.label_font_size_index = 0

        self.display_stats()

        # Create a counter for counting "frames" of the design
        self.count = 0

    def set_children_focus_policy(self, policy):
        """A method to overide default properties of key presses."""

        def recursive_set_child_focus_policy(parent_QWidget):
            for childQWidget in parent_QWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursive_set_child_focus_policy(childQWidget)
        recursive_set_child_focus_policy(self)

    def next_val(self, list, value):
        """A method to select the next value in a list."""
        idx = list.index(value) + 1
        if idx > len(list) - 1:
            idx = 0
        return list[idx]

    def get_op(self, operator, a, b):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b

    def paintEvent(self, event):
        """A method to setup the paint event."""

        self.draw_background()
        self.get_design_colors()
        self.display_stats()

        if self.allow_image_movement:
            canvas_painter = QPainter()
            canvas_painter.begin(self)
            canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

            self.draw_design()

            self.count += 1

            self.scene.update()

            if self.count % 2 == 0:
                self.scene.clear()
                self.draw_design()

            self.scene.setSceneRect(0, 0, self.image_width, self.image_width)

            canvas_painter.end()

    def display_stats(self):
        """A method to display info in the GUI."""

        label_00 = self.display_dict['00_direction']['controls'] + "   - " + \
                   self.display_dict['00_direction']['name'] + ": " + \
                   self.display_dict['00_direction']['state'] + " "

                   # str(float("{:.0f}".format(self.starting_point)))

        label_01 = self.display_dict['01_speed']['controls'] + "     -  " + \
                   self.display_dict['01_speed']['name'] + ": " + \
                   self.display_dict['01_speed']['state']

        label_02 = self.display_dict['02_rect_width']['controls'] + "     -  " + \
                   self.display_dict['02_rect_width']['name'] + ": " + \
                   self.display_dict['02_rect_width']['state']

        label_03 = self.display_dict['03_rect_count']['controls'] + "   -  " + \
                   self.display_dict['03_rect_count']['name'] + ": " + \
                   self.display_dict['03_rect_count']['state']

        label_04 = self.display_dict['04_prox_to_center']['controls'] + "    -  " + \
                   self.display_dict['04_prox_to_center']['name'] + ": " + \
                   self.display_dict['04_prox_to_center']['state']

        label_05 = self.display_dict['05_line_thickness']['controls'] + "    -  " + \
                   self.display_dict['05_line_thickness']['name'] + ": " + \
                   self.display_dict['05_line_thickness']['state']

        label_06 = self.display_dict['06_op_list_00']['controls'] + "  -  " + \
                   self.display_dict['06_op_list_00']['name'] + ":  " + \
                   self.display_dict['06_op_list_00']['state_00'] + ",  " + \
                   self.display_dict['06_op_list_00']['state_01'] + ",  " + \
                   self.display_dict['06_op_list_00']['state_02'] + ",  " + \
                   self.display_dict['06_op_list_00']['state_03']

        label_07 = self.display_dict['07_op_list_01']['controls'] + "     -  " + \
                   self.display_dict['07_op_list_01']['name'] + ":  " + \
                   self.display_dict['07_op_list_01']['state_00'] + ",  " + \
                   self.display_dict['07_op_list_01']['state_01'] + ",  " + \
                   self.display_dict['07_op_list_01']['state_02']

        label_08 = self.display_dict['08_trig_00']['controls'] + "   -   " + \
                   self.display_dict['08_trig_00']['name'] + ":  " + \
                   self.display_dict['08_trig_00']['state_00'] + ", " + \
                   self.display_dict['08_trig_00']['state_01'] + ", " + \
                   self.display_dict['08_trig_00']['state_02'] + ", " + \
                   self.display_dict['08_trig_00']['state_03']

        label_09 = self.display_dict['09_trig_01']['controls'] + "   -   " + \
                   self.display_dict['09_trig_01']['name'] + ":  " + \
                   self.display_dict['09_trig_01']['state_00'] + ", " + \
                   self.display_dict['09_trig_01']['state_01'] + ", " + \
                   self.display_dict['09_trig_01']['state_02'] + ", " + \
                   self.display_dict['09_trig_01']['state_03']

        label_10 = self.display_dict['10_trig_02']['controls'] + " - " + \
                   self.display_dict['10_trig_02']['name'] + ": " + \
                   self.display_dict['10_trig_02']['state_00'] + ", " + \
                   self.display_dict['10_trig_02']['state_01'] + ", " + \
                   self.display_dict['10_trig_02']['state_02'] + ", " + \
                   self.display_dict['10_trig_02']['state_03'] + ", " + \
                   self.display_dict['10_trig_02']['state_04']

        self.label.setText(label_00 + "\n" +
                           label_01 + "\n" +
                           label_02 + "\n" +
                           label_03 + "\n" +
                           label_04 + "\n" +
                           label_05 + "\n" +
                           label_06 + "\n" +
                           label_07 + "\n" +
                           label_08 + "\n" +
                           label_09 + "\n" +
                           label_10)

        self.label.setStyleSheet(f"font: {self.label_font_size[0][self.label_font_size_index][0]}pt MS Shell Dlg 2;"
                                 "background-color: rgba(255, 255, 255, 0);"
                                 "color: rgb(189, 189, 189);")

        self.label.setGeometry(10, self.window_height - self.label_font_size[0][self.label_font_size_index][1],
                               750, self.label_font_size[0][self.label_font_size_index][2])

    def keyPressEvent(self, QKeyEvent):
        """A method to assign functions to key presses."""

        # Assigns the keys to move the design forward or backward
        if QKeyEvent.key() == Qt.Key_Right:
            self.forward()
        elif QKeyEvent.key() == Qt.Key_Left:
            self.backward()

        # Assigns the key to pause the design movement
        elif QKeyEvent.key() == Qt.Key_Space:
            if self.allow_image_movement:
                self.pause_movement()
            elif self.last_direction_was_forward:
                self.forward()
            elif not self.last_direction_was_forward:
                self.backward()

        # Assigns the keys to adjust speed
        elif QKeyEvent.key() == Qt.Key_Down:
            self.speed_down()
        elif QKeyEvent.key() == Qt.Key_Up:
            self.speed_up()

        # Assigns the keys to adjust rectangle width
        elif QKeyEvent.key() == Qt.Key_1:
            self.rect_width_down()
        elif QKeyEvent.key() == Qt.Key_2:
            self.rect_width_up()

        # Assigns the keys to adjust rectangle count
        elif QKeyEvent.key() == Qt.Key_Q:
            self.rect_count_decrease()
        elif QKeyEvent.key() == Qt.Key_W:
            self.rect_count_increase()

        # Assigns the keys to adjust prox_to_center
        elif QKeyEvent.key() == Qt.Key_A:
            self.prox_to_center_decrease()
        elif QKeyEvent.key() == Qt.Key_S:
            self.prox_to_center_increase()

        # Assigns the keys to adjust line thickness
        elif QKeyEvent.key() == Qt.Key_Z:
            self.line_thickness_decrease()
        elif QKeyEvent.key() == Qt.Key_X:
            self.line_thickness_increase()

        # Assigns the key to adjust the label font size
        elif QKeyEvent.key() == Qt.Key_Shift:
            self.label_font_size_adjust()

        # Assigns the keys to adjust trigonometric functions
        elif QKeyEvent.key() == Qt.Key_E:
            self.trig_list[0] = self.next_val(self.trig_options, self.trig_list[0])
            self.display_dict['08_trig_00']['state_00'] = self.trig_update(self.trig_list[0])
        elif QKeyEvent.key() == Qt.Key_R:
            self.trig_list[1] = self.next_val(self.trig_options, self.trig_list[1])
            self.display_dict['08_trig_00']['state_01'] = self.trig_update(self.trig_list[1])
        elif QKeyEvent.key() == Qt.Key_T:
            self.trig_list[2] = self.next_val(self.trig_options, self.trig_list[2])
            self.display_dict['08_trig_00']['state_02'] = self.trig_update(self.trig_list[2])
        elif QKeyEvent.key() == Qt.Key_Y:
            self.trig_list[3] = self.next_val(self.trig_options, self.trig_list[3])
            self.display_dict['08_trig_00']['state_03'] = self.trig_update(self.trig_list[3])
        elif QKeyEvent.key() == Qt.Key_D:
            self.trig_list[4] = self.next_val(self.trig_options, self.trig_list[4])
            self.display_dict['09_trig_01']['state_00'] = self.trig_update(self.trig_list[4])
        elif QKeyEvent.key() == Qt.Key_F:
            self.trig_list[5] = self.next_val(self.trig_options, self.trig_list[5])
            self.display_dict['09_trig_01']['state_01'] = self.trig_update(self.trig_list[5])
        elif QKeyEvent.key() == Qt.Key_G:
            self.trig_list[6] = self.next_val(self.trig_options, self.trig_list[6])
            self.display_dict['09_trig_01']['state_02'] = self.trig_update(self.trig_list[6])
        elif QKeyEvent.key() == Qt.Key_H:
            self.trig_list[7] = self.next_val(self.trig_options, self.trig_list[7])
            self.display_dict['09_trig_01']['state_03'] = self.trig_update(self.trig_list[7])
        elif QKeyEvent.key() == Qt.Key_C:
            self.trig_list[8] = self.next_val(self.trig_options, self.trig_list[8])
            self.display_dict['10_trig_02']['state_00'] = self.trig_update(self.trig_list[8])
        elif QKeyEvent.key() == Qt.Key_V:
            self.trig_list[9] = self.next_val(self.trig_options, self.trig_list[9])
            self.display_dict['10_trig_02']['state_01'] = self.trig_update(self.trig_list[9])
        elif QKeyEvent.key() == Qt.Key_B:
            self.trig_list[10] = self.next_val(self.trig_options, self.trig_list[10])
            self.display_dict['10_trig_02']['state_02'] = self.trig_update(self.trig_list[10])
        elif QKeyEvent.key() == Qt.Key_N:
            self.trig_list[11] = self.next_val(self.trig_options, self.trig_list[11])
            self.display_dict['10_trig_02']['state_03'] = self.trig_update(self.trig_list[11])
        elif QKeyEvent.key() == Qt.Key_M:
            self.trig_list[12] = self.next_val(self.trig_options, self.trig_list[12])
            self.display_dict['10_trig_02']['state_04'] = self.trig_update(self.trig_list[12])

        # Assign the keys to adjust operators for the design equations
        elif QKeyEvent.key() == Qt.Key_3:
            self.op_list[0] = self.next_val(self.op_options, self.op_list[0])
            self.display_dict['06_op_list_00']['state_00'] = self.operator_update(self.op_list[0])
        elif QKeyEvent.key() == Qt.Key_4:
            self.op_list[1] = self.next_val(self.op_options, self.op_list[1])
            self.display_dict['06_op_list_00']['state_01'] = self.operator_update(self.op_list[1])
        elif QKeyEvent.key() == Qt.Key_5:
            self.op_list[2] = self.next_val(self.op_options, self.op_list[2])
            self.display_dict['06_op_list_00']['state_02'] = self.operator_update(self.op_list[2])
        elif QKeyEvent.key() == Qt.Key_6:
            self.op_list[3] = self.next_val(self.op_options, self.op_list[3])
            self.display_dict['06_op_list_00']['state_03'] = self.operator_update(self.op_list[3])
        elif QKeyEvent.key() == Qt.Key_7:
            self.op_list[4] = self.next_val(self.op_options, self.op_list[4])
            self.display_dict['07_op_list_01']['state_00'] = self.operator_update(self.op_list[4])
        elif QKeyEvent.key() == Qt.Key_8:
            self.op_list[5] = self.next_val(self.op_options, self.op_list[5])
            self.display_dict['07_op_list_01']['state_01'] = self.operator_update(self.op_list[5])
        elif QKeyEvent.key() == Qt.Key_9:
            self.op_list[6] = self.next_val(self.op_options, self.op_list[6])
            self.display_dict['07_op_list_01']['state_02'] = self.operator_update(self.op_list[6])

        # Assigns the key to soft reset the design
        elif QKeyEvent.key() == Qt.Key_Backspace:
            self.soft_reset()

        # Assigns the key to hard reset the design
        elif QKeyEvent.key() == Qt.Key_Delete:
            self.hard_reset()

    def forward(self):
        """A method to have the image move forward."""
        if not self.forward_true:
            self.backward_true = False
            self.allow_image_movement = True
            self.forward_true = True
            self.last_direction_was_forward = True
            self.display_dict['00_direction']['state'] = 'Forward'
        else:
            self.pause_movement()

    def backward(self):
        """A method to have the image move backward."""
        if not self.backward_true:
            self.forward_true = False
            self.allow_image_movement = True
            self.backward_true = True
            self.last_direction_was_forward = False
            self.display_dict['00_direction']['state'] = 'Backward'
        else:
            self.pause_movement()

    def pause_movement(self):
        """A method to pause movement, then resume movement when pressed again in the most recent direction."""
        if self.allow_image_movement:
            self.allow_image_movement = False
            self.starting_point += 0
            self.forward_true = False
            self.backward_true = False
            self.display_dict['00_direction']['state'] = 'Paused'
        else:
            if self.last_direction_was_forward:
                self.forward_true = True
                self.backward_true = False
                self.allow_image_movement = True
                self.forward()
            elif not self.last_direction_was_forward:
                self.backward_true = True
                self.forward_true = False
                self.allow_image_movement = True
                self.backward()

    def speed_up(self):
        """A method to increase the speed."""
        if self.speed > 100:
            pass
        else:
            self.speed *= 1.5
            if self.speed > 0.001:
                self.display_dict['01_speed']['state'] = str(float("{:.1f}".format(self.speed * 100)))
            else:
                self.display_dict['01_speed']['state'] = str(float("{:.3f}".format(self.speed * 100)))

    def speed_down(self):
        """A method to decrease the speed."""
        if self.speed < 0.00001:
            pass
        else:
            self.speed /= 1.5
            if self.speed > 0.001:
                self.display_dict['01_speed']['state'] = str(float("{:.1f}".format(self.speed * 100)))
            else:
                self.display_dict['01_speed']['state'] = str(float("{:.3f}".format(self.speed * 100)))

    def rect_width_up(self):
        """A method to increase the size of the rectangle width."""
        if self.rect_width > 10000:
            pass
        else:
            self.rect_width *= 1.25
            self.display_dict['02_rect_width']['state'] = str("{:.1f}".format(float(self.rect_width)))    # Original code

    def rect_width_down(self):
        """A method to decrease the size of the rectangle."""
        if self.rect_width < 2:
            pass
        elif self.rect_width >= 2:
            self.rect_width /= 1.25
            self.display_dict['02_rect_width']['state'] = str("{:.1f}".format(float(self.rect_width)))

    def rect_count_increase(self):
        """A method to increase the rectangle count."""
        self.rect_count += 1
        self.display_dict['03_rect_count']['state'] = str(self.rect_count)

    def rect_count_decrease(self):
        """A method to increase the rectangle count."""
        if self.rect_count == 1:
            pass
        elif self.rect_count > 1:
            self.rect_count -= 1
            self.display_dict['03_rect_count']['state'] = str(self.rect_count)

    def prox_to_center_increase(self):
        """A method to increase the proximity of the design to the center of the image."""
        self.prox_to_center += 1
        self.display_dict['04_prox_to_center']['state'] = str(self.prox_to_center)

    def prox_to_center_decrease(self):
        """A method to increase the proximity of the design to the center of the image."""
        if self.prox_to_center == 1:
            pass
        elif self.prox_to_center > 1:
            self.prox_to_center -= 1
            self.display_dict['04_prox_to_center']['state'] = str(self.prox_to_center)

    def line_thickness_increase(self):
        """A method to increase the line thickness."""
        self.line_thickness += 1
        self.display_dict['05_line_thickness']['state'] = str(self.line_thickness)

    def line_thickness_decrease(self):
        """A method to decrease the line thickness."""
        if self.line_thickness == 1:
            pass
        elif self.line_thickness > 1:
            self.line_thickness -= 1
            self.display_dict['05_line_thickness']['state'] = str(self.line_thickness)

    def label_font_size_adjust(self):
        """A method to adjust the label font size."""
        if self.label_font_size_index == 2:
            self.label_font_size_index = 0
        else:
            self.label_font_size_index += 1

    def trig_update(self, trig_list_item):
        """A method to update the trigonometric functions in the display."""
        if trig_list_item == float:
            return 'None'
        elif trig_list_item == sin:
            return 'Sine'
        elif trig_list_item == cos:
            return 'Cosine'
        elif trig_list_item == tan:
            return 'Tangent'

    def operator_update(self, op_list_item):
        """A method to update the operators in the display."""
        if op_list_item == '+':
            return '+'
        elif op_list_item == '-':
            return '-'
        elif op_list_item == '*':
            return '*'
        elif op_list_item == '/':
            return '/'

    def soft_reset(self):
        """A method to reset the starting point and speed."""

        # Reset movements
        self.allow_image_movement = False
        self.backward_true = False
        self.forward_true = False

        self.starting_point = self.reset_list[0]
        self.speed = self.reset_list[1]

    def hard_reset(self):
        """A method to hard reset all variables variables."""

        # Clear scene
        self.scene.clear()

        # Reset movements
        self.allow_image_movement = False
        self.backward_true = False
        self.forward_true = False

        # Reset key press variables
        self.starting_point = self.reset_list[0]
        self.speed = self.reset_list[1]
        self.rect_width = self.reset_list[2]
        self.rect_count = self.reset_list[3]
        self.prox_to_center = self.reset_list[4]
        self.line_thickness = self.reset_list[5]

        self.trig_list = [float, float, float, float,
                          float, float, float, float,
                          float, float, float, float, float]

        self.op_list = ['/', '-', '/', '/', '-', '+', '+']

        # Reset display stats
        self.display_dict['00_direction']['state'] = 'Press → to begin!'
        self.display_dict['01_speed']['state'] = str(float("{:.1f}".format(self.speed * 100)))
        self.display_dict['02_rect_width']['state'] = str("{:.2f}".format(self.rect_width))
        self.display_dict['03_rect_count']['state'] = str(self.rect_count)
        self.display_dict['04_prox_to_center']['state'] = str(self.prox_to_center)
        self.display_dict['05_line_thickness']['state'] = str(self.line_thickness)

        # Reset operator display stats
        self.display_dict['06_op_list_00']['state_00'] = '/'
        self.display_dict['06_op_list_00']['state_01'] = '-'
        self.display_dict['06_op_list_00']['state_02'] = '/'
        self.display_dict['06_op_list_00']['state_03'] = '/'
        self.display_dict['07_op_list_01']['state_00'] = '-'
        self.display_dict['07_op_list_01']['state_01'] = '+'
        self.display_dict['07_op_list_01']['state_02'] = '+'

        # Reset trigonometric function display stats
        self.display_dict['08_trig_00']['state_00'] = 'None'
        self.display_dict['08_trig_00']['state_01'] = 'None'
        self.display_dict['08_trig_00']['state_02'] = 'None'
        self.display_dict['08_trig_00']['state_03'] = 'None'
        self.display_dict['09_trig_01']['state_00'] = 'None'
        self.display_dict['09_trig_01']['state_01'] = 'None'
        self.display_dict['09_trig_01']['state_02'] = 'None'
        self.display_dict['09_trig_01']['state_03'] = 'None'
        self.display_dict['10_trig_02']['state_00'] = 'None'
        self.display_dict['10_trig_02']['state_01'] = 'None'
        self.display_dict['10_trig_02']['state_02'] = 'None'
        self.display_dict['10_trig_02']['state_03'] = 'None'
        self.display_dict['10_trig_02']['state_04'] = 'None'

    def draw_background(self):
        """A method to draw the background."""

        pen = QPen(QColor(0, 0, 0), 1, )

        grad = QLinearGradient(QPoint(self.image_width, 0), QPoint(self.image_width, self.image_width))

        bg_start_colors = [30, 5, 5]
        bg_end_colors = [15, 5, 35]

        gradient_position = 0
        grad_pos_inc = 1.0 / self.bg_stripe_count
        for i in range(self.bg_stripe_count + 1):
            grad.setColorAt(gradient_position if gradient_position <= 1 else 1,
                            QColor(bg_start_colors[0], bg_start_colors[1], bg_start_colors[2]))
            gradient_position += grad_pos_inc / 2
            grad.setColorAt(gradient_position if gradient_position <= 1 else 1,
                            QColor(bg_end_colors[0], bg_end_colors[1], bg_end_colors[2]))
            gradient_position += grad_pos_inc / 2

        r = QRectF(QPointF(0, 0), QSizeF(self.image_width, self.image_width))
        self.scene.setBackgroundBrush(grad)
        self.scene.addRect(r, pen)

    def get_design_colors(self):
        """A method to declare the starting and ending colors, then create a list of colors."""

        design_start_colors = [140, 255, 140]
        design_end_colors = [5, 55, 140]

        self.design_colors.append((design_start_colors[0], design_start_colors[1], design_start_colors[2]))

        red_increment = (design_end_colors[0] - design_start_colors[0]) / self.rect_count
        green_increment = (design_end_colors[1] - design_start_colors[1]) / self.rect_count
        blue_increment = (design_end_colors[2] - design_start_colors[2]) / self.rect_count

        for i in range(self.rect_count):
            design_start_colors[0] += red_increment
            design_start_colors[1] += green_increment
            design_start_colors[2] += blue_increment
            self.design_colors.append(
                (int(design_start_colors[0]), int(design_start_colors[1]), int(design_start_colors[2])))

    def draw_design(self):
        """A method to draw a second design."""

        for i in range(1, self.rect_count):
            for j in range(i, self.image_width, int(self.image_width / self.rect_count)):
                pen = QPen(QColor(self.design_colors[i][0], self.design_colors[i][1], self.design_colors[i][2]),
                           self.line_thickness, Qt.SolidLine)

                design = self.scene.addRect(
                    # The starting x-value of the first rectangle
                    self.get_op(self.op_list[1],
                                self.trig_list[0](self.trig_list[1](
                    self.get_op(self.op_list[0],
                                self.image_half,
                                self.trig_list[2](self.prox_to_center)))),
                    self.get_op(self.op_list[2],
                                self.trig_list[3](self.starting_point),
                                self.trig_list[4](i))),

                    # The starting y-value of the first rectangle
                    self.get_op(self.op_list[4],
                                self.trig_list[5](
                    self.get_op(self.op_list[3],
                                self.trig_list[6](self.image_half),
                                self.trig_list[7](self.prox_to_center))),
                                self.trig_list[8](self.starting_point)),

                    # The x length of of the first rectangle
                    self.get_op(self.op_list[5],
                                self.trig_list[9](self.rect_width),
                                self.trig_list[10](self.starting_point)),

                    # The y length of of the first rectangle
                    self.get_op(self.op_list[6],
                                self.trig_list[11](self.rect_width),
                                self.trig_list[12](self.starting_point)),
                    pen)

                """
                Original, non-alterable code:
                
                design = self.scene.addRect(
                    trig(trig(self.image_half / trig(self.prox_to_center)) - trig(self.starting_point) / trig(i)),
                    trig(trig(self.image_half / trig(self.prox_to_center)) - trig(self.starting_point)),
                    trig(self.rect_width + trig(self.starting_point)),
                    trig(self.rect_width + trig(self.starting_point)),
                    pen
                """

                transform = QTransform()
                transform.translate(self.image_half, self.image_half / 2)
                transform.rotate(round((i / j) * (360 / self.rect_count)))
                transform.rotate((j * (360 / self.rect_count)))
                design.setTransform(transform)

            if self.forward_true:
                self.starting_point += self.speed
            elif self.backward_true:
                self.starting_point -= self.speed

        self.scene.update()


class MyApplication(QApplication):
    def __init__(self, *args):

        super().__init__(*args)

    def set_invention(self, art_invention):
        self.art_invention = art_invention


if __name__ == '__main__':
    app = MyApplication(sys.argv)
    invention = ArtInvention()
    app.set_invention(invention)
    invention.show()

    sys.exit(app.exec())
