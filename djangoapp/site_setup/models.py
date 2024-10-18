from django.db import models
from utils.model_validators import validade_png
from utils.images import resize_image


class MenuLink(models.Model):
    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=True)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True,
        default=None,
    )
    order = models.PositiveIntegerField(
        default=0, verbose_name="Order"
    )  # Novo campo de ordenação

    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'
        # Adicione esta linha para definir a ordenação padrão
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.order:
            # Atribui um novo valor de 'order' se não estiver definido
            max_order = MenuLink.objects.filter(site_setup=self.site_setup).aggregate(
                max_order=models.Max('order'))['max_order']
            self.order = (max_order or 0) + 1
        super(MenuLink, self).save(*args, **kwargs)

    def __str__(self):
        return self.text


class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/', blank=True, default='',
        validators=[validade_png],

    )

    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        if favicon_changed:
            resize_image(self.favicon, 32)

    def __str__(self):
        return self.title
