# ESC/POS Commands
ESC = b'\x1b'
GS = b'\x1d'
NEWLINE = b'\n'

class Printer:
    def __init__(self, printer_device="/dev/usb/lp0"):
        self.printer_device = printer_device
    
    def set_text_size(self, size=1):
        """Set text size based on size parameter (1-8)."""
        if not self.printer:
            return
        if size < 1:
            size = 1
        elif size > 8:
            size = 8
        size_byte = (size - 1) << 4 | (size - 1)
        self.printer.write(ESC + b'\x21' + bytes([size_byte]))

    def set_bold(self, enable=True):
        """Enable bold if enable=True, otherwise disable."""
        if not self.printer:
            return
        self.printer.write(ESC + b'\x45' + (b'\x01' if enable else b'\x00'))

    def select_font(self, font='A'):
        """Select Font A (default) or Font B."""
        if not self.printer:
            return
        if font.upper() == 'B':
            self.printer.write(ESC + b'\x4d\x01')
        else:
            self.printer.write(ESC + b'\x4d\x00')

    def set_underline(self, style=0):
        """Set underline style: 0 = none, 1 = single, 2 = double."""
        if not self.printer:
            return
        if style not in [0, 1, 2]:
            style = 0
        self.printer.write(ESC + b'\x2d' + bytes([style]))

    def set_alignment(self, alignment='left'):
        """Set text alignment: 'left', 'center', or 'right'."""
        if not self.printer:
            return
        alignments = {'left': 0, 'center': 1, 'right': 2}
        align_code = alignments.get(alignment.lower(), 0)
        self.printer.write(ESC + b'\x61' + bytes([align_code]))

    def set_invert(self, enable=True):
        """Enable or disable inverted text (white on black)."""
        if not self.printer:
            return
        self.printer.write(ESC + b'\x42' + (b'\x01' if enable else b'\x00'))

    def set_character_spacing(self, spacing=0):
        """Set character spacing in dots."""
        if not self.printer:
            return
        self.printer.write(ESC + b'\x20' + bytes([spacing]))

    def set_line_spacing(self, spacing=30):
        """Set line spacing in dots."""
        if not self.printer:
            return
        self.printer.write(ESC + b'\x33' + bytes([spacing]))

    def open(self):
        """Open the connection to the printer."""
        if not self.printer:
            try:
                self.printer_device = self.printer_device
                self.printer = open(self.printer_device, 'wb')
                print(f"Connected to printer at {self.printer_device}")
            except FileNotFoundError:
                self.printer = None
                print(f"Printer device {self.printer_device} not found.")
            except PermissionError:
                self.printer = None
                print(f"Permission denied for {self.printer_device}. Try running with sudo.")

    def close(self):
        """Close the connection to the printer."""
        if self.printer:
            self.printer.close()
            self.printer = None
            print("Printer connection closed.")

    def print_line(self, text):
        """Print a line of text and move to the next line."""
        if not self.printer:
            return
        
        if (len(text) and text[-1] == '\n'):
            text = text[:-1]

        self.printer.write(text.encode() + NEWLINE)
