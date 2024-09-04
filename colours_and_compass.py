import time
import math
import board
import busio
import adafruit_tcs34725
import adafruit_lsm303dlh_mag
import adafruit_ssd1306
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)

rgb_sensor = adafruit_tcs34725.TCS34725(i2c)

compass = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

WIDTH = 128
HEIGHT = 64
BORDER = 5
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

def is_north(magnetic_field):
    x, y, _ = magnetic_field 
    angle = math.degrees(math.atan2(y, x))
    print(angle)
    return -30 <= angle <= 30

def display_rgb(r, g, b):
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    
    draw.text((0, 0), f"R: {r}", font=font, fill=255)
    draw.text((0, 10), f"G: {g}", font=font, fill=255)
    draw.text((0, 20), f"B: {b}", font=font, fill=255)
    
    oled.image(image)
    oled.show()

def main():
    try:
        while True:
            r, g, b = rgb_sensor.color_rgb_bytes
            print(f"Color: R={r}, G={g}, B={b}")
            
            display_rgb(r, g, b)

            magnetic_field = compass.magnetic
            print(f"Magnetic field: {magnetic_field}")

            if is_north(magnetic_field):
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("North detected: LED ON")
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
                print("Not North: LED OFF")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
