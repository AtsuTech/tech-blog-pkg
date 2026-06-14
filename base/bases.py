from wagtail import blocks
from wagtail.blocks import StructBlock
from wagtail.blocks import CharBlock, ChoiceBlock

class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("h1", "H1"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("h5", "H5"),
            ("h6", "H6"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "base/blocks/heading_block.html"



# コードブロック
class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("typescript", "TypeScript"),
            ("java", "Java"),
            ("php", "PHP"),
            ("bash", "Bash"),
            ("sql", "SQL"),
            ("html", "HTML"),
            ("css", "CSS"),
            ("json", "JSON"),
        ]
    )

    code = blocks.TextBlock()

    class Meta:
        icon = "code"
        label = "Code"
        template = "base/blocks/code_block.html"
