from pages.utils import BlockType, register_block_type
from django import forms
from django.template.loader import render_to_string


@register_block_type
class SouthamptonGameJamBlockType(BlockType):
    title = forms.CharField()

    def render(self, request, data):
        if request.user.is_anonymous:
            return ""
        return super(SouthamptonGameJamBlockType, self).render(request, data)

    def render_content(self, request, data):
        return render_to_string("southampton_game_jam_2017/page_blocks/block.html",
                                request=request)
