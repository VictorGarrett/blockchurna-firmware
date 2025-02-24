from printer.printer import Printer
from datetime import date

printer = Printer()

def print_vote_receipt(voter_id, voter_name, counselor_vote_pin, mayor_vote_pin):
    print("Printing vote receipt...")
    # Print header information
    printer.open()
    printer.select_font('A')
    printer.set_bold(False)
    printer.set_text_size(1)
    printer.print_line("COMPROVANTE DE VOTACAO")
    printer.print_line("ELEICOES MUNICIPAIS 2024-1 TURNO")
    printer.print_line("DATA: " + date.today().strftime('%d/%m/%Y'))
    printer.print_line("")

    # Print voter name
    printer.set_bold(True)
    printer.select_font('A')
    printer.set_text_size(3)
    wrapped_name = "\n".join(_abbreviate_and_wrap(voter_name, 32, 0.5))
    printer.print_line(wrapped_name)
    printer.print_line("")

    # Print PIN codes
    printer.select_font('A')
    printer.set_bold(False)
    printer.set_text_size(1)
    printer.print_line(f"PIN VER: {counselor_vote_pin}")
    printer.print_line(f"PIN PRE: {mayor_vote_pin}")
    printer.print_line("")

    # Print Titulo Eleitoral and location details
    printer.print_line(f"ID do Eleitor: {voter_id}")
    printer.print_line("UF: PR  Zona: 177  Secao: UTFPR")
    printer.print_line("")
    printer.print_line("")
    printer.close()


def _abbreviate_and_wrap(name, printer_columns, bold_adjustment=0.1, max_lines=3):
    """
    Abbreviate and wrap a full name to fit within the printer's column limits.
    
    :param name: The full name as a string.
    :param printer_columns: The total number of columns (characters) per line.
    :param bold_adjustment: Reduction factor for bold text (default: 10%).
    :param max_lines: Maximum number of lines allowed (default: 3).
    :return: A list of strings representing the wrapped lines.
    """
    # Calculate the effective maximum characters per line
    max_chars_per_line = int(printer_columns * (1 - bold_adjustment))
    
    def abbreviate_middle_names(parts):
        """Abbreviate middle names to initials while keeping the first and last names intact."""
        if len(parts) <= 2:
            return parts  # No middle names to abbreviate
        return [parts[0]] + [f"{p[0]}." for p in parts[1:-1]] + [parts[-1]]

    def wrap_text(words):
        """Wrap text into lines based on the max characters per line."""
        lines, current_line = [], ""
        for word in words:
            # Check if adding the word exceeds the line limit
            if len(current_line) + len(word) + 1 <= max_chars_per_line:
                current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    # Split the name into parts
    name_parts = name.split()
    
    # First attempt: Use the full name
    lines = wrap_text(name_parts)
    if len(lines) <= max_lines:
        return lines

    # Second attempt: Abbreviate middle names
    abbreviated_parts = abbreviate_middle_names(name_parts)
    lines = wrap_text(abbreviated_parts)
    if len(lines) <= max_lines:
        return lines

    # Final attempt: Truncate the name to first and last name
    truncated_name = [name_parts[0], name_parts[-1]]
    lines = wrap_text(truncated_name)
    return lines[:max_lines]  # Ensure no more than max_lines are returned