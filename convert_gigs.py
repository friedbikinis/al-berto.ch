import re
import sys

# Sicherstellen, dass UTF-8 für Standard-Ein/Ausgabe verwendet wird (falls nötig)
# Dies ist meist in Python 3 Standard, hilft aber bei manchen Systemen
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def convert_gig_list(input_file, output_file):
    # Regex-Pattern:
    # ^(\d+)           -> Erfasst die ID am Zeilenanfang (Gruppe 1)
    # \s+              -> Ein oder mehr Leerzeichen
    # (\d{2}\.\d{2}\.\d{4}) -> Erfasst das Datum TT.MM.JJJJ (Gruppe 2)
    # \s*-\s*          -> Der Bindestrich mit optionalen Leerzeichen drumherum
    # (.*)$            -> Erfasst den restlichen Text bis zum Ende der Zeile (Gruppe 3)
    pattern = re.compile(r'^(\d+)\s+(\d{2}\.\d{2}\.\d{4})\s*-\s*(.*)$')

    try:
        # Explizites Encoding/Decoding beim Öffnen der Dateien
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            
            lines_processed = 0
            
            for line in f_in:
                # HTML-Tags entfernen (z.B. <font size="1">)
                clean_line = re.sub(r'<[^>]*>', '', line).strip()
                
                if not clean_line:
                    continue # Leere Zeilen überspringen

                match = pattern.match(clean_line)
                
                if match:
                    gig_id = match.group(1)
                    gig_date = match.group(2)
                    gig_info = match.group(3).strip()
                    
                    # HTML Zeile schreiben
                    html_line = (
                        '    <tr>\n'
                        '      <td class="gig-id">{0}</td>\n'
                        '      <td class="gig-date">{1}</td>\n'
                        '      <td class="gig-info">{2}</td>\n'
                        '    </tr>\n'.format(gig_id, gig_date, gig_info)
                    )
                    f_out.write(html_line)
                    lines_processed += 1
                else:
                    # Warnung ohne Emojis
                    print("Warning: Line could not be processed: " + clean_line)

            # Erfolgsmeldung ohne Emojis
            print("Success! {} lines converted from '{}' to '{}'.".format(
                lines_processed, input_file, output_file))

    except FileNotFoundError:
        print("Error: The file '{}' was not found.".format(input_file))
    except UnicodeDecodeError:
        print("Error: Could not read file. Please ensure '{}' is saved as UTF-8.".format(input_file))
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))

if __name__ == "__main__":
    input_filename = 'list-concert-date-changed.txt'
    output_filename = 'gigs_html.txt'
    
    print("Starting conversion of {}...".format(input_filename))
    convert_gig_list(input_filename, output_filename)