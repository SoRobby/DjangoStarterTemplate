import csv

from django.http import HttpResponse
from django.views import View


class ExportToCSVView(View):
    model = None
    filename = 'export.csv'

    def get_fields(self):
        # Return a list of field names (as strings) from the model
        return [field.name for field in self.model._meta.fields]

    def get_queryset(self):
        # Return a queryset of all objects by default. Override if needed.
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        # Create a response with a csv mime type
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Get fields
        fields = self.get_fields()

        # Write header
        writer.writerow(fields)

        # Get data
        queryset = self.get_queryset()

        # Write rows
        for obj in queryset:
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)

        return response
