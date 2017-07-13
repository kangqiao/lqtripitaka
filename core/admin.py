# Register your models here.
from django.contrib import admin

from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget, ForeignKeyWidget
from .models import *

# class LQSutraResource(ModelResource):
#     class Meta:
#         model = LQSutra
#
#     def import_data(self, dataset, dry_run=False, raise_errors=False,
#                     use_transactions=None, collect_failed_rows=False, **kwargs):
#         pass
#
#     def before_import(self, dataset, using_transactions, dry_run, **kwargs):
#         pass
#
#
# class LQSutraAdmin(ImportMixin, admin.ModelAdmin):
#     def show_lqsutra_list(self, instance):
#         list = instance.lqsutra_list.all()
#         ret = """<a href="/xadmin/core/sutra/?_p_lqsutra__id__exact=%s" >""" % instance.id
#         for sutra in list:
#             ret += """%s -> %s <br>""" % (sutra.code, sutra.name)
#         ret += """</a>"""
#         return ret
#     show_lqsutra_list.short_description = "龙泉收录"
#     show_lqsutra_list.allow_tags = True
#     show_lqsutra_list.is_column = True
#     list_display = ("code", "name", "show_lqsutra_list", "remark")
#     resource_class = LQSutraResource


class MyForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        instance = None
        try:
            instance = super(MyForeignKeyWidget, self).clean(value, row)
        except Exception as e:
            pass
        if not instance:
            instance = self.model()
            setattr(instance, self.field, value)
        return instance

class CacheDuplicateWidget(ForeignKeyWidget):
    cacheMap = {}
    def clean(self, value, row=None, *args, **kwargs):
        instance = None
        try:
            instance = super(CacheDuplicateWidget, self).clean(value, row)
        except Exception as e:
            pass
        if not instance:
            if value in CacheDuplicateWidget.cacheMap:
                instance = CacheDuplicateWidget.cacheMap.get(value)
            else:
                instance = self.model()
                setattr(instance, self.field, value)
                CacheDuplicateWidget.cacheMap[value] = instance
        return instance

class RollRescource(ModelResource):
    series = fields.Field(
        column_name='series',
        attribute='series',
        widget=MyForeignKeyWidget(Series, 'code'))
    sutra = fields.Field(
        column_name='sutra',
        attribute='sutra',
        widget=MyForeignKeyWidget(Sutra, 'code'))
    start_volume = fields.Field(
        column_name='start_volume',
        attribute='start_volume',
        widget=CacheDuplicateWidget(Volume, 'code'))
    end_volume = fields.Field(
        column_name='end_volume',
        attribute='end_volume',
        widget=CacheDuplicateWidget(Volume, 'code'))
    start_page = fields.Field(
        column_name='start_page',
        attribute='start_page',
        widget=CacheDuplicateWidget(Page, 'code'))
    end_page = fields.Field(
        column_name='end_page',
        attribute='end_page',
        widget=CacheDuplicateWidget(Page, 'code'))
    class Meta:
        model = Roll
        import_id_fields = ('code',)
        fields = ('code', 'name', 'type', 'series', 'sutra', 'start_volume', 'end_volume', 'start_page', 'end_page', 'remark')

    def before_save_instance(self, instance, using_transactions, dry_run):
        if not using_transactions and dry_run:
            pass
        else:
            instance.series.save()
            instance.series = instance.series
            instance.sutra.save()
            instance.sutra = instance.sutra
            instance.start_volume.save()
            instance.start_volume = instance.start_volume.code
            instance.end_volume.save()
            instance.end_volume = instance.end_volume.code
            instance.start_page.save()
            instance.start_page = instance.start_page.code
            instance.end_page.save()
            instance.end_page = instance.end_page.code


class RollAdmin(ImportMixin, admin.ModelAdmin):
    def real_page_count(self, instance):
        count = Page.objects.filter(roll=instance.id).count()
        if count > 0:
            return """<a href='/xadmin/core/page/?_p_roll__id__exact=%s'>%s</a>""" % (instance.id, count)
        return count
    real_page_count.short_description = "实存页数"
    real_page_count.allow_tags = True
    real_page_count.is_column = True

    list_display = ("code", "name", "type", "series", "sutra", "start_volume", "end_volume", "start_page", "end_page", "page_count", "real_page_count", "qianziwen")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name"]
    list_filter = ["series", "sutra", "code", ]
    relfield_style = "fk-select"
    reversion_enable = True
    resource_class = RollRescource

# admin.site.register(LQSutra, LQSutraAdmin)
admin.site.register(Roll, RollAdmin)