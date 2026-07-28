"""Seed the site with the owner's real content.

Idempotent: every entry is matched by a natural key and updated in place, so the
command can be re-run after editing the data below. Translated fields are written with
explicit `_ru` / `_en` suffixes — passing the bare name would only fill the language
that happens to be active.

    make dev bash
    python manage.py seed_portfolio
"""

from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import Course, Education, Experience, Profile, ProjectCategory, Skill, SkillGroup, SocialLink

PROFILE = {
    "full_name": "Игорь Хайлов",
    "headline_ru": "Python-разработчик, Backend-разработчик, Web-разработчик",
    "headline_en": "Python Developer, Backend Developer, Web Developer",
    "role_ru": "Backend-разработчик · Python / Django",
    "role_en": "Backend Developer · Python / Django",
    "summary_ru": (
        "Путь в IT начал с HTML, CSS и Python: консольные утилиты, скрипты автоматизации, "
        "десктопные приложения на wxPython. Сейчас разрабатываю backend веб-приложений на Django."
    ),
    "summary_en": (
        "Started with HTML, CSS and Python: console utilities, automation scripts and wxPython "
        "desktop apps. Today I build web application backends with Django."
    ),
    "bio_ru": (
        "Программирую с 2019 года. Работал с авторизацией пользователей, отправкой почты, "
        "Ajax и Mapbox API. Сейчас — Django и DRF, PostgreSQL, Celery, Docker и деплой на Linux-серверах. "
        "Постоянно изучаю новые технологии и применяю их на практике."
    ),
    "bio_en": (
        "Coding since 2019. Worked with user authentication, transactional email, Ajax and the "
        "Mapbox API. These days: Django and DRF, PostgreSQL, Celery, Docker and deployments on "
        "Linux servers. Constantly learning and shipping new technologies."
    ),
    "location_ru": "Самарканд, Узбекистан",
    "location_en": "Samarkand, Uzbekistan",
    "email": "info@itnova.uz",
    "phone": "+998 33 345-41-15",
    "birth_date": date(1999, 1, 29),
    "career_started_at": 2019,
    "is_available_for_hire": True,
    "meta_description_ru": "Игорь Хайлов — backend-разработчик на Python и Django. Самарканд, Узбекистан.",
    "meta_description_en": "Igor Khaylov — backend developer, Python and Django. Samarkand, Uzbekistan.",
    "meta_keywords_ru": "Python, Django, backend, разработчик, Самарканд, Узбекистан",
    "meta_keywords_en": "Python, Django, backend developer, Samarkand, Uzbekistan",
    "is_active": True,
}


def _social(rank: int, url: str, icon: str, title: str) -> dict:
    return {"rank": rank, "url": url, "icon": icon, "title_ru": title, "title_en": title}


SOCIAL_LINKS = [
    _social(10, "https://t.me/igorkhaylov", "bxl-telegram", "Telegram"),
    _social(20, "https://github.com/igorkhaylov", "bxl-github", "GitHub"),
    _social(30, "https://www.facebook.com/igorkhaylov", "bxl-facebook", "Facebook"),
    _social(40, "https://www.instagram.com/igorkhaylov", "bxl-instagram", "Instagram"),
]

