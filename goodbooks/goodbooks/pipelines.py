# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class GoodbooksPipeline:
    #def process_item(self, item, spider):
    #    return item

    def open_spider(self, spider):
        self.filename_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.filename_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        filename = str(item['item-type']) + 'info'
        del item['item-type']
        if filename not in self.filename_to_exporter:
            f = open(f'{filename}.csv', 'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.filename_to_exporter[filename] = exporter
        return self.filename_to_exporter[filename]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
