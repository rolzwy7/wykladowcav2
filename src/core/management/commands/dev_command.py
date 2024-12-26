"""dev_command"""

# flake8: noqa=E501
from django.core.management.base import BaseCommand

from core.libs.html_operations.program import program_normalize, program_remarkdownify


class Command(BaseCommand):
    """dev_command"""

    help = "dev_command"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        ret = program_remarkdownify(
            """
<ul class="my-list" style="color: black;">
    <li class="item" style="color: red;">12345</li>
    <li class="item" style="color: red;">
    inner
        <ol>
            <li>1</li>
            <li>2</li>
            <li>3</li>
        </ol>
    </li>
    <li class="item">123</li>
    <li class="item" style="color: red;">
        <ol>
            <li>1</li>
            <li>2</li>
            <li>inner
                <ul>
                    <li>aa</li>
                    <li>dsa</li>
                    <li>fds</li>
                    <li>sad</li>
                </ul>
            </li>
        </ol>
    </li>
    <li class="item" style="color: red;">1</li>
</ul>
            """
        )

        print(ret)
        print("=" * 32)
        print(program_normalize(ret))
