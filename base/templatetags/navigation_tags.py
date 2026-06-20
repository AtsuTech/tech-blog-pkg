from django import template

from base.models import BlogTitleText,FooterText

register = template.Library()



@register.inclusion_tag("base/includes/blog_title_text.html", takes_context=True)
def get_blog_title_text(context):
    blog_title_text = context.get("blog_title_text", "")

    if not blog_title_text:
        instance = BlogTitleText.objects.filter(live=True).first()
        blog_title_text = instance.title_text if instance else "My Blog"

    return {
        "blog_title_text": blog_title_text,
    }

@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }