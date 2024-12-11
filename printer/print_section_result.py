from printer.printer import Printer
from datetime import date
import json
from collections import Counter
import os

printer = Printer()

def print_section_result():
    usb_drive_path = os.path.join('/media', 'pi', 'blockchurna_drive')
    file_name = os.path.join(usb_drive_path, "finalized_section.section")

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file) 
    except FileNotFoundError:
        print("Arquivo não encontrado. Certifique-se de que finalized_section.section está no local correto.")
        return
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON. Verifique o formato do arquivo.")
        return

    votes = data.get("votes", [])

    vote_counts = Counter(vote["candidate"] for vote in votes)

    # Print header information
    printer.open()
    printer.select_font('A')
    printer.set_bold(False)
    printer.set_text_size(1)
    printer.print_line("RESULTADO DE SECAO")
    printer.print_line("ELEICOES MUNICIPAIS 2024-1 TURNO")
    printer.print_line("DATA: " + date.today().strftime('%d/%m/%Y'))
    printer.print_line("")

    # Print vote results
    printer.select_font('A')
    printer.set_bold(False)
    printer.set_text_size(1)
    for candidate, count in vote_counts.items():
        printer.print_line(f"{candidate}: {count} voto(s)")
    
    printer.print_line("")

    # Print location details
    printer.print_line("UF: PR  Zona: 177  Secao: UTFPR")
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
