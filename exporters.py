import json
import dicttoxml
from datetime import timedelta, datetime, date
from decimal import Decimal

class ExportFactory:
    @staticmethod
    def _prepare_data(obj):
        """Recursively convert EVERYTHING into XML-friendly types (lists, dicts, strings)."""
        # 1. Handle Lists and Tuples (Crucial for SQL results)
        if isinstance(obj, (list, tuple)):
            return [ExportFactory._prepare_data(item) for item in obj]
        
        # 2. Handle Dictionaries
        if isinstance(obj, dict):
            return {str(k): ExportFactory._prepare_data(v) for k, v in obj.items()}
        
        # 3. Handle the 'Illegal' XML types (Timedelta, Decimal, Dates)
        if isinstance(obj, (timedelta, Decimal, datetime, date)):
            return str(obj)
        
        # 4. Return basic types (int, str, float, bool) as they are
        return obj

    @staticmethod
    def export(data, format_type):
        # Thoroughly scrub the data
        clean_data = ExportFactory._prepare_data(data)
        
        filename = "report"
        
        if format_type == 'json':
            with open(f"{filename}.json", "w", encoding='utf-8') as f:
                json.dump(clean_data, f, indent=4)
            print(f"Successfully exported to {filename}.json")
        
        elif format_type == 'xml':
            try:
                # attr_type=False makes the XML much cleaner
                xml_binary = dicttoxml.dicttoxml(clean_data, custom_root='root', attr_type=False)
                with open(f"{filename}.xml", "wb") as f:
                    f.write(xml_binary)
                print(f"Successfully exported to {filename}.xml")
            except Exception as e:
                # This will tell us EXACTLY what the library is still crying about
                print(f"XML Export Error: {e}")