EXPERIENCE = [
    {
        "rank": 10,
        "position_ru": "Backend-разработчик, фриланс",
        "position_en": "Backend Developer, freelance",
        "company_ru": "Фриланс",
        "company_en": "Freelance",
        "started_at": date(2020, 1, 1),
        "is_current": True,
        "highlights_ru": (
            "Backend-разработка сайтов и веб-приложений на Django\n"
            "Доработка и поддержка существующих проектов\n"
            "Веб-приложения для бизнеса под ключ\n"
            "Преподавал программирование на Python в IT-школе"
        ),
        "highlights_en": (
            "Backend development of websites and web applications with Django\n"
            "Maintenance and feature work on existing projects\n"
            "Turnkey web applications for business\n"
            "Taught Python programming at an IT school"
        ),
    },
    {
        "rank": 20,
        "position_ru": "Программист, специалист технической поддержки",
        "position_en": "Programmer, IT support specialist",
        "company_ru": "ООО «Sam Antep Gilam»",
        "company_en": "Sam Antep Gilam LLC",
        "location_ru": "Самарканд",
        "location_en": "Samarkand",
        "started_at": date(2018, 1, 1),
        "is_current": True,
        "highlights_ru": (
            "Написание Python-скриптов для автоматизации работы\n"
            "Техподдержка и обслуживание компьютерной техники\n"
            "Установка и настройка программного обеспечения\n"
            "Настройка сети и устранение неисправностей\n"
            "Установка и настройка камер видеонаблюдения\n"
            "Подключение сертификатов для работы с банк-клиентом"
        ),
        "highlights_en": (
            "Python automation scripts for daily operations\n"
            "Hardware support and maintenance\n"
            "Software installation and configuration\n"
            "Network setup and troubleshooting\n"
            "CCTV installation and configuration\n"
            "Certificate setup for the bank-client software"
        ),
    },
    {
        "rank": 30,
        "position_ru": "Оператор ЭВМ",
        "position_en": "Computer operator",
        "company_ru": "Топливный железнодорожный склад",
        "company_en": "Railway fuel depot",
        "location_ru": "Самарканд",
        "location_en": "Samarkand",
        "started_at": date(2018, 1, 1),
        "finished_at": date(2018, 12, 31),
        "highlights_ru": (
            "Техподдержка и обслуживание компьютерной техники\nУстановка и настройка программного обеспечения"
        ),
        "highlights_en": "Hardware support and maintenance\nSoftware installation and configuration",
    },
    {
        "rank": 40,
        "position_ru": "Стажировка",
        "position_en": "Internship",
        "company_ru": "Самаркандская городская электросеть",
        "company_en": "Samarkand City Power Grid",
        "started_at": date(2013, 1, 1),
        "finished_at": date(2017, 12, 31),
        "description_ru": "Летняя стажировка",
        "description_en": "Summer internship",
        "highlights_ru": (
            "Перенос должностных инструкций в электронный формат\nОцифровка схем\nРешение мелких проблем с компьютерами"
        ),
        "highlights_en": (
            "Digitised job descriptions\nDigitised electrical schematics\nDay-to-day computer troubleshooting"
        ),
    },
]

EDUCATION = [
    {
        "rank": 10,
        "institution_ru": "Самаркандский профессиональный колледж железнодорожного транспорта",
        "institution_en": "Samarkand Professional College of Railway Transport",
        "degree_ru": "Среднее профессиональное образование",
        "degree_en": "Vocational secondary education",
        "speciality_ru": "Эксплуатация железных дорог — дежурный по станции",
        "speciality_en": "Railway operations — station duty officer",
        "started_at": date(2015, 9, 1),
        "finished_at": date(2018, 6, 30),
    },
    {
        "rank": 20,
        "institution_ru": "Учебный центр «Samarqand Bilim Orzu»",
        "institution_en": "Samarqand Bilim Orzu training centre",
        "degree_ru": "Компьютерные курсы",
        "degree_en": "Computer courses",
        "started_at": date(2014, 1, 1),
        "finished_at": date(2014, 12, 31),
        "description_ru": "Офисные программы и работа в интернете, окончил на отлично",
        "description_en": "Office software and internet basics, graduated with distinction",
    },
]

COURSES = [
    {
        "rank": 10,
        "title_ru": "HTML5, CSS и JavaScript",
        "title_en": "HTML5, CSS and JavaScript",
        "provider_ru": "Самообразование, открытые курсы",
        "provider_en": "Self-education, open courses",
        "started_at": date(2018, 1, 1),
        "finished_at": date(2019, 12, 31),
        "highlights_ru": "Вёрстка и семантика HTML\nОсновы CSS и адаптивность\nРабота с медиафайлами",
        "highlights_en": "HTML markup and semantics\nCSS fundamentals and responsive layout\nWorking with media files",
    },
    {
        "rank": 20,
        "title_ru": "Программирование на Python",
        "title_en": "Python programming",
        "provider_ru": "Foxford и открытые курсы",
        "provider_en": "Foxford and open courses",
        "started_at": date(2019, 1, 1),
        "finished_at": date(2020, 12, 31),
        "highlights_ru": "Python и стандартная библиотека\nООП на практике\nРабота с базами данных и SQL",
        "highlights_en": "Python and the standard library\nOOP in practice\nDatabases and SQL",
    },
    {
        "rank": 30,
        "title_ru": "Администрирование Linux",
        "title_en": "Linux administration",
        "provider_ru": "Самообразование",
        "provider_en": "Self-education",
        "started_at": date(2019, 1, 1),
        "finished_at": date(2020, 12, 31),
        "highlights_ru": "Архитектура Linux\nФайловые системы\nУправление пользователями и правами",
        "highlights_en": "Linux architecture\nFile systems\nUser and permission management",
    },
]

