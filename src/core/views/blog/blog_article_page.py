from django.template.response import TemplateResponse


def blog_article_page(request, slug: str):
    """blog_article_page"""
    template_name = "geeks/pages/blog/BlogArticle.html"
    return TemplateResponse(request, template_name, {"slug": slug})
