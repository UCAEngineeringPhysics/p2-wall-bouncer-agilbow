from time import sleep, sleep_us, sleep_ms, ticks_us
from machine import Pin, PWM
from dual_motor_driver import DualMotorDriver
from distance_sensor import DistanceSensor

# SETUP

ds = DistanceSensor(trig_id=3, echo_id=2)

dmd = DualMotorDriver(left_ids=(15, 13, 14), right_ids=(16, 18, 17), stby_id=12)
dmd.enable()



ledRed = PWM(Pin(28))
ledBlue = PWM(Pin(26))
ledGreen = PWM(Pin(27))

ledRed.freq(1000)
ledBlue.freq(1000)
ledGreen.freq(1000)

button = Pin(21, Pin.IN, Pin.PULL_UP)


def mode_switch(pin):
    global modeValue
    modeValue += 1
    
button.irq(trigger= Pin.IRQ_RISING, handler=mode_switch)

modeValue = 1


firstDutyIncrease = 655
firstDutyDecrease = 655
firstDutyValue = 0

secondDutyValue = 0
secondDutyIncrease = 655
secondDutyDecrease = 655

dutyValue = 0
dutyIncrease = 655
dutyDecrease = 655

workTimeCounter = 0
resetCounter = 0

# LOOP

# 1. All three LEDs need to blink at a rate of 5Hz for 2 seconds.

#The two for loops nested in the first for loop run for a total of 0.2 seconds, so making
#this last 2 seconds can be done by running the two for loops 10 times.

while True:
    d = ds.distance
    if modeValue == 1 and d != None:
        for r in range(10):
            for i in range(100):
                ledRed.duty_u16(dutyValue)
                ledBlue.duty_u16(dutyValue)
                ledGreen.duty_u16(dutyValue)
                dutyValue += dutyIncrease
                sleep(1/1000)
            for i in reversed(range(100)):
                ledRed.duty_u16(dutyValue)
                ledBlue.duty_u16(dutyValue)
                ledGreen.duty_u16(dutyValue)
                dutyValue -= dutyDecrease
                sleep(1/1000)
        break
ledRed.duty_u16(0)
ledBlue.duty_u16(0)
ledGreen.duty_u16(0)


# 2/3. Switching between pause mode and work mode.

while True:
#     d = ds.distance
#     print(d)
    if modeValue % 2 != 0:
        dutyValue = 0
        for i in range(100):
            ledGreen.duty_u16(dutyValue)
            dutyValue = dutyValue + dutyIncrease
            sleep(0.5/100)
        for i in reversed(range(100)):
            ledGreen.duty_u16(dutyValue)
            dutyValue = dutyValue - dutyDecrease
            sleep(0.5/100)
    else:
        ledGreen.duty_u16(65535)
        print(workTimeCounter)
        d = ds.distance
        print(d)
        
        if d != None and d <= 0.35:
            dmd.stop()
            sleep(0.5)
            dmd.linear_backward(0.2)
            sleep(0.5)
            dmd.stop()
            dmd.spin_right(0.2)
            sleep(1)
            dmd.stop()
            workTimeCounter += 2.4
        elif d != None and d > 0.35:
            dmd.linear_forward(0.5)
            
        sleep(0.1)
        workTimeCounter += 0.1
        
#         d = ds.distance
#         print(d)
        if modeValue % 2 != 0:
            print("Pausing")
            dmd.stop()
            continue
        if workTimeCounter >= 44 and workTimeCounter <= 46:
            print("Battery Low")
            break

ledGreen.duty_u16(0)

# 4. Work time at 45 seconds.

while True:
#     d = ds.distance
#     print(d)
    if modeValue % 2 != 0:
        dmd.stop()
        dutyValue = 0
        for i in range(100):
            ledBlue.duty_u16(dutyValue)
            dutyValue = dutyValue + dutyIncrease
            sleep(0.5/100)
        for i in reversed(range(100)):
            ledBlue.duty_u16(dutyValue)
            dutyValue = dutyValue - dutyDecrease
            sleep(0.5/100)
    else:
        ledBlue.duty_u16(65535)
        sleep(0.2)
        workTimeCounter += 0.2
        print(workTimeCounter)
        d = ds.distance
        print(d)
        
        dmd.linear_forward(0.4)
        
        if d != None and d <= 0.35:
            dmd.stop()
            sleep(0.5)
            dmd.linear_backward(0.2)
            sleep(0.5)
            dmd.stop()
            dmd.spin_right(0.2)
            sleep(1)
            dmd.stop()
            workTimeCounter += 2.4
        elif d != None and d > 0.35:
            dmd.linear_forward(0.25)
        
#         d = ds.distance
#         print(d)
        if modeValue % 2 != 0:
            print("Pausing")
            dmd.stop()
            continue
        if workTimeCounter >= 54 and workTimeCounter <= 56:
            print("Battery Critical")
            break

ledBlue.duty_u16(0)
dutyValue = 0

# 4. (again) Work time at 55 seconds.

while True:
#     d = ds.distance
#     print(d)
    if modeValue % 2 != 0:
        secondDutyValue = 0
        for i in range(100):
            ledRed.duty_u16(dutyValue)
            dutyValue += dutyIncrease
            sleep(1/2000)
        for i in reversed(range(100)):
            ledRed.duty_u16(dutyValue)
            dutyValue -= dutyDecrease
            sleep(1/2000)
        resetCounter += 0.005
        print(resetCounter)
        if resetCounter >= 5 and resetCounter <= 5.01:
            machine.reset()
    else:
#         ledBlue.duty_u16(65535)
        secondDutyValue = 0
        for i in range(100):
            ledRed.duty_u16(secondDutyValue)
            secondDutyValue += secondDutyIncrease
            sleep(1/2000)
        for i in reversed(range(100)):
            ledRed.duty_u16(secondDutyValue)
            secondDutyValue -= secondDutyDecrease
            sleep(1/2000)
        
        d = ds.distance
        print(d)
        
        dmd.linear_forward(0.4)
        
        if d != None and d <= 0.35:
            dmd.stop()
            sleep(0.5)
            dmd.linear_backward(0.2)
            sleep(0.5)
            dmd.stop()
            dmd.spin_right(0.2)
            sleep(1)
            dmd.stop()
            workTimeCounter += 2.4
        elif d != None and d > 0.35:
            dmd.linear_forward(0.25)
        
        resetCounter += 0.005
        print(resetCounter)
#         d = ds.distance
#         print(d)
        if resetCounter >= 5:
            machine.reset()
        if modeValue % 2 != 0:
            dmd.stop()
            continue

ledRed.duty_u16(0)
ledBlue.duty_u16(0)
ledGreen.duty_u16(0)

