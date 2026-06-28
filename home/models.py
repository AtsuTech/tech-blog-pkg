from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from blog.models import BlogIndexPage
from blog.models import BlogPage #ブログのモデル
from users.models import User #ユーザーのモデル

class HomePage(Page):

    # ホームページは1つしか作成できないようにする
    max_count = 1

    hero_title = models.CharField(
        max_length=100,
        default="My Tech Blog"
    )

    hero_subtitle = models.TextField(
        blank=True,
        default="Web開発・個人開発・技術学習について発信します"
    )

    #画像
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    intro = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("intro"),
    ]

    subpage_types = ["blog.BlogIndexPage"]

    class Meta:
        verbose_name = "Home Page"

    # 最新の記事を10件取得
    def get_context(self, request):
        context = super().get_context(request)

        context["latest_posts"] = (
            BlogPage.objects.live()
            .public()
            .order_by("-first_published_at")[:10]
        )
        context["profile_user"] = User.objects.first()

        return context