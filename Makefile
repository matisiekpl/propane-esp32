deploy:
	ampy -d 0.5 --port /dev/tty.usbserial-0001 -b 115200 put main.py

run:
	ampy -d 0.5 --port /dev/tty.usbserial-0001 -b 115200 run main.py

dry:
	ampy -d 0.5 --port /dev/tty.usbserial-0001 -b 115200 run dry.py

reset:
	esptool.py --port /dev/tty.usbserial-0001 erase_flash
	esptool.py --port /dev/tty.usbserial-0001 --chip esp32 write_flash -z 0x1000 ESP32_GENERIC-20240222-v1.22.2.bin