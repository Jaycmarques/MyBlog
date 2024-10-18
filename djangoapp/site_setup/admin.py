from django.contrib import admin
from django.http import HttpRequest
from site_setup.models import MenuLink, SiteSetup
from adminsortable2.admin import SortableAdminBase, SortableTabularInline


# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path',
#     list_display_links = 'id', 'text', 'url_or_path',
#     search_fields = 'id', 'text', 'url_or_path',


class MenuLinkInline(SortableTabularInline):
    model = MenuLink
    extra = 1
    fields = ['text', 'url_or_path', 'new_tab', 'order']


@admin.register(SiteSetup)
# Aqui, herde de SortableAdminBase
class SiteSetupAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [MenuLinkInline]
    # Ajuste para exibir os campos desejados
    list_display = ('title', 'description')


def has_add_permission(self, request: HttpRequest) -> bool:
    return not SiteSetup.objects.exists()
