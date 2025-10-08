#!/usr/bin/env python3
"""
Servo diagnostics helper for Raspberry Pi.

Usage:
  sudo python3 servo_diagnostics.py [--pin BCM_PIN]

What it does:
  - Tries pigpio (best) to send servo pulse widths (500, 1500, 2500 us)
  - Falls back to RPi.GPIO software PWM (50Hz) if pigpio isn't available
  - Falls back to gpiozero Servo if nothing else available

Notes / common fixes:
  - Ensure you're using BCM pin numbering. `Servo(18)` means BCM 18 (physical pin 12).
  - Verify the servo power: use an external 5V supply capable of the servo current and connect its GND to the Pi GND.
  - Many servos draw >500mA on move; powering from the Pi 5V rail can cause brownouts.
  - pigpio provides more stable servo pulses on modern Pi models. Install with: sudo apt install pigpio python3-pigpio && sudo systemctl enable --now pigpiod
  - If the servo still doesn't move, check wiring, try a different pin, and confirm the servo isn't damaged.
"""

import time
import argparse
import sys


def print_wiring_checks(pin):
    print(f"Testing servo on BCM pin {pin} (physical pin may differ).")
    print("Wiring checklist:")
    print(" - Servo +V should be 5V (or appropriate for your servo), not the Pi's 3.3V signal pin.")
    print(" - Servo GND must be connected to Pi GND.")
    print(" - Control wire should be connected to the BCM pin (not the 5V pin).")
    print(" - Use an external 5V supply for the servo if it draws significant current.")
    print()


def try_pigpio(pin):
    try:
        import pigpio
    except Exception as e:
        print("pigpio not available:", e)
        return False

    print("Trying pigpio backend (recommended)")
    pi = pigpio.pi()
    if not pi.connected:
        print("pigpio daemon not running or couldn't connect. Start it with:")
        print("  sudo systemctl enable --now pigpiod")
        pi.stop()
        return False

    try:
        for pulse in (500, 1500, 2500):
            print(f"Setting pulsewidth {pulse} us")
            pi.set_servo_pulsewidth(pin, pulse)
            time.sleep(2)
        print("Stopping pulses (set pulsewidth 0)")
        pi.set_servo_pulsewidth(pin, 0)
    finally:
        pi.stop()
    return True


def try_rpigpio_pwm(pin):
    try:
        import RPi.GPIO as GPIO
    except Exception as e:
        print("RPi.GPIO not available:", e)
        return False

    print("Trying RPi.GPIO PWM backend at 50Hz")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz -> 20ms period
    pwm.start(0)
    try:
        for pulse in (500, 1500, 2500):
            # Convert microseconds to duty cycle percent (pulse_us / 20000 * 100)
            duty = (pulse / 20000.0) * 100.0
            print(f"Setting pulse {pulse}us -> duty {duty:.2f}%")
            pwm.ChangeDutyCycle(duty)
            time.sleep(2)
        print("Stopping PWM (duty 0)")
        pwm.ChangeDutyCycle(0)
    finally:
        pwm.stop()
        GPIO.cleanup()
    return True


def try_gpiozero_servo(pin):
    try:
        from gpiozero import Servo
    except Exception as e:
        print("gpiozero Servo not available:", e)
        return False

    print("Trying gpiozero Servo (uses software PWM) with common pulse widths")
    # Use typical 0.5ms-2.5ms window; adjust if your servo expects 1ms-2ms
    servo = Servo(pin, min_pulse_width=500/1_000_000, max_pulse_width=2500/1_000_000)
    try:
        print("Moving to min (-1)")
        servo.value = -1
        time.sleep(2)
        print("Moving to mid (0)")
        servo.value = 0
        time.sleep(2)
        print("Moving to max (+1)")
        servo.value = 1
        time.sleep(2)
    finally:
        servo.detach()
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pin', type=int, default=18, help='BCM pin number to test (default 18)')
    args = parser.parse_args()

    pin = args.pin
    print_wiring_checks(pin)

    # Try pigpio first
    if try_pigpio(pin):
        print("pigpio test completed")
        return

    # Try RPi.GPIO PWM
    if try_rpigpio_pwm(pin):
        print("RPi.GPIO PWM test completed")
        return

    # Fallback to gpiozero
    if try_gpiozero_servo(pin):
        print("gpiozero test completed")
        return

    print("No supported backend worked. Install pigpio (recommended) or RPi.GPIO/gpiozero.")
    print("To install pigpio: sudo apt install pigpio python3-pigpio && sudo systemctl enable --now pigpiod")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        sys.exit(0)
