# Register your models here.
from django.contrib import admin

from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget, ForeignKeyWidget
from .models import *


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

# class SutraName(Widget):
#     def clean(self, value, row=None, *args, **kwargs):
#         return self._instance.sutra.name
#
#     def render(self, value, obj=None):
#         return value

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

    def render(self, value, obj=None):
        return value

class RollRescource(ModelResource):
    series = fields.Field(
        column_name='series',
        attribute='series',
        widget=MyForeignKeyWidget(Series, 'code'))
    sutra = fields.Field(
        column_name='sutra',
        attribute='sutra',
        widget=MyForeignKeyWidget(Sutra, 'code'))
    # name = fields.Field(
    #     column_name='name',
    #     attribute='name',
    #     widget=SutraName())
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
        export_order = ('series', 'sutra', 'name', 'type', 'code', 'start_volume', 'start_page', 'end_page', 'end_volume', 'remark')
        fields = ('code', 'name', 'type', 'series', 'sutra', 'start_volume', 'end_volume', 'start_page', 'end_page', 'remark')

    # def after_import_instance(self, instance, new, **kwargs):
    #     for field in self.get_fields():
    #         if isinstance(field.widget, SutraName):
    #             field.widget._instance = instance

    def before_save_instance(self, instance, using_transactions, dry_run):
        if not using_transactions and dry_run:
            pass
        else:
            instance.before_save()

    def after_save_instance(self, instance, using_transactions, dry_run):
        if not using_transactions and dry_run:
            pass
        else:
            instance.after_save()

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if using_transactions:
            if dry_run or result.has_errors():
                pass
            else:
                #此处可做一些数据的统计, 例如新增多少, 更新多少,
                #还有, 对此次导入的卷数, 册数, 经数, 页数, 以及初始化所有页基础数据.
                pass


class RollAdmin(ImportMixin, admin.ModelAdmin):
    def real_page_count(self, instance):
        count = Page.objects.filter(roll=instance.id).count()
        if count > 0:
            return """<a href='/xadmin/core/page/?_p_roll__id__exact=%s'>%s</a>""" % (instance.id, count)
        return count
    real_page_count.short_description = "实存页数"
    real_page_count.allow_tags = True
    real_page_count.is_column = True

    list_display = ("series", "sutra", "code", "type", "name", "start_volume", "start_page", "end_page",  "end_volume", "real_page_count", "remark")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name"]
    list_filter = ["series", "sutra", "code", ]
    relfield_style = "fk-select"
    reversion_enable = True
    resource_class = RollRescource

# admin.site.register(LQSutra, LQSutraAdmin)
admin.site.register(Roll, RollAdmin)
admin.site.site_header = '龙泉大藏经'
admin.site.site_title = '龙泉大藏经'
admin.site.index_title = '龙泉大藏经'