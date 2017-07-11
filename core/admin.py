from django.contrib import admin

# Register your models here.
from django.contrib import admin
import xadmin

from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin, ImportExportModelAdmin

from .models import *

class LQSutraResource(ModelResource):



    class Meta:
        model = LQSutra

    def import_data(self, dataset, dry_run=False, raise_errors=False,
                    use_transactions=None, collect_failed_rows=False, **kwargs):
        pass

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        pass


class LQSutraAdmin(ImportMixin, admin.ModelAdmin):
    def show_lqsutra_list(self, instance):
        list = instance.lqsutra_list.all()
        ret = """<a href="/xadmin/core/sutra/?_p_lqsutra__id__exact=%s" >""" % instance.id
        for sutra in list:
            ret += """%s -> %s <br>""" % (sutra.code, sutra.name)
        ret += """</a>"""
        return ret
    show_lqsutra_list.short_description = "龙泉收录"
    show_lqsutra_list.allow_tags = True
    show_lqsutra_list.is_column = True
    list_display = ("code", "name", "show_lqsutra_list", "remark")
    resource_class = LQSutraResource



class RollRescource(ModelResource):
    class Meta:
        model = Roll
        import_id_fields = ('code',)
        fields = ('sutra__code', 'sutra__name', 'name', 'start_volume', 'end_volume', 'start_page', 'end_page')

class RollAdmin(ImportExportModelAdmin):
    def real_page_count(self, instance):
        count = Page.objects.filter(roll=instance.id).count()
        if count > 0:
            return """<a href='/xadmin/core/page/?_p_roll__id__exact=%s'>%s</a>""" % (instance.id, count)
        return count
    real_page_count.short_description = "实存页数"
    real_page_count.allow_tags = True
    real_page_count.is_column = True

    list_display = ("code", "name", "type", "series", "sutra", "page_count", "real_page_count", "qianziwen")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name", "qianziwen"]
    list_filter = ["series", "sutra", "code", ]
    relfield_style = "fk-select"
    reversion_enable = True
    resource_class = LQSutraResource

admin.site.register(LQSutra, LQSutraAdmin)
admin.site.register(Roll, RollAdmin)