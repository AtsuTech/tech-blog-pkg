from django.db import models

# Create your models here.
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,

    # import PublishingPanel:
    PublishingPanel,
)

# import RichTextField:
from wagtail.fields import RichTextField

# import DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin:
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

# import register_snippet:
from wagtail.snippets.models import register_snippet



# ブログタイトルのテキスト
@register_snippet
class BlogTitleText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    title_text =  models.TextField(
        max_length=300,
        blank=True,
        help_text="記事一覧で表示する概要"
    )


    panels = [
        FieldPanel("title_text"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Blog title text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"blog_title_text": self.title_text}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "ブログタイトルのテキスト"


# フッターテキスト
@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "フッターのテキスト"