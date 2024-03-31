from escpos.printer import Serial

serial_port = "COM3"
printer = Serial(serial_port, baudrate=9600)
printer.text("hello")
printer.cut()