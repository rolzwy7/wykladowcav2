def create_link(text: str, href: str, color: str = "primary"):
    """Create link for eventlog"""
    return f'<a href="{href}" class="text-{color} fw-bold me-1">{text}</a>'
