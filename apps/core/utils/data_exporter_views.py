import csv

from django.http import HttpResponse
from django.views import View
import json
from django.core.serializers import serialize
from django.core.exceptions import ImproperlyConfigured

class BaseDataExporterView(View):
    """
    Base class for exporting data. This class should have common methods and attributes
    shared by all export formats.
    """
    model = None
    filename = 'export'

    def get_fields(self):
        # Return a list of field names (as strings) from the model
        return [field.name for field in self.model._meta.fields]

    def get_queryset(self):
        # Return a queryset of all objects by default. Override if needed.
        return self.model.objects.all()


class ExportToCSVView(BaseDataExporterView):
    filename = 'export.csv'

    def get(self, request, *args, **kwargs):
        # Validate file extension
        if not self.filename.lower().endswith('.csv'):
            raise ImproperlyConfigured("Filename must have a .csv extension for ExportToCSVView")

        # Create a response with a file of type csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Get fields
        fields = self.get_fields()

        # Write header
        writer.writerow(fields)

        # Get the data
        queryset = self.get_queryset()

        # Write rows
        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)
        return response


class ExportToJSONView(BaseDataExporterView):
    filename = 'export.json'

    def get(self, request, *args, **kwargs):
        # Validate file extension
        if not self.filename.lower().endswith('.json'):
            raise ImproperlyConfigured("Filename must have a .json extension for ExportToJSONView")

        data = serialize('json', self.get_queryset(), fields=self.get_fields())
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        return response


class ExportToTextView(BaseDataExporterView):
    filename = 'export.txt'

    def get(self, request, *args, **kwargs):
        # Validate file extension
        if not self.filename.lower().endswith('.txt'):
            raise ImproperlyConfigured("Filename must have a .txt extension for ExportToTextView")

        queryset = self.get_queryset()
        fields = self.get_fields()

        # Create a list of strings where each string is a line in the text file
        lines = []
        for obj in queryset:
            for field in fields:
                value = getattr(obj, field)
                lines.append(f"{field}: {value}")
            lines.append("\n")  # Add a blank line between objects for readability

        response = HttpResponse('\n'.join(lines), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        return response
