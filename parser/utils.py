def parse_date(unformatted_data):
    if len(unformatted_data) == 8:
        return '-'.join((
            unformatted_data[0:4],
            unformatted_data[4:6],
            unformatted_data[6:8]
        ))
    else:
        return ''