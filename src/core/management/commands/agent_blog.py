"""Agent Blog"""

# core/management/commands/agent_blog.py
# flake8: noqa=E501
# pylint: disable=line-too-long

import os

from django.core.management.base import BaseCommand, CommandError

from core.models import BlogPost


class Command(BaseCommand):
    """
    Komenda Django do modyfikacji pól w modelu BlogPost przez agenta AI.

    Przykłady użycia:
    1. Zmiana wartości pola 'meta_title' dla wpisu o ID 1:
       python manage.py agent_blog --id 1 --field "meta_title" --value "Nowy meta tytuł"

    2. Zmiana treści ('content') dla wpisu o ID 1 z pliku:
       python manage.py agent_blog --id 1 --field "content" --file_path "/sciezka/do/pliku/tresc.md"

    3. Zmiana statusu publikacji:
       python manage.py agent_blog --id 1 --field "status" --value "published"
    """

    help = "Modyfikuje wybrane pole w instancji modelu BlogPost."

    def add_arguments(self, parser):
        """Dodaje argumenty do komendy."""
        parser.add_argument(
            "--id",
            type=int,
            required=True,
            help="ID obiektu BlogPost do zaktualizowania.",
        )
        parser.add_argument(
            "--field",
            type=str,
            required=True,
            help="Nazwa pola w modelu BlogPost do zaktualizowania.",
        )
        parser.add_argument(
            "--value",
            type=str,
            help="Nowa wartość dla podanego pola. Nie jest wymagane, jeśli używasz --file_path.",
        )
        parser.add_argument(
            "--file_path",
            type=str,
            help='Ścieżka do pliku, którego zawartość zostanie wczytana jako wartość. Używane głównie dla pola "content".',
        )

    def handle(self, *args, **options):
        """Główna logika komendy."""
        blog_post_id = options["id"]
        field_name = options["field"]
        value = options["value"]
        file_path = options["file_path"]

        # Sprawdzenie, czy podano wartość lub ścieżkę do pliku
        if value is None and file_path is None:
            raise CommandError("Musisz podać argument --value lub --file_path.")

        # Pobranie obiektu z bazy danych
        try:
            post = BlogPost.manager.get(pk=blog_post_id)
        except BlogPost.DoesNotExist:
            raise CommandError(f'BlogPost o ID "{blog_post_id}" nie istnieje.')

        # Sprawdzenie, czy podane pole istnieje w modelu
        if not hasattr(post, field_name):
            raise CommandError(
                f'Pole o nazwie "{field_name}" nie istnieje w modelu BlogPost.'
            )

        # Wczytanie wartości z pliku, jeśli podano ścieżkę
        final_value = value
        if file_path:
            if not os.path.exists(file_path):
                raise CommandError(f'Plik pod ścieżką "{file_path}" nie istnieje.')
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    final_value = f.read()
            except Exception as e:
                raise CommandError(f'Nie udało się odczytać pliku "{file_path}": {e}')

        # Ustawienie nowej wartości dla pola
        try:
            # Specjalna obsługa dla pól typu BooleanField
            field_object = post._meta.get_field(field_name)
            if field_object.get_internal_type() == "BooleanField":
                if str(final_value).lower() in ["true", "1", "yes"]:
                    final_value = True
                else:
                    final_value = False

            setattr(post, field_name, final_value)
            # Uruchamia pełną walidację modelu przed zapisem
            post.full_clean()
            post.save(update_fields=[field_name])
        except Exception as e:
            raise CommandError(
                f'Wystąpił błąd podczas aktualizacji pola "{field_name}": {e}'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Pomyślnie zaktualizowano pole "{field_name}" dla BlogPost o ID {blog_post_id}.'
            )
        )
