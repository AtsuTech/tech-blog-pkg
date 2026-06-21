from django.db import models

# Create your models here.
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtailmarkdown.blocks import MarkdownBlock #wagtail-markdown
from base.bases import CodeBlock,HeadingBlock #自作の見出しブロック



# ----------------------------
# Category
# ----------------------------
@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # panels = [
    #     FieldPanel("name"),
    #     FieldPanel("slug"),
    # ]

    def __str__(self):
        return self.name



# ----------------------------
# Blog Tag を検索表示
# ----------------------------
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


# ----------------------------
# Alert Block
# ----------------------------
class AlertBlock(blocks.StructBlock):
    level = blocks.ChoiceBlock(
        choices=[
            ("info", "Info"),
            ("warning", "Warning"),
            ("danger", "Danger"),
            ("success", "Success"),
        ]
    )

    content = blocks.RichTextBlock()

    class Meta:
        icon = "warning"
        label = "Alert"


# ----------------------------
# Blog Index Page
# ----------------------------
class BlogIndexPage(Page):
    """
    ブログ一覧ページ
    """

    subpage_types = ["blog.BlogPage"]
    max_count = 1

    # -----タグに紐づくブログ記事を検索-------
    def get_context(self,request):
        context = super().get_context(request)

        #
        blog_entries = BlogPage.objects.child_of(self).live()

        tag = request.GET.get('tag')
        

        if tag:
            blog_entries = blog_entries.filter(tags__name=tag)
            print("tag:", tag)
            print("after filter:", blog_entries.count())  # ← これを追加

        context['blog_entries'] = blog_entries
        return context

    class Meta:
        verbose_name = "Blog Index"




# ----------------------------
# Blog Page
# ----------------------------

class BlogPage(Page):

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]


    summary = models.TextField(
        max_length=300,
        blank=True,
        help_text="記事一覧で表示する概要"
    )

    eyecatch = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="posts"
    )


    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="beginner"
    )

    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True
    )

    content = StreamField(
        [
            #("heading", blocks.CharBlock()),
            ("heading", HeadingBlock()),
            ("rich_text", blocks.RichTextBlock()),
            ('markdown', MarkdownBlock()), # MarkdownFieldを追加
            ("code", CodeBlock()),
            ("image", ImageChooserBlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ("alert", AlertBlock()),
            ("embed", blocks.URLBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    # SEO

    # seo_title = models.CharField(
    #     max_length=255,
    #     blank=True
    # )

    # meta_description = models.CharField(
    #     max_length=160,
    #     blank=True
    # )

    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


    # Analytics
    view_count = models.PositiveIntegerField(
        default=0
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("eyecatch"),

        MultiFieldPanel(
            [
                FieldPanel("category"),
                #FieldPanel("series"),
                FieldPanel("difficulty"),
                FieldPanel("tags"),
            ],
            heading="Classification",
        ),

        FieldPanel("content"),

        MultiFieldPanel(
            [
                #FieldPanel("published_at"),
            ],
            heading="Publishing",
        ),

        MultiFieldPanel(
            [
                #FieldPanel("seo_title"),
                #FieldPanel("meta_description"),
                FieldPanel("og_image"),
            ],
            heading="SEO",
        ),
    ]

    parent_page_types = ["blog.BlogIndexPage"]

    class Meta:
        verbose_name = "Blog Post"

    def __str__(self):
        return self.title