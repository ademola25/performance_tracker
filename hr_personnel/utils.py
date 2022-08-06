import csv

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')




HEADERS = {
    'shop_id': {'field':'id', 'required':True},
    'platinum_member': {'field':'platinum_member', 'required':False},
}


def import_document_validator(document):
    # check file valid csv format
    try:
        dialect = csv.Sniffer().sniff(document.read(1024))
        document.seek(0, 0)
    except csv.Error:
        raise ValidationError(u'Not a valid CSV file')
    reader = csv.reader(document.read().splitlines(), dialect)
    csv_headers = []
    required_headers = [header_name for header_name, values in
                        HEADERS.items() if values['required']]
    for y_index, row in enumerate(reader):
        # check that all headers are present
        if y_index == 0:
            # store header_names to sanity check required cells later
            csv_headers = [header_name.lower() for header_name in row if header_name]
            missing_headers = set(required_headers) - set([r.lower() for r in row])
            if missing_headers:
                missing_headers_str = ', '.join(missing_headers)
                raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
            continue
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            continue
        # sanity check required cell values
        for x_index, cell_value in enumerate(row):
            # if indexerror, probably an empty cell past the headers col count
            try:
                csv_headers[x_index]
            except IndexError:
                continue
            if csv_headers[x_index] in required_headers:
                if not cell_value:
                    raise ValidationError(u'Missing required value %s for row %s' %
                                            (csv_headers[x_index], y_index + 1))
    return True