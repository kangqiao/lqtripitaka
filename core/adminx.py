from __future__ import absolute_import
import xadmin
from xadmin import views
from .models import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction


@xadmin.sites.register(views.website.IndexView)
class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": u"大藏经", "content": "<h3> 欢迎来到龙泉大藏经管理平台 </h3><p>项目地址: https://github.com/kangqiao/lqtripitaka<br/>QQ: 279197764</p>"},
            {"type": "list", "model": "core.Series", "params": {"o": "-code"}},
            {"type": "chart", "model": "core.accessrecord", "chart": "user_count","params": {"_p_date__gte": "2017-01-01", "p": 1, "_p_date__lt": "2017-06-16"}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start","btns": [{"model": Series}, {"model": Sutra}, {"title": "Google", "url": "http://www.google.com"}]},
            #{"type": "addform", "model": Series},
            {"type": "list", "model": "core.Sutra", "params": {"o": "-code"}}
        ]
    ]


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    global_search_models = [Series, Sutra, Translator]
    global_models_icon = {
        Series: "fa fa-laptop", Sutra: "fa fa-square", Volume: "fa fa-copy", Roll: "fa fa-bars", Page: "fa fa-pagelines", Translator: "fa fa-flag"
    }
    menu_style = 'default'  # 'accordion'


@xadmin.sites.register(Series)
class SeriesAdmin(object):
    list_display = ("code", "name", "type", "dynasty", "volume_count", "sutra_count", "publish_name", "publish_date")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name", 'dynasty', 'type', 'publish_name']
    relfield_style = "fk-select"
    reversion_enable = True


@xadmin.sites.register(Volume)
class VolumeAdmin(object):
    list_display = ("code", "name", "series", "remark")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name"]
    relfield_style = "fk-select"
    reversion_enable = True


@xadmin.sites.register(Sutra)
class SutraAdmin(object):
    list_display = ("code", "name", "type", "clazz", "series", "translator", "dynasty", "historic_site", "roll_count", "qianziwen")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name", "type", "clazz", "series", "translator", "dynasty", "historic_site", "qianziwen"]
    relfield_style = "fk-select"
    reversion_enable = True


@xadmin.sites.register(Roll)
class RollAdmin(object):
    list_display = ("code", "name", "series", "sutra", "page_count", "qianziwen")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name", "qianziwen"]
    relfield_style = "fk-select"
    reversion_enable = True

class PageResourceInline(object):
    model = PageResource
    extra = 1
    style = "accordion"

@xadmin.sites.register(Page)
class PageAdmin(object):

    def open_page_resource(self, instance):
        count = instance.page_resources.count()
        return count
    open_page_resource.short_description = "Resource"
    open_page_resource.allow_tags = True
    open_page_resource.is_column = True

    list_display = ("code", "name", "type", "series", "volume", "sutra", "roll", "pre_page", "next_page", "open_page_resource")
    list_display_links = ("code", "name",)

    relfield_style = "fk-select"
    style_fields = {"system": "radio-inline"}
    reversion_enable = True
    actions = [BatchChangeAction, ]
    inlines = [PageResourceInline]

    search_fields = ["code", "name"]
    list_filter = [
        "series", "volume", "sutra", "roll", (
            "code",
            xadmin.filters.MultiSelectFieldListFilter,
        ),
    ]

    # form_layout = (
    #     Col("col1",
    #         Fieldset("页", "code", "name", "type", "series", "volume", "sutra", "roll", "pre_page", "next_page"),
    #         span=6, horizontal=True
    #         ),
    #     Col("col2",
    #         Inline(PageResourceInline),
    #         span=4, horizontal=True
    #         )
    # )



@xadmin.sites.register(Translator)
class TranslatorAdmin(object):
    list_display = ("name", "type", "remark")
    list_display_links = ("name",)
    wizard_form_list = [
        ("First's Form", ("name", "type")),
        ("Second Form", ("remark",))
    ]

    search_fields = ["name", "type", "remark"]
    relfield_style = "fk-select"
    reversion_enable = True
    actions = [BatchChangeAction, ]


@xadmin.sites.register(NormName)
class NormNameAdmin(object):
    def get_map_list(self, instance):
        list = instance.map_list.all()
        ret = ""
        for map in list:
            ret += """<a href="/xadmin/core/normnamemap/%s/update/" >%s</a> | """ % (map.id, map.name)
        return ret
    get_map_list.short_description = "相关对照列表"
    get_map_list.allow_tags = True
    get_map_list.is_column = True

    list_display = ("type", "name", "get_map_list")
    list_display_links = ("name",)
    search_fields = ["type", "name"]
    relfield_style = "fk-select"
    reversion_enable = True
    list_filter = [
        "type", "name",
    ]


@xadmin.sites.register(NormNameMap)
class NormNameMapAdmin(object):
    list_display = ("name", "type", "norm_name", "remark")
    list_display_links = ("name", "norm_name")
    search_fields = ["name", "type", "norm_name"]
    relfield_style = "fk-select"
    reversion_enable = True
    list_filter = [
        "type", "norm_name", "name",
    ]

@xadmin.sites.register(AccessRecord)
class AccessRecordAdmin(object):
    def avg_count(self, instance):
        return int(instance.view_count / instance.user_count)

    avg_count.short_description = "Avg Count"
    avg_count.allow_tags = True
    avg_count.is_column = True

    list_display = ("date", "user_count", "view_count", "avg_count")
    list_display_links = ("date",)

    list_filter = ["date", "user_count", "view_count"]
    actions = None
    aggregate_fields = {"user_count": "sum", "view_count": "sum"}

    refresh_times = (3, 5, 10)
    data_charts = {
        "user_count": {'title': u"User Report", "x-field": "date", "y-field": ("user_count", "view_count"),
                       "order": ('date',)},
        "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)},
        "per_month": {'title': u"Monthly Users", "x-field": "_chart_month", "y-field": ("user_count",),
                      "option": {
                          "series": {"bars": {"align": "center", "barWidth": 0.8, 'show': True}},
                          "xaxis": {"aggregate": "sum", "mode": "categories"},
                      },
                      },
    }

    def _chart_month(self, obj):
        return obj.date.strftime("%B")


'''
# xadmin.sites.site.register(Series, SeriesAdmin)
# xadmin.sites.site.register(Sutra, SutraAdmin)
# xadmin.sites.site.register(Translator, TranslatorAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
'''