SKILL_GROUPS = [
    {
        "rank": 10,
        "title_ru": "Backend",
        "title_en": "Backend",
        "skills": [
            ("Python", 90, "bxl-python", True),
            ("Django", 90, "bxl-django", True),
            ("Django REST Framework", 85, "", True),
            ("Celery", 75, "", False),
            ("PostgreSQL", 80, "bxl-postgresql", True),
            ("Redis", 70, "bxl-redis", False),
        ],
    },
    {
        "rank": 20,
        "title_ru": "Инфраструктура",
        "title_en": "Infrastructure",
        "skills": [
            ("Docker", 80, "bxl-docker", True),
            ("Linux", 85, "bxl-tux", True),
            ("Nginx", 70, "", False),
            ("Git / CI-CD", 80, "bxl-git", True),
            ("MinIO / S3", 70, "", False),
        ],
    },
    {
        "rank": 30,
        "title_ru": "Frontend",
        "title_en": "Frontend",
        "skills": [
            ("HTML / CSS", 75, "bxl-html5", False),
            ("JavaScript", 65, "bxl-javascript", False),
            ("TypeScript", 55, "bxl-typescript", False),
            ("React", 55, "bxl-react", False),
        ],
    },
]

PROJECT_CATEGORIES = [
    {"rank": 10, "slug": "web", "title_ru": "Веб-сайты", "title_en": "Websites"},
    {"rank": 20, "slug": "webapp", "title_ru": "Веб-приложения", "title_en": "Web applications"},
    {"rank": 30, "slug": "tools", "title_ru": "Инструменты", "title_en": "Tools"},
]


class Command(BaseCommand):
    help = "Populate the site with the owner's profile, resume, skills and project categories."

    @transaction.atomic
    def handle(self, *args, **options):
        profile, _created = Profile.objects.update_or_create(
            full_name=PROFILE["full_name"],
            defaults={k: v for k, v in PROFILE.items() if k != "full_name"},
        )
        self.stdout.write(self.style.SUCCESS(f"Profile: {profile}"))

        for data in SOCIAL_LINKS:
            SocialLink.objects.update_or_create(profile=profile, url=data["url"], defaults=data)
        self.stdout.write(f"Social links: {len(SOCIAL_LINKS)}")

        for data in EXPERIENCE:
            Experience.objects.update_or_create(position_ru=data["position_ru"], defaults=data)
        self.stdout.write(f"Experience: {len(EXPERIENCE)}")

        for data in EDUCATION:
            Education.objects.update_or_create(institution_ru=data["institution_ru"], defaults=data)
        self.stdout.write(f"Education: {len(EDUCATION)}")

        for data in COURSES:
            Course.objects.update_or_create(title_ru=data["title_ru"], defaults=data)
        self.stdout.write(f"Courses: {len(COURSES)}")

        skills_total = 0
        for group_data in SKILL_GROUPS:
            # Never mutate the module-level constant: the command must survive a re-run
            # inside the same process (tests, shell).
            defaults = {k: v for k, v in group_data.items() if k != "skills"}
            group, _ = SkillGroup.objects.update_or_create(title_ru=defaults["title_ru"], defaults=defaults)
            for index, (name, level, icon, is_featured) in enumerate(group_data["skills"], start=1):
                Skill.objects.update_or_create(
                    name_ru=name,
                    defaults={
                        "name_en": name,
                        "group": group,
                        "level": level,
                        "icon": icon,
                        "is_featured": is_featured,
                        "rank": index * 10,
                    },
                )
                skills_total += 1
        self.stdout.write(f"Skills: {skills_total} in {len(SKILL_GROUPS)} groups")

        for data in PROJECT_CATEGORIES:
            ProjectCategory.objects.update_or_create(slug=data["slug"], defaults=data)
        self.stdout.write(f"Project categories: {len(PROJECT_CATEGORIES)}")

        self.stdout.write(self.style.SUCCESS("Done. Projects are added through the admin."))
