def parse_date(unformatted_data):
    if len(unformatted_data) == 8:
        return '-'.join((
            unformatted_data[0:4],
            unformatted_data[4:6],
            unformatted_data[6:8]
        ))
    else:
        return None
    
def parse_valid_date_or_none(unformatted_data):
    if int(unformatted_data) > 0:
        return parse_date(unformatted_data)
    else:
        return None

def parse_int(text):
    if text.isdigit():
        return int(text)

    return None

def parse_float(text):
    try:
        return float(text.replace(',', '.'))
    except ValueError:
        return None

def parse_cnae(cnae_text_list):
    if len(cnae_text_list) > 0:
        cnaes = cnae_text_list.split(',')

        return cnaes[0]

    return None