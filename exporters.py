import json
import dicttoxml

class ExportFactory:
    @staticmethod
    def export(data, format_type):
        if format_type == 'json':
            with open("report.json", "w") as f:
                json.dump(data, f, indent=4, default=str)
        elif format_type == 'xml':
            xml = dicttoxml.dicttoxml(data)
            with open("report.xml", "wb") as f:
                f.write(xml)
        print(f"Successfully exported to {format_type}")