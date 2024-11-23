from printer import Printer

printer = Printer("/dev/usb/lp1")

if printer.printer:
    # Print header information
    printer.select_font('A')
    printer.set_bold(False)
    printer.set_text_size(1)
    printer.print_line("COMPROVANTE DE VOTACAO")
    printer.print_line("ELEICOES MUNICIPAIS 2024-1 TURNO")
    printer.print_line("DATA: 06/10/2024")
    printer.print_line("")

    # Print voter name
    printer.set_bold(True)
    printer.select_font('A')
    printer.set_text_size(3)
    printer.print_line("FULANO DA SILVA SAURO")
    printer.print_line("")

    # Print PIN codes
    printer.select_font('A')
    printer.set_bold(False)
    printer.set_text_size(1)
    printer.print_line("PIN VER:1234 5678 90AB CDEF GHIJ")
    printer.print_line("PIN PRE:1234 5678 90AB CDEF GHIJ")
    printer.print_line("")

    # Print Titulo Eleitoral and location details
    printer.print_line("Titulo Eleitoral: XXXX YYYY ZZZZ")
    printer.print_line("UF:UF    Zona:ZZZZ    Secao:SSSS")
    printer.print_line("")
    printer.print_line("")

