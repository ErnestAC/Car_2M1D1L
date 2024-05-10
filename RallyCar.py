#created by Peter Vanczak
#adapted by Ernest Aberg
#Version 02
from pybricks.hubs import TechnicHub
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Color, Direction, Port
from pybricks.pupdevices import Motor, Light
from pybricks.robotics import Car
from pybricks.tools import wait

# Set up all devices.
RallyCar = TechnicHub()
drl = Light(Port.A)
front = Motor(Port.D, Direction.CLOCKWISE)
rear = Motor(Port.B, Direction.CLOCKWISE)
steer = Motor(Port.C, Direction.CLOCKWISE)
car = Car(steer, [front, rear])
controller = XboxController()

# Initialize variables.
control_profile_actual = 0
Control_profile_choosen = 0
max_speed = 1500
pedal = 0
power = 0
acceleration = 4000 / 1000
nogas = 700 / 1000
brake = 3000 / 1000
motorbrake = 1000 / 1000
low_light_percent = 40
allow_light = 1

def direct_speed_control():
    car.drive_speed((max_speed / 100) * pedal)

def doWarning(FnlowLightPerc = low_light_percent, FnAllowLight = allow_light):
    drl.on(100)
    car.drive_speed(0)
    wait(400)
    drl.on(FnlowLightPerc * FnAllowLight)
    wait(400)

def copFlasher():
    drl.on(15)
    wait(750)
    drl.on(100)
    wait(15)
    drl.on(15)
    wait(75)
    drl.on(100)
    wait(15)
    drl.on(15)
    wait(75)
    drl.on(100)
    wait(15)

def fadeOnSlipOut(stayOn = 400, brigtnessSteps = 100):
    i = 0
    
    while i < brigtnessSteps:
        if i == 0:
            wait(stayOn)
        drl.on(i)
        i = i + 1
        wait(20)
    wait(stayOn)

def power_mode_realistic():
    global power
    if pedal == 0:
        if abs(power) <= 2:
            power = 0
        else:
            if power > 0:
                power = power - nogas
            else:
                power = power + nogas
    else:
        if power == 0:
            power = (pedal / abs(pedal)) * acceleration
        else:
            if power > 0:
                if pedal > 0:
                    if abs(power - pedal) <= acceleration * 0.66:
                        power = power
                    else:
                        if pedal > power:
                            power = power + acceleration
                        else:
                            power = power - motorbrake
                else:
                    power = power - brake * abs(pedal / 100)
                    if power <= 2:
                        power = 0
            else:
                if pedal < 0:
                    if abs(power - pedal) <= acceleration * 0.66:
                        power = power
                    else:
                        if pedal > power:
                            power = power + motorbrake
                        else:
                            power = power - acceleration
                else:
                    power = power + brake * abs(pedal / 100)
                    if power >= -2:
                        power = 0
    car.drive_power(power)


# The main program starts here.
front.control.limits(speed=max_speed)
rear.control.limits(speed=max_speed)
RallyCar.light.on(Color.CYAN)

while True:
        
    if Button.X in controller.buttons.pressed():
        Control_profile_choosen = 0
        RallyCar.light.on(Color.CYAN)
    else:
        pass
    if Button.B in controller.buttons.pressed():
        Control_profile_choosen = 1
        RallyCar.light.on(Color.MAGENTA)
    else:
        pass
    if Button.Y in controller.buttons.pressed() and Button.A in controller.buttons.pressed():
        RallyCar.light.on(Color.RED)
        break
    else:
        if Button.RB in controller.buttons.pressed() and Button.A in controller.buttons.pressed():
            car.drive_speed(0)

            RallyCar.light.animate([Color.NONE, Color.GREEN], interval=410)
            wait(70)
            while (Button.A not in controller.buttons.pressed()):
                copFlasher()
            if Control_profile_choosen == 1:
                RallyCar.light.on(Color.MAGENTA)        
            else:
                RallyCar.light.on(Color.CYAN) 

        
    if Button.LB in controller.buttons.pressed() and not Button.RB in controller.buttons.pressed():
        if allow_light == 1:
            allow_light = 0
            RallyCar.light.on(Color.NONE)
        else:
            allow_light = 1
            if Control_profile_choosen == 1:
                RallyCar.light.on(Color.MAGENTA)        
            else:
                RallyCar.light.on(Color.CYAN)   
        wait(500)


    if Button.RB in controller.buttons.pressed() and Button.LB in controller.buttons.pressed():
        car.drive_speed(0)

        RallyCar.light.animate([Color.NONE, Color.ORANGE], interval=410)
        wait(70)
        while (Button.RB not in controller.buttons.pressed()):
            doWarning()
        if Control_profile_choosen == 1:
            RallyCar.light.on(Color.MAGENTA)        
        else:
            RallyCar.light.on(Color.CYAN)        




    if Control_profile_choosen != control_profile_actual:
        if Control_profile_choosen == 0:
            front.control.pid(42484, 21242, 5310, 8, 15)
            rear.control.pid(42484, 21242, 5310, 8, 15)
        else:
            front.control.pid(10000, 21242, 5310, 8, 15)
            rear.control.pid(10000, 21242, 5310, 8, 15)
        control_profile_actual = Control_profile_choosen
    else:
        pass
    pedal = controller.triggers()[1] - controller.triggers()[0]

# brake light conditions
    EngineSpeed = front.speed(window=3)
    if (controller.triggers()[0] > 0 and EngineSpeed > 0) or (controller.triggers()[1] > 0 and EngineSpeed < 0):
        drl.on(100)
    else:
        if controller.triggers()[1] > 0 and controller.triggers()[0] > 0:
            drl.on(100)
        else:
            drl.on(low_light_percent * allow_light)
    


    if control_profile_actual == 0:
        power_mode_realistic()
    else:
        direct_speed_control()
    car.steer(controller.joystick_left()[0])
    wait(5)