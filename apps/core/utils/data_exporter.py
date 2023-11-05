import csv

from django.core.exceptions import ImproperlyConfigured
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views import View


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


class AdminExportMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_as_json(self, request, queryset):
        # Serialize the queryset
        data = serialize('json', queryset)

        # Create the HttpResponse object with the appropriate JSON header.
        response = HttpResponse(data, content_type='application/json')
        # Set the HTTP header for a download.
        response['Content-Disposition'] = 'attachment; filename={}.json'.format(self.model._meta)

        return response

    def export_as_text(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={}.txt'.format(meta)

        # Write header
        response.write(','.join(field_names) + '\n')

        # Write data rows
        for obj in queryset:
            row = ','.join([str(getattr(obj, field)) for field in field_names])
            response.write(row + '\n')

        return response


    export_as_csv.short_description = "Export selected to csv"
    export_as_json.short_description = "Export selected to json"
    export_as_text.short_description = "Export selected to text"
