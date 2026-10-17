"""Seed the site with the owner's real content.

Idempotent: every entry is matched by a natural key and updated in place, so the
command can be re-run after editing the data below. Translated fields are written with
explicit `_ru` / `_en` suffixes — passing the bare name would only fill the language
that happens to be active.

    make dev seed            # or: make prod seed on the server

Numbers below (commits, servers, terabytes) were collected in October 2026 from the
git history, GitHub and a read-only survey of the servers. Refresh them here, not in
the admin, so they survive a database reset.
"""

from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import (
    Course,
    Education,
    Experience,
    FocusArea,
    Profile,
    Project,
    ProjectCategory,
    Skill,
    SkillGroup,
    SocialLink,
    Stat,
)


def lines(*items: str) -> str:
    """Highlights are stored one bullet per line."""
    return "\n".join(items)


# =============================================================================
# Profile
# =============================================================================

PROFILE = {
    "full_name_ru": "Игорь Хайлов",
    "full_name_en": "Igor Khaylov",
    "headline_ru": "Python · Django, Платформа и DevOps, Видео и стриминг, GPU и LLM",
    "headline_en": "Python · Django, Platform & DevOps, Video streaming, GPUs & LLMs",
    "role_ru": "Backend-разработчик и инженер инфраструктуры",
    "role_en": "Backend developer & platform engineer",
    "summary_ru": (
        "Пишу backend на Python и Django и сам держу продакшен, на котором он работает: "
        "биллинг и видео онлайн-кинотеатра, образовательные платформы, музейные системы — "
        "и парк из ~100 серверов с Proxmox, S3, мониторингом и GPU-узлами для LLM."
    ),
    "summary_en": (
        "I write Python and Django backends and run the production they live on: the billing "
        "and video of a streaming service, e-learning platforms, museum systems — and a fleet "
        "of ~100 servers with Proxmox, S3, monitoring and GPU nodes for LLMs."
    ),
    "bio_ru": (
        "Я backend-разработчик на Python и Django и одновременно инженер, который отвечает за "
        "продакшен целиком. Программирую с 2019 года, с 2022-го работаю в Intersoft tech: начинал "
        "с backend онлайн-кинотеатра SPlay, а сегодня отвечаю за серверную часть ключевых "
        "продуктов компании и за всю её инфраструктуру — от железа и гипервизоров до CI/CD, "
        "мониторинга и GPU-серверов для языковых моделей.\n\n"
        "Мне важно, чтобы система работала без меня: понятная архитектура, тесты, деплой одной "
        "командой и откат по тегу, мониторинг с алертами, записанные runbook-и и разборы "
        "инцидентов. Для этого я написал собственный django-template — сейчас на нём строятся "
        "все новые backend-проекты компании.\n\n"
        "Родом из Самарканда, живу в Ташкенте. Русский — родной, английский — средний."
    ),
    "bio_en": (
        "I am a Python and Django backend developer and, at the same time, the engineer who owns "
        "production end to end. I have been coding since 2019 and working at Intersoft tech since "
        "2022: I started on the backend of the SPlay streaming service, and today I own the "
        "server side of the company's key products and all of its infrastructure — from "
        "hardware and hypervisors to CI/CD, monitoring and GPU servers for language models.\n\n"
        "I care about systems that run without me: a clear architecture, tests, one-command "
        "deploys with rollback by tag, monitoring with alerts, written runbooks and incident "
        "post-mortems. That is why I wrote my own django-template — every new backend project "
        "of the company is now built on it.\n\n"
        "Born in Samarkand, living in Tashkent. Russian is my native language, English intermediate."
    ),
    "now_ru": lines(
        "Запускаю билетную систему Центра исламской цивилизации: сайт, киоски, касса, турникеты и AI-ассистент",
        "Развиваю платформу мониторинга на ~85 серверов и ~190 сервисов",
        "Сопровождаю GPU-серверы с LLM: 8× NVIDIA B200 и 8× RTX PRO 6000",
        "Переписываю backend Ilmi и SPlay на своём django-template",
        "Проектирую отказоустойчивую платформу на две площадки: Kubernetes, Patroni, репликация S3",
    ),
    "now_en": lines(
        "Launching the ticketing system of the Centre of Islamic Civilization: website, kiosks, cashier, "
        "turnstiles and an AI assistant",
        "Growing the monitoring platform that covers ~85 servers and ~190 services",
        "Running the GPU servers with LLMs: 8× NVIDIA B200 and 8× RTX PRO 6000",
        "Rewriting the Ilmi and SPlay backends on my django-template",
        "Designing a fault-tolerant two-site platform: Kubernetes, Patroni, S3 replication",
    ),
    "location_ru": "Ташкент, Узбекистан",
    "location_en": "Tashkent, Uzbekistan",
    "email": "igorkhaylov@yandex.com",
    "phone": "+998 33 345-41-15",
    "birth_date": None,
    "career_started_at": 2019,
    "is_available_for_hire": True,
    "meta_description_ru": (
        "Игорь Хайлов — backend-разработчик на Python и Django и инженер инфраструктуры: "
        "Proxmox, S3, CI/CD, мониторинг, видеостриминг и GPU для LLM. Ташкент, Узбекистан."
    ),
    "meta_description_en": (
        "Igor Khaylov — Python and Django backend developer and platform engineer: Proxmox, S3, "
        "CI/CD, monitoring, video streaming and GPUs for LLMs. Tashkent, Uzbekistan."
    ),
    "meta_keywords_ru": "Python, Django, backend, DevOps, Proxmox, инфраструктура, стриминг, Ташкент, Узбекистан",
    "meta_keywords_en": "Python, Django, backend developer, DevOps, Proxmox, infrastructure, streaming, Tashkent",
    "is_active": True,
}


def _social(rank: int, url: str, icon: str, title: str) -> dict:
    return {"rank": rank, "url": url, "icon": icon, "title_ru": title, "title_en": title}


# Email and phone come from the Profile fields; these are the links with an icon.
SOCIAL_LINKS = [
    _social(10, "https://t.me/igorkhaylov", "telegram", "Telegram"),
    _social(20, "https://github.com/igorkhaylov", "github", "GitHub"),
]

# =============================================================================
# Headline numbers
# =============================================================================

HERO = Stat.Section.HERO
INFRA = Stat.Section.INFRASTRUCTURE

STATS = [
    # section, rank, value_ru, value_en, label_ru, label_en, note_ru, note_en
    (
        HERO,
        10,
        "5 000+",
        "5,000+",
        "коммитов",
        "commits",
        "в 180+ репозиториях с 2020 года",
        "in 180+ repositories since 2020",
    ),
    (
        HERO,
        20,
        "~100",
        "~100",
        "серверов в зоне ответственности",
        "servers I am responsible for",
        "5 площадок, 10 гипервизоров Proxmox",
        "5 sites, 10 Proxmox hypervisors",
    ),
    (
        HERO,
        30,
        "290 ТБ",
        "290 TB",
        "видео в HLS",
        "of HLS video",
        "видеотека онлайн-кинотеатра SPlay",
        "the SPlay streaming library",
    ),
    (
        HERO,
        40,
        "20+",
        "20+",
        "проектов в продакшене",
        "projects in production",
        "стриминг, медиа, образование, музеи",
        "streaming, media, education, museums",
    ),
    (
        INFRA,
        10,
        "10",
        "10",
        "гипервизоров Proxmox VE",
        "Proxmox VE hypervisors",
        "на четырёх площадках",
        "across four sites",
    ),
    (INFRA, 20, "808", "808", "потоков CPU", "CPU threads", "суммарно на узлах Proxmox", "across the Proxmox nodes"),
    (INFRA, 30, "1,7 ТБ", "1.7 TB", "оперативной памяти", "of RAM", "на гипервизорах", "on the hypervisors"),
    (
        INFRA,
        40,
        "1,4 ПБ",
        "1.4 PB",
        "дискового пространства",
        "of storage",
        "NVMe и RAID под виртуальные машины",
        "NVMe and RAID for VMs",
    ),
    (
        INFRA,
        50,
        "166",
        "166",
        "виртуальных машин",
        "virtual machines",
        "KVM, общий шаблон cloud-init",
        "KVM, a shared cloud-init template",
    ),
    (INFRA, 60, "~870", "~870", "Docker-контейнеров", "Docker containers", "на 83 серверах", "on 83 servers"),
    (
        INFRA,
        70,
        "~400",
        "~400",
        "доменов",
        "domains",
        "за edge-прокси nginx с Let's Encrypt",
        "behind nginx edge proxies with Let's Encrypt",
    ),
    (
        INFRA,
        80,
        "16",
        "16",
        "GPU для AI",
        "GPUs for AI",
        "8× NVIDIA B200 и 8× RTX PRO 6000",
        "8× NVIDIA B200 and 8× RTX PRO 6000",
    ),
    (
        INFRA,
        90,
        "85",
        "85",
        "серверов в мониторинге",
        "servers in monitoring",
        "метрики, логи, алерты",
        "metrics, logs, alerts",
    ),
    (
        INFRA,
        100,
        "75",
        "75",
        "self-hosted CI-раннеров",
        "self-hosted CI runners",
        "GitHub Actions на 27 серверах",
        "GitHub Actions on 27 servers",
    ),
]

# =============================================================================
# Focus areas: "What I do" (about) and the infrastructure cards
# =============================================================================

ABOUT = FocusArea.Section.ABOUT
INFRA_AREA = FocusArea.Section.INFRASTRUCTURE

FOCUS_AREAS = [
    {
        "section": ABOUT,
        "rank": 10,
        "icon": "code",
        "title_ru": "Backend на Django",
        "title_en": "Django backends",
        "summary_ru": "API для веба и мобильных приложений, биллинг и платежи, фоновые задачи, многоязычность.",
        "summary_en": "APIs for web and mobile apps, billing and payments, background jobs, multilingual content.",
        "highlights_ru": lines(
            "Платёжные системы Узбекистана: Payme, Click, Atmos, Octo, Paynet, Uzum, Alif",
            "Подписки, балансы и покупки в App Store и Google Play",
            "Тесты на pytest и документация API для каждого клиента",
        ),
        "highlights_en": lines(
            "Uzbek payment systems: Payme, Click, Atmos, Octo, Paynet, Uzum, Alif",
            "Subscriptions, balances, App Store and Google Play purchases",
            "pytest suites and API docs for every client app",
        ),
        "stack_ru": "Python, Django, DRF, Celery, PostgreSQL, Redis",
        "stack_en": "Python, Django, DRF, Celery, PostgreSQL, Redis",
    },
    {
        "section": ABOUT,
        "rank": 20,
        "icon": "server",
        "title_ru": "Инфраструктура",
        "title_en": "Infrastructure",
        "summary_ru": "Железо, гипервизоры, сеть, хранилища и доставка кода — для всех продуктов компании.",
        "summary_en": "Hardware, hypervisors, network, storage and code delivery for every product of the company.",
        "highlights_ru": lines(
            "~100 серверов на пяти площадках",
            "Proxmox, S3, бастионы, edge-прокси",
            "Деплой одной командой и откат по тегу",
        ),
        "highlights_en": lines(
            "~100 servers on five sites",
            "Proxmox, S3, bastions, edge proxies",
            "One-command deploys and rollback by tag",
        ),
        "stack_ru": "Proxmox VE, Docker, nginx, MinIO, Linux",
        "stack_en": "Proxmox VE, Docker, nginx, MinIO, Linux",
    },
    {
        "section": ABOUT,
        "rank": 30,
        "icon": "play",
        "title_ru": "Видео и стриминг",
        "title_en": "Video & streaming",
        "summary_ru": "Видеоконвейер онлайн-кинотеатра и образовательных платформ.",
        "summary_en": "The video pipeline of a streaming service and of e-learning platforms.",
        "highlights_ru": lines(
            "Кодирование на GPU и AES-шифрование HLS",
            "IPTV-origin для телеканалов",
            "~290 ТБ видеотеки с зеркалами",
        ),
        "highlights_en": lines(
            "GPU encoding and AES-encrypted HLS",
            "An IPTV origin for live TV channels",
            "~290 TB video library with mirrors",
        ),
        "stack_ru": "FFmpeg, NVENC, HLS, SRT",
        "stack_en": "FFmpeg, NVENC, HLS, SRT",
    },
    {
        "section": ABOUT,
        "rank": 40,
        "icon": "cpu",
        "title_ru": "AI-инфраструктура",
        "title_en": "AI infrastructure",
        "summary_ru": "GPU-серверы и языковые модели, на которых работают AI-функции продуктов.",
        "summary_en": "GPU servers and language models behind the AI features of our products.",
        "highlights_ru": lines(
            "16 GPU в двух серверах",
            "LLM-шлюз с ключами и бюджетами",
            "AI-ассистенты в продуктах с проверкой вызовов инструментов",
        ),
        "highlights_en": lines(
            "16 GPUs in two servers",
            "An LLM gateway with keys and budgets",
            "AI assistants inside products with validated tool calls",
        ),
        "stack_ru": "SGLang, vLLM, ComfyUI, CUDA",
        "stack_en": "SGLang, vLLM, ComfyUI, CUDA",
    },
    {
        "section": ABOUT,
        "rank": 50,
        "icon": "activity",
        "title_ru": "Наблюдаемость",
        "title_en": "Observability",
        "summary_ru": "Узнаю о проблеме раньше пользователей — и записываю, почему она случилась.",
        "summary_en": "I learn about a problem before the users do — and write down why it happened.",
        "highlights_ru": lines(
            "Мониторинг ~85 серверов и ~190 сервисов",
            "Стандарт /deep-health/ для всех проектов",
            "Runbook-и и разборы инцидентов",
        ),
        "highlights_en": lines(
            "Monitoring of ~85 servers and ~190 services",
            "A /deep-health/ standard for every project",
            "Runbooks and incident post-mortems",
        ),
        "stack_ru": "VictoriaMetrics, Grafana, VictoriaLogs",
        "stack_en": "VictoriaMetrics, Grafana, VictoriaLogs",
    },
    {
        "section": ABOUT,
        "rank": 60,
        "icon": "box",
        "title_ru": "Стандарты и шаблоны",
        "title_en": "Standards & templates",
        "summary_ru": "Шаблоны и правила, по которым команда пишет и выкатывает код.",
        "summary_en": "The templates and rules the team writes and ships code by.",
        "highlights_ru": lines(
            "django-template — основа ~30 проектов компании",
            "Единый стиль кода, коммитов и документации",
            "Аудиты безопасности и QA с помощью AI-агентов",
        ),
        "highlights_en": lines(
            "django-template — the base of ~30 company projects",
            "One style for code, commits and documentation",
            "Security audits and QA with AI agents",
        ),
        "stack_ru": "Ruff, pytest, pre-commit, GitHub Actions",
        "stack_en": "Ruff, pytest, pre-commit, GitHub Actions",
    },
    {
        "section": INFRA_AREA,
        "rank": 10,
        "icon": "layers",
        "title_ru": "Виртуализация",
        "title_en": "Virtualisation",
        "summary_ru": "10 физических гипервизоров Proxmox VE на четырёх площадках: HPE, Dell, Gigabyte, Huawei.",
        "summary_en": "10 physical Proxmox VE hypervisors on four sites: HPE, Dell, Gigabyte, Huawei.",
        "highlights_ru": lines(
            "Ввод узлов, RAID и ZFS, бенчмарки fio на каждом узле",
            "Общий cloud-init-шаблон Ubuntu и проброс GPU в виртуальные машины",
            "Переустановил повреждённый узел удалённо через Redfish и свой PXE-сервер — без выезда в ЦОД",
        ),
        "highlights_en": lines(
            "Node commissioning, RAID and ZFS, fio benchmarks on every node",
            "A shared Ubuntu cloud-init template and GPU passthrough into VMs",
            "Reinstalled a damaged node remotely via Redfish and my own PXE server — no trip to the DC",
        ),
        "stack_ru": "Proxmox VE, KVM, ZFS, mdadm, cloud-init, Redfish",
        "stack_en": "Proxmox VE, KVM, ZFS, mdadm, cloud-init, Redfish",
    },
    {
        "section": INFRA_AREA,
        "rank": 20,
        "icon": "shield",
        "title_ru": "Сеть и доступ",
        "title_en": "Network & access",
        "summary_ru": "Каждая площадка закрыта своим SSH-бастионом, устройства за NAT доступны через обратные туннели.",
        "summary_en": "Every site sits behind its own SSH bastion; devices behind NAT are reached via reverse tunnels.",
        "highlights_ru": lines(
            "Бастионы, fail2ban и межсетевые экраны на хостах",
            "MikroTik и OPNsense на площадках, VPN на WireGuard",
            "Обратные SSH-туннели на systemd с автопереподключением",
            "Раскатка изменений на 66 из 66 серверов идемпотентными скриптами",
        ),
        "highlights_en": lines(
            "Bastions, fail2ban and host firewalls",
            "MikroTik and OPNsense on the sites, WireGuard VPN",
            "Self-healing reverse SSH tunnels on systemd",
            "Rolling changes out to 66 of 66 servers with idempotent scripts",
        ),
        "stack_ru": "OpenSSH, MikroTik, OPNsense, WireGuard, systemd",
        "stack_en": "OpenSSH, MikroTik, OPNsense, WireGuard, systemd",
    },
    {
        "section": INFRA_AREA,
        "rank": 30,
        "icon": "globe",
        "title_ru": "Edge и TLS",
        "title_en": "Edge & TLS",
        "summary_ru": "9 edge-прокси nginx, ~400 доменов, сертификаты Let's Encrypt выпускаются автоматически.",
        "summary_en": "9 nginx edge proxies, ~400 domains, Let's Encrypt certificates issued automatically.",
        "highlights_ru": lines(
            "Единый baseline: JSON-логи, HTTP/2, TLS 1.2/1.3, catch-all, ротация логов",
            "Шаблон vhost и выпуск сертификатов через certbot",
            "Логи edge в VictoriaLogs, HLS-кеширование для видео",
        ),
        "highlights_en": lines(
            "One baseline: JSON logs, HTTP/2, TLS 1.2/1.3, catch-all, log rotation",
            "A vhost template and certbot-issued certificates",
            "Edge logs in VictoriaLogs, HLS caching for video",
        ),
        "stack_ru": "nginx, certbot, Vector",
        "stack_en": "nginx, certbot, Vector",
    },
    {
        "section": INFRA_AREA,
        "rank": 40,
        "icon": "git",
        "title_ru": "CI/CD",
        "title_en": "CI/CD",
        "summary_ru": "Серверы не собирают код: CI собирает образ, сервер только скачивает его и перезапускает сервисы.",
        "summary_en": "Servers never build code: CI builds the image, the server only pulls it and restarts.",
        "highlights_ru": lines(
            "GitHub Actions и GitLab CI: тесты → образ → registry → деплой по SSH",
            "~75 self-hosted раннеров и приватный Docker registry",
            "Откат на предыдущий образ по тегу",
        ),
        "highlights_en": lines(
            "GitHub Actions and GitLab CI: tests → image → registry → SSH deploy",
            "~75 self-hosted runners and a private Docker registry",
            "Rollback to the previous image by tag",
        ),
        "stack_ru": "GitHub Actions, GitLab CI, Docker, GHCR",
        "stack_en": "GitHub Actions, GitLab CI, Docker, GHCR",
    },
    {
        "section": INFRA_AREA,
        "rank": 50,
        "icon": "database",
        "title_ru": "Хранилища и данные",
        "title_en": "Storage & data",
        "summary_ru": "Объектное хранилище MinIO на нескольких площадках и десятки баз данных.",
        "summary_en": "MinIO object storage on several sites and dozens of databases.",
        "highlights_ru": lines(
            "MinIO S3: бакеты, пользователи, квоты и политики — скриптами",
            "PostgreSQL (PostGIS, pgvector, TimescaleDB), ClickHouse, Redis, Elasticsearch",
            "Бэкапы pg_dump в S3 с проверочным восстановлением",
        ),
        "highlights_en": lines(
            "MinIO S3: buckets, users, quotas and policies — scripted",
            "PostgreSQL (PostGIS, pgvector, TimescaleDB), ClickHouse, Redis, Elasticsearch",
            "pg_dump backups to S3 with test restores",
        ),
        "stack_ru": "MinIO, PostgreSQL, ClickHouse, Redis",
        "stack_en": "MinIO, PostgreSQL, ClickHouse, Redis",
    },
    {
        "section": INFRA_AREA,
        "rank": 60,
        "icon": "activity",
        "title_ru": "Мониторинг",
        "title_en": "Monitoring",
        "summary_ru": "Метрики, логи и алерты по всему парку — и собственная статус-страница с паспортами проектов.",
        "summary_en": "Metrics, logs and alerts across the fleet — plus my own status page with project passports.",
        "highlights_ru": lines(
            "VictoriaMetrics с push-агентами и токеном на каждый сервер",
            "Мониторинг железа: IPMI, SMART, RAID, вентиляторы, GPU",
            "Алерты в Telegram, разборы инцидентов с причинами",
        ),
        "highlights_en": lines(
            "VictoriaMetrics with push agents and a token per server",
            "Hardware monitoring: IPMI, SMART, RAID, fans, GPUs",
            "Telegram alerts and post-mortems with root causes",
        ),
        "stack_ru": "VictoriaMetrics, vmalert, Grafana, VictoriaLogs",
        "stack_en": "VictoriaMetrics, vmalert, Grafana, VictoriaLogs",
    },
    {
        "section": INFRA_AREA,
        "rank": 70,
        "icon": "play",
        "title_ru": "Видео и real-time",
        "title_en": "Video & real-time",
        "summary_ru": "Хранение и раздача видео, кодирование на GPU, live-каналы и видеозвонки.",
        "summary_en": "Video storage and delivery, GPU encoding, live channels and video calls.",
        "highlights_ru": lines(
            "~290 ТБ HLS на трёх origin-серверах с зеркалами",
            "Приём каналов по SRT и multicast, MediaMTX",
            "LiveKit с TURN для звонков во внутренних продуктах",
        ),
        "highlights_en": lines(
            "~290 TB of HLS on three origin servers with mirrors",
            "SRT and multicast channel ingest, MediaMTX",
            "LiveKit with TURN for calls in internal products",
        ),
        "stack_ru": "FFmpeg, NVENC, HLS, SRT, LiveKit",
        "stack_en": "FFmpeg, NVENC, HLS, SRT, LiveKit",
    },
    {
        "section": INFRA_AREA,
        "rank": 80,
        "icon": "cpu",
        "title_ru": "GPU и AI",
        "title_en": "GPUs & AI",
        "summary_ru": "Два сервера для языковых моделей, генерации изображений и видео, распознавания и синтеза речи.",
        "summary_en": "Two servers for language models, image and video generation, speech recognition and synthesis.",
        "highlights_ru": lines(
            "8× NVIDIA B200 (HGX) и 8× RTX PRO 6000 Blackwell",
            "SGLang и vLLM за LLM-шлюзом с ключами и бюджетами",
            "ComfyUI, STT и TTS для видеокоманды и продуктов",
        ),
        "highlights_en": lines(
            "8× NVIDIA B200 (HGX) and 8× RTX PRO 6000 Blackwell",
            "SGLang and vLLM behind an LLM gateway with keys and budgets",
            "ComfyUI, STT and TTS for the video team and the products",
        ),
        "stack_ru": "SGLang, vLLM, ComfyUI, CUDA",
        "stack_en": "SGLang, vLLM, ComfyUI, CUDA",
    },
]

# =============================================================================
# Resume
# =============================================================================

EXPERIENCE = [
    {
        "rank": 10,
        "position_ru": "Backend-разработчик и инженер инфраструктуры",
        "position_en": "Backend developer & platform engineer",
        "company_ru": "Intersoft tech",
        "company_en": "Intersoft tech",
        "company_url": "https://intersoft.uz",
        "location_ru": "Ташкент",
        "location_en": "Tashkent",
        "started_at": date(2022, 5, 1),
        "finished_at": None,
        "is_current": True,
        "description_ru": (
            "Продуктовая IT-компания: стриминг, медиа, образование, музейные и корпоративные системы. "
            "Пришёл backend-разработчиком в команду SPlay, со временем стал отвечать за серверную часть "
            "ключевых продуктов и за всю инфраструктуру компании."
        ),
        "description_en": (
            "A product IT company: streaming, media, education, museum and enterprise systems. I joined as "
            "a backend developer on SPlay and grew into owning the server side of the key products and the "
            "whole infrastructure of the company."
        ),
        "highlights_ru": lines(
            "Основной backend-разработчик SPlay, платформ Qizil Pomada и Ilmi, ARK и билетной системы "
            "Центра исламской цивилизации",
            "Отвечаю за весь парк серверов: ~100 хостов на пяти площадках, 10 гипервизоров Proxmox, S3, "
            "сеть и доступ через бастионы",
            "Построил платформу мониторинга и стандарт /deep-health/ для всех проектов",
            "Ввёл в эксплуатацию GPU-серверы для LLM: 8× NVIDIA B200 и 8× RTX PRO 6000",
            "Написал django-template — обязательную основу новых backend-проектов (~30 проектов)",
            "Настроил CI/CD: сборка образов в GitHub Actions и GitLab CI, деплой по SSH, self-hosted раннеры",
            "Пишу runbook-и и разборы инцидентов с причинами",
        ),
        "highlights_en": lines(
            "Main backend developer of SPlay, the Qizil Pomada and Ilmi platforms, ARK and the ticketing "
            "system of the Centre of Islamic Civilization",
            "Own the whole server fleet: ~100 hosts on five sites, 10 Proxmox hypervisors, S3, the network "
            "and bastion-based access",
            "Built the monitoring platform and the /deep-health/ standard for every project",
            "Brought GPU servers for LLMs into production: 8× NVIDIA B200 and 8× RTX PRO 6000",
            "Wrote django-template — the mandatory base of new backend projects (~30 so far)",
            "Set up CI/CD: images built in GitHub Actions and GitLab CI, SSH deploys, self-hosted runners",
            "Write runbooks and incident post-mortems with root causes",
        ),
    },
    {
        "rank": 20,
        "position_ru": "Backend-разработчик, фриланс",
        "position_en": "Backend developer, freelance",
        "company_ru": "Фриланс",
        "company_en": "Freelance",
        "location_ru": "",
        "location_en": "",
        "started_at": date(2020, 1, 1),
        "finished_at": None,
        "is_current": True,
        "description_ru": "",
        "description_en": "",
        "highlights_ru": lines(
            "Сайт Агентства кинематографии Узбекистана: разработка, хостинг и поддержка (2023–2024)",
            "Сайт Ташкентского международного кинофестиваля: редизайн и сопровождение (2024)",
            "Сайт Свято-Алексеевского собора в Самарканде — от дизайна до сервера",
            "Backend мобильного узбекско-итальянского словаря",
            "Преподавал программирование на Python в IT-школе",
        ),
        "highlights_en": lines(
            "Website of the Cinematography Agency of Uzbekistan: development, hosting and support (2023–2024)",
            "Website of the Tashkent International Film Festival: redesign and maintenance (2024)",
            "Website of St. Alexius Cathedral in Samarkand — from design to server",
            "Backend of an Uzbek–Italian dictionary mobile app",
            "Taught Python programming at an IT school",
        ),
    },
    {
        "rank": 30,
        "position_ru": "Программист, специалист технической поддержки",
        "position_en": "Programmer, IT support specialist",
        "company_ru": "ООО «Sam Antep Gilam»",
        "company_en": "Sam Antep Gilam LLC",
        "location_ru": "Самарканд",
        "location_en": "Samarkand",
        "started_at": date(2019, 1, 1),
        "finished_at": date(2022, 4, 30),
        "is_current": False,
        "description_ru": "",
        "description_en": "",
        "highlights_ru": lines(
            "Python-скрипты для автоматизации работы",
            "Техподдержка и обслуживание компьютерной техники",
            "Настройка сети и видеонаблюдения",
            "Подключение сертификатов для работы с банк-клиентом",
        ),
        "highlights_en": lines(
            "Python automation scripts for daily operations",
            "Hardware support and maintenance",
            "Network and CCTV setup",
            "Certificate setup for the bank-client software",
        ),
    },
    {
        "rank": 40,
        "position_ru": "Оператор ЭВМ",
        "position_en": "Computer operator",
        "company_ru": "Топливный железнодорожный склад",
        "company_en": "Railway fuel depot",
        "location_ru": "Самарканд",
        "location_en": "Samarkand",
        "started_at": date(2018, 1, 1),
        "finished_at": date(2018, 12, 31),
        "is_current": False,
        "description_ru": "",
        "description_en": "",
        "highlights_ru": lines("Техподдержка и обслуживание компьютерной техники", "Установка и настройка ПО"),
        "highlights_en": lines("Hardware support and maintenance", "Software installation and configuration"),
    },
    {
        "rank": 50,
        "position_ru": "Стажировка",
        "position_en": "Internship",
        "company_ru": "Самаркандская городская электросеть",
        "company_en": "Samarkand City Power Grid",
        "location_ru": "Самарканд",
        "location_en": "Samarkand",
        "started_at": date(2013, 1, 1),
        "finished_at": date(2017, 12, 31),
        "is_current": False,
        "description_ru": "Летние стажировки",
        "description_en": "Summer internships",
        "highlights_ru": lines("Перевод должностных инструкций в электронный вид", "Оцифровка схем"),
        "highlights_en": lines("Digitised job descriptions", "Digitised electrical schematics"),
    },
]

EDUCATION = [
    {
        "rank": 10,
        "institution_ru": "Самаркандский профессиональный колледж железнодорожного транспорта",
        "institution_en": "Samarkand Professional College of Railway Transport",
        "degree_ru": "Среднее профессиональное образование",
        "degree_en": "Vocational secondary education",
        "speciality_ru": "Эксплуатация железных дорог",
        "speciality_en": "Railway operations",
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
        "description_ru": "Окончил с отличием",
        "description_en": "Graduated with distinction",
    },
]

COURSES = [
    {
        "rank": 10,
        "title_ru": "Администрирование Linux, сети и виртуализация",
        "title_en": "Linux administration, networking and virtualisation",
        "provider_ru": "Самообразование и практика",
        "provider_en": "Self-study and practice",
        "started_at": date(2019, 1, 1),
        "is_current": True,
    },
    {
        "rank": 20,
        "title_ru": "Программирование на Python",
        "title_en": "Python programming",
        "provider_ru": "Foxford и открытые курсы",
        "provider_en": "Foxford and open courses",
        "started_at": date(2019, 1, 1),
        "finished_at": date(2020, 12, 31),
    },
    {
        "rank": 30,
        "title_ru": "HTML5, CSS и JavaScript",
        "title_en": "HTML5, CSS and JavaScript",
        "provider_ru": "Открытые курсы",
        "provider_en": "Open courses",
        "started_at": date(2018, 1, 1),
        "finished_at": date(2019, 12, 31),
    },
]

# =============================================================================
# Stack. (name_ru, name_en, is_featured). Projects reference skills by name_ru.
# =============================================================================

SKILL_GROUPS = [
    {
        "rank": 10,
        "title_ru": "Backend",
        "title_en": "Backend",
        "skills": [
            ("Python", "Python", True),
            ("Django", "Django", True),
            ("Django REST Framework", "Django REST Framework", True),
            ("Celery", "Celery", False),
            ("Django Channels", "Django Channels", False),
            ("PostgreSQL", "PostgreSQL", True),
            ("Redis", "Redis", False),
            ("ClickHouse", "ClickHouse", False),
            ("Elasticsearch", "Elasticsearch", False),
            ("pytest", "pytest", False),
            ("Платёжные шлюзы", "Payment gateways", False),
            ("Telegram-боты (aiogram)", "Telegram bots (aiogram)", False),
        ],
    },
    {
        "rank": 20,
        "title_ru": "Инфраструктура",
        "title_en": "Infrastructure",
        "skills": [
            ("Linux", "Linux", True),
            ("Docker", "Docker", True),
            ("Proxmox VE", "Proxmox VE", True),
            ("KVM", "KVM", False),
            ("Nginx", "Nginx", False),
            ("MinIO / S3", "MinIO / S3", True),
            ("ZFS / RAID", "ZFS / RAID", False),
            ("MikroTik", "MikroTik", False),
            ("OPNsense", "OPNsense", False),
            ("WireGuard", "WireGuard", False),
            ("Bash", "Bash", False),
        ],
    },
    {
        "rank": 30,
        "title_ru": "CI/CD и мониторинг",
        "title_en": "CI/CD & monitoring",
        "skills": [
            ("Git", "Git", False),
            ("GitHub Actions", "GitHub Actions", True),
            ("GitLab CI", "GitLab CI", False),
            ("GHCR / Docker Registry", "GHCR / Docker Registry", False),
            ("VictoriaMetrics", "VictoriaMetrics", True),
            ("Grafana", "Grafana", False),
            ("VictoriaLogs", "VictoriaLogs", False),
            ("Alertmanager", "Alertmanager", False),
        ],
    },
    {
        "rank": 40,
        "title_ru": "Видео и real-time",
        "title_en": "Video & real-time",
        "skills": [
            ("FFmpeg", "FFmpeg", True),
            ("NVENC", "NVENC", False),
            ("HLS", "HLS", True),
            ("SRT", "SRT", False),
            ("MediaMTX", "MediaMTX", False),
            ("LiveKit", "LiveKit", False),
            ("WebRTC", "WebRTC", False),
        ],
    },
    {
        "rank": 50,
        "title_ru": "AI-инфраструктура",
        "title_en": "AI infrastructure",
        "skills": [
            ("NVIDIA GPU", "NVIDIA GPU", True),
            ("SGLang", "SGLang", False),
            ("vLLM", "vLLM", False),
            ("LLM-шлюз", "LLM gateway", False),
            ("ComfyUI", "ComfyUI", False),
            ("STT / TTS", "STT / TTS", False),
        ],
    },
    {
        "rank": 60,
        "title_ru": "Интеграции",
        "title_en": "Integrations",
        "skills": [
            ("Keycloak", "Keycloak", False),
            ("Odoo", "Odoo", False),
            ("Hikvision ISAPI", "Hikvision ISAPI", False),
            ("OSRM", "OSRM", False),
            ("Firebase", "Firebase", False),
        ],
    },
    {
        "rank": 70,
        "title_ru": "Frontend",
        "title_en": "Frontend",
        "skills": [
            ("HTML / CSS", "HTML / CSS", False),
            ("JavaScript", "JavaScript", False),
            ("TypeScript", "TypeScript", False),
            ("React", "React", False),
            ("HTMX", "HTMX", False),
            ("Alpine.js", "Alpine.js", False),
        ],
    },
]

# =============================================================================
# Projects
# =============================================================================

PROJECT_CATEGORIES = [
    {"rank": 10, "slug": "media", "title_ru": "Медиа и стриминг", "title_en": "Media & streaming"},
    {"rank": 20, "slug": "education", "title_ru": "Образование и сервисы", "title_en": "Education & services"},
    {"rank": 30, "slug": "culture", "title_ru": "Музеи и госсектор", "title_en": "Museums & public sector"},
    {"rank": 40, "slug": "enterprise", "title_ru": "Корпоративные системы", "title_en": "Enterprise systems"},
    {"rank": 50, "slug": "infrastructure", "title_ru": "Инфраструктура", "title_en": "Infrastructure"},
    {"rank": 60, "slug": "personal", "title_ru": "Свои проекты", "title_en": "Own projects"},
    {"rank": 70, "slug": "open-source", "title_ru": "Open source", "title_en": "Open source"},
]

LIVE = Project.Status.LIVE
INTERNAL = Project.Status.INTERNAL
DEVELOPMENT = Project.Status.DEVELOPMENT
OPEN_SOURCE = Project.Status.OPEN_SOURCE
ARCHIVED = Project.Status.ARCHIVED

CIC_RU = "Центр исламской цивилизации в Узбекистане"
CIC_EN = "Centre of Islamic Civilization in Uzbekistan"

# `category` is a PROJECT_CATEGORIES slug, `skills` are Skill.name_ru values from
# SKILL_GROUPS above. Featured projects are shown wider, with their highlights.
PROJECTS = [
    {
        "rank": 10,
        "slug": "splay",
        "category": "media",
        "status": LIVE,
        "is_featured": True,
        "title_ru": "SPlay — онлайн-кинотеатр",
        "title_en": "SPlay — streaming service",
        "summary_ru": "Подписочный видеосервис: фильмы, сериалы, телеканалы и мини-драмы на телефонах, Smart TV и в вебе",
        "summary_en": "Subscription video service: films, series, live TV and mini-dramas on phones, Smart TVs and the web",
        "description_ru": (
            "SPlay (бывший SevimliPlay) — онлайн-кинотеатр с фильмами, сериалами, мультфильмами, "
            "трансляциями телеканалов и вертикальными мини-драмами SDrama. Клиенты — Android, iOS, "
            "Android TV, Tizen, webOS, Apple TV и веб.\n\n"
            "С мая 2022 года я основной разработчик серверной части: основной API, биллинг, статистика, "
            "видеоконвейер и live-TV origin — и вся инфраструктура, на которой это работает. Сервис "
            "собран из нескольких Django-сервисов: контент и пользователи, биллинг с отдельной базой, "
            "статистика в ClickHouse, сервис VOD и GPU-кодировщик. Видеотека — около 290 ТБ HLS на трёх "
            "origin-серверах с зеркалами."
        ),
        "description_en": (
            "SPlay (formerly SevimliPlay) is a streaming service with films, series, cartoons, live TV "
            "channels and vertical SDrama mini-dramas. Clients: Android, iOS, Android TV, Tizen, webOS, "
            "Apple TV and the web.\n\n"
            "Since May 2022 I have been the main developer of the server side — the core API, billing, "
            "statistics, the video pipeline and the live-TV origin — and of all the infrastructure it runs "
            "on. The service is a set of Django services: content and users, billing with its own database, "
            "statistics in ClickHouse, a VOD service and a GPU encoder. The library is about 290 TB of HLS "
            "on three mirrored origin servers."
        ),
        "role_ru": "Ведущий backend-разработчик · DevOps",
        "role_en": "Lead backend developer · DevOps",
        "period_ru": "2022 — н.в.",
        "period_en": "2022 — now",
        "highlights_ru": lines(
            "Основной API: каталог, эпизоды, подборки, ТВ-каналы, реклама, промокоды, мини-драмы, поиск "
            "на Elasticsearch — около 1 450 из 1 790 коммитов",
            "Биллинг: подписки и баланс, Payme, Click, Atmos, Octo, Paynet, покупки в App Store и Google Play",
            "Собственное AES-шифрование HLS с короткоживущими подписанными ссылками и защита каналов от ретрансляции",
            "Кодирование на GPU (FFmpeg + NVENC): несколько качеств, спрайты превью, метрики кодировщика",
            "Live-TV origin: приём multicast и SRT, перекодирование на GPU, раздача HLS и ретрансляция "
            "канала кабельному оператору",
            "Статистика просмотров и подписок в ClickHouse с ежедневными отчётами в Telegram",
            "Спроектировал серверную архитектуру и сам поднял всю инфраструктуру сервиса",
        ),
        "highlights_en": lines(
            "Core API: catalogue, episodes, collections, TV channels, ads, promo codes, mini-dramas, "
            "Elasticsearch search — about 1,450 of 1,790 commits",
            "Billing: subscriptions and balance, Payme, Click, Atmos, Octo, Paynet, App Store and Google Play "
            "purchases",
            "Custom AES encryption of HLS with short-lived signed links and protection of live channels "
            "against restreaming",
            "GPU encoding (FFmpeg + NVENC): several qualities, preview sprites, encoder metrics",
            "Live-TV origin: multicast and SRT ingest, GPU transcoding, HLS delivery and a relay to a cable operator",
            "Viewing and subscription statistics in ClickHouse with daily Telegram reports",
            "Designed the server architecture and built the whole infrastructure of the service myself",
        ),
        "project_url": "https://splay.uz",
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Redis",
            "ClickHouse",
            "Elasticsearch",
            "Платёжные шлюзы",
            "FFmpeg",
            "NVENC",
            "HLS",
            "SRT",
            "Docker",
            "Nginx",
            "Proxmox VE",
        ],
    },
    {
        "rank": 20,
        "slug": "iccu-tickets",
        "category": "culture",
        "status": DEVELOPMENT,
        "is_featured": True,
        "title_ru": "Билетная система Центра исламской цивилизации",
        "title_en": "Ticketing for the Centre of Islamic Civilization",
        "summary_ru": "Сеансы, сайт, киоски, касса, турникеты и AI-ассистент покупки для крупного музея в Ташкенте",
        "summary_en": "Timed sessions, website, kiosks, cashier desk, turnstiles and an AI purchase assistant for a major "
        "museum in Tashkent",
        "description_ru": (
            "Билетная система Центра исламской цивилизации в Узбекистане: продажа на сеансы через сайт, "
            "киоски самообслуживания, кассу и организации, проверка QR-билетов на турникетах, кассовая "
            "дисциплина со сменами и фискальными чеками, доставка билетов в Telegram. Купить билет можно "
            "и через AI-ассистента, который работает на собственных языковых моделях Центра.\n\n"
            "Весь backend — мой: от модели данных и правил ценообразования до API-документации для "
            "каждого клиента — сайта, киоска, кассы, турникетов и бота."
        ),
        "description_en": (
            "The ticketing system of the Centre of Islamic Civilization in Uzbekistan: timed-session sales "
            "on the website, self-service kiosks, the cashier desk and for organisations, QR validation at "
            "the turnstiles, cash discipline with shifts and fiscal receipts, ticket delivery in Telegram. "
            "A ticket can also be bought through an AI assistant running on the Centre's own language "
            "models.\n\n"
            "The whole backend is mine: from the data model and pricing rules to the API docs for every "
            "client — website, kiosk, cashier, turnstiles and bot."
        ),
        "role_ru": "Backend-архитектор",
        "role_en": "Backend architect",
        "client_ru": CIC_RU,
        "client_en": CIC_EN,
        "period_ru": "2026",
        "period_en": "2026",
        "highlights_ru": lines(
            "Сеансы с вместимостью, правила цен, допуслуги, групповые заявки и бронь гидов",
            "Каналы продаж: сайт, киоски с приёмом наличных, касса, организации (B2B)",
            "Проверка QR-билетов на турникетах и пунктах контроля",
            "Оплата картами через e-commerce банка с HMAC-подписью и собственный генератор EMV QR",
            "AI-ассистент покупки: 12 разрешённых инструментов, проверка по JSON Schema, семафор на GPU",
            "Около 700 тестов и документация всех 84 маршрутов API",
        ),
        "highlights_en": lines(
            "Sessions with capacity, pricing rules, add-ons, group requests and guide booking",
            "Sales channels: website, cash-accepting kiosks, cashier desk, organisations (B2B)",
            "QR ticket validation at turnstiles and checkpoints",
            "Card payments via the bank's e-commerce with HMAC signatures and my own EMV QR generator",
            "AI purchase assistant: 12 whitelisted tools, JSON Schema validation, a GPU semaphore",
            "About 700 tests and docs for all 84 API routes",
        ),
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Redis",
            "MinIO / S3",
            "LLM-шлюз",
            "pytest",
            "Docker",
        ],
    },
    {
        "rank": 30,
        "slug": "ilmi",
        "category": "education",
        "status": LIVE,
        "is_featured": True,
        "title_ru": "Ilmi и «Qizil Pomada» — онлайн-образование",
        "title_en": "Ilmi & Qizil Pomada — online education",
        "summary_ru": "Одна кодовая база для нескольких платформ: онлайн-курсы, мастер-классы, онлайн-школа и сертификаты",
        "summary_en": "One codebase for several platforms: online courses, master classes, an online school and "
        "certificates",
        "description_ru": (
            "Платформы онлайн-обучения компании «Qizil Pomada» — qptolov.uz и ilmi.uz — с мобильными "
            "приложениями для iOS и Android. Я единственный автор backend: курсы и мастер-классы, "
            "онлайн-школа, корзина, генерация сертификатов, вход по одноразовому коду и QR, приём платежей. "
            "Видео хранится и отдаётся собственным зашифрованным HLS.\n\n"
            "На Ilmi — около 28 тысяч пользователей, 190 курсов, 3 100 уроков и 2,6 ТБ видео. В 2026 году "
            "переписываю backend Ilmi на своём django-template."
        ),
        "description_en": (
            "The e-learning platforms of Qizil Pomada — qptolov.uz and ilmi.uz — with iOS and Android "
            "apps. I am the only backend author: courses and master classes, an online school, a cart, "
            "certificate generation, sign-in by one-time code and QR, payments. Video is stored and served "
            "as our own encrypted HLS.\n\n"
            "Ilmi has about 28 thousand users, 190 courses, 3,100 lessons and 2.6 TB of video. In 2026 I am "
            "rewriting the Ilmi backend on my django-template."
        ),
        "role_ru": "Backend-разработчик · DevOps",
        "role_en": "Backend developer · DevOps",
        "client_ru": "ООО «Qizil Pomada»",
        "client_en": "Qizil Pomada LLC",
        "period_ru": "2024 — н.в.",
        "period_en": "2024 — now",
        "highlights_ru": lines(
            "Единственный автор backend: 384 из 385 коммитов в основном репозитории",
            "Восемь платёжных систем: Payme, Click, Atmos, Octo, Payze, Alif, Uzum, Paynet",
            "Собственный видеохостинг: очередь FFmpeg, AES-HLS, одноразовые ссылки, одна сессия на аккаунт",
            "Генерация именных сертификатов",
            "Аудит безопасности: 7 находок, все закрыты в тот же день с регрессионными тестами",
            "Сам поднял и настроил серверы проекта",
        ),
        "highlights_en": lines(
            "Sole backend author: 384 of 385 commits in the main repository",
            "Eight payment systems: Payme, Click, Atmos, Octo, Payze, Alif, Uzum, Paynet",
            "Own video hosting: an FFmpeg queue, AES-HLS, one-time links, one session per account",
            "Personalised certificate generation",
            "Security audit: 7 findings, all fixed the same day with regression tests",
            "Built and configured the project servers myself",
        ),
        "project_url": "https://ilmi.uz",
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Redis",
            "Платёжные шлюзы",
            "FFmpeg",
            "HLS",
            "Firebase",
            "Docker",
            "Nginx",
        ],
    },
    {
        "rank": 40,
        "slug": "monitoring",
        "category": "infrastructure",
        "status": INTERNAL,
        "is_featured": True,
        "title_ru": "Платформа мониторинга компании",
        "title_en": "Company-wide monitoring platform",
        "summary_ru": "Метрики, логи, алерты и статус-страница для ~85 серверов, ~70 проектов и ~190 сервисов",
        "summary_en": "Metrics, logs, alerts and a status page for ~85 servers, ~70 projects and ~190 services",
        "description_ru": (
            "Центральный мониторинг для всего парка: метрики на VictoriaMetrics с push-агентами и "
            "авторизацией по токену на каждый сервер, blackbox-проверки сайтов и сертификатов, логи в "
            "VictoriaLogs, алерты в Telegram. Поверх — собственная control plane на Django и React: реестр "
            "проектов с «паспортами», опрос /deep-health/, таймлайны доступности, инциденты и журнал аудита."
        ),
        "description_en": (
            "Central monitoring for the whole fleet: VictoriaMetrics with push agents and a token per "
            "server, blackbox probes of sites and certificates, logs in VictoriaLogs, Telegram alerts. On "
            "top — my own control plane in Django and React: a project registry with passports, /deep-health/ "
            "polling, availability timelines, incidents and an audit log."
        ),
        "role_ru": "Автор · DevOps",
        "role_en": "Author · DevOps",
        "period_ru": "2026",
        "period_en": "2026",
        "highlights_ru": lines(
            "Единственный автор: 158 из 158 коммитов",
            "~85 серверов, ~70 проектов, ~190 сервисов и ~320 доменов с проверкой DNS и TLS",
            "Мониторинг железа: IPMI, SMART, RAID, вентиляторы, GPU",
            "Стандарт /deep-health/ с эталонной реализацией на Django — внедрён в десяток проектов",
            "Паспорта 69 из 70 проектов собраны параллельными read-only AI-агентами с проверкой на утечку секретов",
            "Статус-стена на 98-дюймовом экране и алерты по темам Telegram-форума",
        ),
        "highlights_en": lines(
            "Sole author: 158 of 158 commits",
            "~85 servers, ~70 projects, ~190 services and ~320 domains with DNS and TLS checks",
            "Hardware monitoring: IPMI, SMART, RAID, fans, GPUs",
            "A /deep-health/ standard with a Django reference implementation, rolled out to a dozen projects",
            "Passports of 69 of 70 projects drafted by parallel read-only AI agents with a secret-leak check",
            "A status wall on a 98-inch screen and alerts routed to Telegram forum topics",
        ),
        "skills": [
            "VictoriaMetrics",
            "Grafana",
            "VictoriaLogs",
            "Alertmanager",
            "Python",
            "Django",
            "React",
            "Docker",
        ],
    },
    {
        "rank": 50,
        "slug": "gpu-ai",
        "category": "infrastructure",
        "status": INTERNAL,
        "is_featured": True,
        "title_ru": "GPU-серверы для LLM",
        "title_en": "GPU servers for LLMs",
        "summary_ru": "8× NVIDIA B200 и 8× RTX PRO 6000 Blackwell: языковые модели, генерация изображений и видео, речь",
        "summary_en": "8× NVIDIA B200 and 8× RTX PRO 6000 Blackwell: language models, image and video generation, speech",
        "description_ru": (
            "Ввёл в эксплуатацию и сопровождаю два GPU-сервера, на которых работают AI-функции наших "
            "продуктов. На HGX-узле с 8× NVIDIA B200 работают крупные языковые и мультимодальные модели на "
            "SGLang за LLM-шлюзом с ключами и бюджетами. Узел с 8× RTX PRO 6000 Blackwell (768 ГБ "
            "видеопамяти, 1 ТБ RAM) обслуживает vLLM, ComfyUI для генерации изображений, видео и липсинка, "
            "распознавание и синтез речи. Конфигурации и runbook-и живут в git."
        ),
        "description_en": (
            "I brought into production and run two GPU servers behind the AI features of our products. The "
            "HGX node with 8× NVIDIA B200 serves large language and multimodal models on SGLang behind an "
            "LLM gateway with keys and budgets. The 8× RTX PRO 6000 Blackwell node (768 GB of VRAM, 1 TB of "
            "RAM) runs vLLM, ComfyUI for image, video and lip-sync generation, speech recognition and "
            "synthesis. Configs and runbooks live in git."
        ),
        "role_ru": "DevOps / MLOps",
        "role_en": "DevOps / MLOps",
        "period_ru": "2026",
        "period_en": "2026",
        "highlights_ru": lines(
            "Сравнение моделей (GLM, Qwen, DeepSeek, Kimi, MiniMax) и бенчмарки",
            "LLM-шлюз со строгой маршрутизацией, виртуальными ключами и бюджетами",
            "Runbook-и инцидентов: перезагрузка драйверов, падения CUDA graph, гарантийная замена GPU-модуля",
            "Установка ОС через BMC и виртуальные носители — без физического доступа",
            "На этих моделях работают AI-ассистент билетной системы, перевод в Zamon и помощник EnglishKids",
        ),
        "highlights_en": lines(
            "Model evaluation (GLM, Qwen, DeepSeek, Kimi, MiniMax) and benchmarks",
            "An LLM gateway with strict routing, virtual keys and budgets",
            "Incident runbooks: driver reloads, CUDA graph crashes, a warranty GPU tray replacement",
            "OS installs through the BMC and virtual media — no physical access needed",
            "These models power the ticketing AI assistant, the Zamon translations and the EnglishKids helper",
        ),
        "skills": ["NVIDIA GPU", "SGLang", "vLLM", "LLM-шлюз", "ComfyUI", "STT / TTS", "Docker", "Linux"],
    },
    {
        "rank": 60,
        "slug": "ark",
        "category": "enterprise",
        "status": INTERNAL,
        "title_ru": "ARK Workspace — корпоративная платформа",
        "title_en": "ARK Workspace — corporate platform",
        "summary_ru": "Кадры и посещаемость, задачи, чаты и звонки, заявки на транспорт и съёмки, единый вход и Odoo",
        "summary_en": "HR and attendance, tasks, chats and calls, transport and shooting requests, SSO and Odoo",
        "description_ru": (
            "Внутренняя корпоративная система: справочник сотрудников и оргструктура, учёт посещаемости по "
            "терминалам распознавания лиц Hikvision, менеджер задач, чаты со звонками на LiveKit, заявки на "
            "съёмки и на транспорт с диспетчеризацией и картой в реальном времени, согласование документов "
            "с QR-проверкой. Единый вход через Keycloak, кадровые данные синхронизируются с Odoo."
        ),
        "description_en": (
            "An internal corporate system: staff directory and org structure, attendance from Hikvision "
            "face-recognition terminals, a task manager, chats with LiveKit calls, shooting and transport "
            "requests with dispatching and a live map, document approval with QR verification. Single "
            "sign-on through Keycloak, HR data synchronised with Odoo."
        ),
        "role_ru": "Ведущий backend · интеграции",
        "role_en": "Lead backend · integrations",
        "period_ru": "2023 — н.в.",
        "period_en": "2023 — now",
        "highlights_ru": lines(
            "Три поколения backend: ARK People (282 из 290 коммитов), ARK v2 и ARK Workspace",
            "Связка терминалов Hikvision с Odoo: люди, лица, события прохода",
            "Переписал агент Hikvision и нашёл ошибку часового пояса в прошивке, сдвигавшую ~16 тыс. отметок",
            "Транспорт: GPS-телеметрия в PostGIS, заказы машин, диспетчеризация, маршруты через OSRM",
            "Odoo с собственными модулями и входом через Keycloak (OIDC)",
            "Перенос S3-бакета без потерь: 57,7 тыс. объектов, переключение за 68 секунд",
        ),
        "highlights_en": lines(
            "Three backend generations: ARK People (282 of 290 commits), ARK v2 and ARK Workspace",
            "Hikvision terminals linked to Odoo: people, faces, access events",
            "Rewrote the Hikvision agent and found a firmware timezone bug that shifted ~16k attendance records",
            "Transport: GPS telemetry in PostGIS, car orders, dispatching, routes via OSRM",
            "Odoo with custom modules and Keycloak (OIDC) sign-in",
            "A lossless S3 bucket migration: 57.7k objects, a 68-second cutover",
        ),
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Django Channels",
            "Celery",
            "PostgreSQL",
            "Keycloak",
            "Odoo",
            "Hikvision ISAPI",
            "LiveKit",
            "OSRM",
        ],
    },
    {
        "rank": 70,
        "slug": "video-platform",
        "category": "infrastructure",
        "status": LIVE,
        "title_ru": "Видеоплатформа: кодирование, VOD и IPTV",
        "title_en": "Video platform: encoding, VOD and IPTV",
        "summary_ru": "~290 ТБ HLS на трёх origin-серверах, кодирование на GPU и live-каналы",
        "summary_en": "~290 TB of HLS on three origin servers, GPU encoding and live channels",
        "description_ru": (
            "Видеоинфраструктура SPlay и образовательных платформ: конвейер кодирования на FFmpeg с NVENC, "
            "хранение и раздача HLS-видеотеки на трёх origin-серверах с зеркалами, приём телеканалов по "
            "multicast и SRT с перекодированием на GPU, запись эфира."
        ),
        "description_en": (
            "The video infrastructure of SPlay and the e-learning platforms: an FFmpeg + NVENC encoding "
            "pipeline, HLS library storage and delivery on three mirrored origin servers, TV channel ingest "
            "over multicast and SRT with GPU transcoding, broadcast recording."
        ),
        "role_ru": "Автор · DevOps",
        "role_en": "Author · DevOps",
        "period_ru": "2022 — н.в.",
        "period_en": "2022 — now",
        "highlights_ru": lines(
            "~290 ТБ HLS VOD на трёх серверах с зеркальными копиями",
            "Кодирование на GPU: несколько качеств видео и аудио, спрайты превью, AES-128",
            "IPTV-origin: multicast/SRT → GPU → HLS и ретрансляция кабельному оператору",
            "Запись каналов 15-минутными сегментами",
            "HLS-кеширование на edge-прокси",
        ),
        "highlights_en": lines(
            "~290 TB of HLS VOD on three servers with mirror copies",
            "GPU encoding: several video and audio qualities, preview sprites, AES-128",
            "IPTV origin: multicast/SRT → GPU → HLS and a relay to a cable operator",
            "Channel recording in 15-minute segments",
            "HLS caching on the edge proxies",
        ),
        "skills": ["FFmpeg", "NVENC", "HLS", "SRT", "MediaMTX", "Nginx", "Linux"],
    },
    {
        "rank": 80,
        "slug": "society-uz",
        "category": "culture",
        "status": LIVE,
        "title_ru": "WOSCU — society.uz и woscu.org",
        "title_en": "WOSCU — society.uz & woscu.org",
        "summary_ru": "Портал о культурном наследии Узбекистана: рукописи, эпиграфика, памятники, издания, лекции и фильмы",
        "summary_en": "Portal on the cultural legacy of Uzbekistan: manuscripts, epigraphy, monuments, editions, lectures "
        "and films",
        "description_ru": (
            "Портал Всемирного общества по изучению, сохранению и популяризации культурного наследия "
            "Узбекистана (woscu.org, society.uz). Большая контентная модель: новости, рукописи, "
            "архитектурная эпиграфика и памятники, карта археологических объектов, факсимильные издания, "
            "лекции, конгрессы, медиатека, документальные фильмы, ЮНЕСКО. Я основной backend-разработчик с "
            "2022 года.\n\n"
            "Также восстановил из бэкапа и перенёс в Docker старый сайт общества legacy.uz — «Культурное "
            "наследие Узбекистана в собраниях мира»."
        ),
        "description_en": (
            "The portal of the World Society for the Study, Preservation and Popularization of the Cultural "
            "Legacy of Uzbekistan (woscu.org, society.uz). A large content model: news, manuscripts, "
            "architectural epigraphy and monuments, a map of archaeological sites, facsimile editions, "
            "lectures, congresses, a media library, documentaries, UNESCO. I have been the main backend "
            "developer since 2022.\n\n"
            "I also restored the Society's older site legacy.uz — \"Cultural Legacy of Uzbekistan in World "
            'Collections" — from a backup and moved it into Docker.'
        ),
        "role_ru": "Backend-разработчик · DevOps",
        "role_en": "Backend developer · DevOps",
        "client_ru": "WOSCU",
        "client_en": "WOSCU",
        "period_ru": "2022 — н.в.",
        "period_en": "2022 — now",
        "highlights_ru": lines(
            "Основной backend-разработчик: около 185 из 257 коммитов",
            "Контентная модель на десятки разделов и API v2 для фронтенда",
            "Конвертация изображений в WebP, CKEditor, фоновые задачи на Celery",
            "Восстановил legacy.uz (MODX/PHP) из бэкапа и упаковал в Docker",
        ),
        "highlights_en": lines(
            "Main backend developer: about 185 of 257 commits",
            "A content model of dozens of sections and an API v2 for the frontend",
            "WebP image conversion, CKEditor, Celery background jobs",
            "Restored legacy.uz (MODX/PHP) from a backup and packaged it in Docker",
        ),
        "project_url": "https://woscu.org",
        "skills": ["Python", "Django", "Django REST Framework", "Celery", "PostgreSQL", "Docker", "Nginx"],
    },
    {
        "rank": 90,
        "slug": "zamon-uz",
        "category": "media",
        "status": LIVE,
        "title_ru": "Zamon.uz — новостной портал",
        "title_en": "Zamon.uz — news portal",
        "summary_ru": "Новый backend портала: лента, рубрики, reels, курсы валют, погода, роли редакции и LLM-перевод",
        "summary_en": "A new portal backend: feed, sections, reels, exchange rates, weather, newsroom roles and LLM "
        "translation",
        "description_ru": (
            "Новостной портал Zamon.uz. В 2025–2026 годах я написал новый backend: новости и рубрики, теги, "
            "reels, статические страницы, курсы валют и погода, роли журналиста и редактора в админке, "
            "перенос данных со старого сайта. Материалы переводятся в админке с помощью LLM сразу на "
            "узбекский (латиница и кириллица), русский и английский."
        ),
        "description_en": (
            "The Zamon.uz news portal. In 2025–2026 I wrote its new backend: news and sections, tags, reels, "
            "static pages, exchange rates and weather, journalist and editor roles in the admin, data "
            "migration from the old site. Articles are translated in the admin by an LLM into Uzbek (Latin "
            "and Cyrillic), Russian and English at once."
        ),
        "role_ru": "Backend-разработчик",
        "role_en": "Backend developer",
        "period_ru": "2025 — н.в.",
        "period_en": "2025 — now",
        "highlights_ru": lines(
            "Новый backend: 95 из 106 коммитов",
            "LLM-перевод материалов на четыре языка и письменности",
            "Sitemap с прогревом кеша и Google Indexing API",
            "Медиа в MinIO, деплой через GitHub Actions, перенос данных со старого сайта",
        ),
        "highlights_en": lines(
            "New backend: 95 of 106 commits",
            "LLM translation of articles into four languages and scripts",
            "Sitemaps with cache warming and the Google Indexing API",
            "Media in MinIO, GitHub Actions deploys, data migration from the old site",
        ),
        "project_url": "https://zamon.uz",
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Redis",
            "MinIO / S3",
            "LLM-шлюз",
            "GitHub Actions",
        ],
    },
    {
        "rank": 100,
        "slug": "sobor",
        "category": "personal",
        "status": LIVE,
        "is_featured": True,
        "title_ru": "Сайт Свято-Алексеевского собора",
        "title_en": "St. Alexius Cathedral website",
        "summary_ru": "Сайт собора в Самарканде: новости, православный календарь, жития святых и умный поиск",
        "summary_en": "The website of the cathedral in Samarkand: news, the Orthodox calendar, lives of saints and smart "
        "search",
        "description_ru": (
            "Сайт Свято-Алексеевского собора в Самарканде — от дизайна до сервера делаю сам. Django 6 с HTMX "
            "и Alpine.js, нечёткий поиск на pg_trgm, настроенный на реальных данных, православный календарь "
            "с правилами дат и вычисляемой пасхалией, около 2 100 житий святых, 46 праздников, словарь из "
            "229 терминов и 588 новостей, перенесённых из Telegram-канала. В 2026 году переписал свою первую "
            "версию сайта 2021 года."
        ),
        "description_en": (
            "The website of St. Alexius Cathedral in Samarkand — I do everything from design to the server. "
            "Django 6 with HTMX and Alpine.js, fuzzy search on pg_trgm tuned on real data, the Orthodox "
            "calendar with date rules and a computed Paschalion, about 2,100 lives of saints, 46 feasts, a "
            "229-term glossary and 588 news posts imported from the Telegram channel. In 2026 I rewrote my "
            "own first version of the site from 2021."
        ),
        "role_ru": "Разработчик и администратор",
        "role_en": "Developer and administrator",
        "period_ru": "2021 — н.в.",
        "period_en": "2021 — now",
        "highlights_ru": lines(
            "Единственный разработчик: 119 коммитов и около 550 тестов",
            "Православный календарь с вычисляемой пасхалией",
            "Нечёткий поиск на PostgreSQL pg_trgm",
            "Импорт 588 новостей из Telegram",
            "Медиа в собственном S3, SEO с hreflang, работает на моём сервере",
        ),
        "highlights_en": lines(
            "Sole developer: 119 commits and about 550 tests",
            "The Orthodox calendar with a computed Paschalion",
            "Fuzzy search on PostgreSQL pg_trgm",
            "588 news posts imported from Telegram",
            "Media in my own S3, SEO with hreflang, runs on my own server",
        ),
        "project_url": "https://sobor.uz",
        "skills": [
            "Python",
            "Django",
            "HTMX",
            "Alpine.js",
            "PostgreSQL",
            "Redis",
            "Celery",
            "MinIO / S3",
            "Docker",
        ],
    },
    {
        "rank": 110,
        "slug": "django-template",
        "category": "open-source",
        "status": OPEN_SOURCE,
        "is_featured": True,
        "title_ru": "django-template",
        "title_en": "django-template",
        "summary_ru": "Production-шаблон Django: Docker, uv, CI/CD в GHCR и деплой по SSH — основа ~30 проектов компании",
        "summary_en": "A production Django starter: Docker, uv, CI/CD to GHCR and SSH deploys — the base of ~30 company "
        "projects",
        "description_ru": (
            "Мой публичный шаблон для backend-проектов: Django 5.2 + DRF, PostgreSQL, Redis, Celery, MinIO, "
            "Nginx, настройки по окружениям, структурные логи, pytest, Ruff, pre-commit, GitHub Actions и "
            "GitLab CI со сборкой образа в GHCR и деплоем по SSH, документация по деплою и бэкапам. В "
            "компании на нём построено около 30 проектов, для новых он обязателен. Этот сайт тоже на нём."
        ),
        "description_en": (
            "My public starter for backend projects: Django 5.2 + DRF, PostgreSQL, Redis, Celery, MinIO, "
            "Nginx, per-environment settings, structured logs, pytest, Ruff, pre-commit, GitHub Actions and "
            "GitLab CI that build the image into GHCR and deploy over SSH, plus deploy and backup docs. About "
            "30 company projects are built on it, and it is mandatory for new ones. This site runs on it too."
        ),
        "role_ru": "Автор",
        "role_en": "Author",
        "period_ru": "2025 — н.в.",
        "period_en": "2025 — now",
        "highlights_ru": lines(
            "Около 30 проектов компании построены на шаблоне",
            "Сервер не собирает код: git pull и make prod deploy",
            "Тесты без внешних сервисов и проверка рассинхрона миграций",
            "Прошёл состязательное ревью: исправлены 24 найденные проблемы",
        ),
        "highlights_en": lines(
            "About 30 company projects are built on it",
            "Servers never build: git pull and make prod deploy",
            "Tests without external services and a migrations drift check",
            "Hardened by an adversarial review: 24 findings fixed",
        ),
        "repository_url": "https://github.com/igorkhaylov/django-template",
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Redis",
            "MinIO / S3",
            "Docker",
            "GitHub Actions",
            "pytest",
        ],
    },
    {
        "rank": 120,
        "slug": "iccu-digital",
        "category": "culture",
        "status": LIVE,
        "title_ru": "Цифровые сервисы Центра исламской цивилизации",
        "title_en": "Digital services of the Centre of Islamic Civilization",
        "summary_ru": "QR-пропуска, цифровой архив экспонатов, каталог книг, IT-инвентарь, роботы-гиды и аудиогид",
        "summary_en": "QR passes, a digital exhibit archive, a book catalogue, IT inventory, robot guides and an audio guide",
        "description_ru": (
            "Набор систем для музея и визит-центра. Часть backend-сервисов пишу сам, за все отвечаю как "
            "DevOps: серверы, деплой, мониторинг и связка сервисов между собой."
        ),
        "description_en": (
            "A set of systems for the museum and visitor centre. I write part of the backend services and "
            "own all of them as DevOps: servers, deploys, monitoring and how the services talk to each other."
        ),
        "role_ru": "Backend · DevOps",
        "role_en": "Backend · DevOps",
        "client_ru": CIC_RU,
        "client_en": CIC_EN,
        "period_ru": "2025 — н.в.",
        "period_en": "2025 — now",
        "highlights_ru": lines(
            "QR Pass — бейджи с печатью в PDF и контроль доступа на мероприятиях",
            "Цифровой архив экспонатов на трёх языках с 360°-кадрами, аудио и видео и киоск-приложение для планшетов",
            "API каталога книг и рукописей с генеалогическими деревьями",
            "IT-инвентарь с картой залов: рефакторинг и перенос в продакшен без потери 453 точек размещения",
            "Роботы-гиды UBTECH Cruzr: свой backend, интеграция SDK и ROS, уход от облака производителя",
            "Аудиогид: объединил четыре репозитория в монорепо и построил ops-слой",
            "Статус-стена на экране у входа и доступ охраны к камерам через SSH-туннели",
        ),
        "highlights_en": lines(
            "QR Pass — badges printed to PDF and access control at events",
            "A trilingual digital exhibit archive with 360° frames, audio and video, plus a tablet kiosk app",
            "A book and manuscript catalogue API with family trees",
            "IT inventory with hall maps: refactored and moved to production without losing 453 placements",
            "UBTECH Cruzr robot guides: own backend, SDK and ROS integration, moving off the vendor cloud",
            "Audio guide: merged four repositories into a monorepo and built the ops layer",
            "A status wall at the entrance and camera access for security over SSH tunnels",
        ),
        "project_url": "https://iccu.uz",
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "MinIO / S3",
            "Docker",
            "Nginx",
            "VictoriaMetrics",
        ],
    },
    {
        "rank": 130,
        "slug": "shared-services",
        "category": "infrastructure",
        "status": LIVE,
        "title_ru": "Общие сервисы: LiveKit, OSRM, S3, Keycloak",
        "title_en": "Shared services: LiveKit, OSRM, S3, Keycloak",
        "summary_ru": "Видеозвонки, маршруты, объектное хранилище и единый вход — одна инсталляция на все проекты",
        "summary_en": "Video calls, routing, object storage and SSO — one installation for every project",
        "description_ru": (
            "Вместо отдельной копии в каждом проекте — общие сервисы с ключом на проект, квотами и учётом "
            "потребления: LiveKit SFU с TURN для видеозвонков, OSRM для маршрутов по Узбекистану за шлюзом "
            "APISIX, MinIO S3 на нескольких площадках с единым стандартом бакетов и политик, Keycloak для "
            "единого входа, приватный Docker registry."
        ),
        "description_en": (
            "Instead of a copy in every project — shared services with a key per project, quotas and usage "
            "accounting: a LiveKit SFU with TURN for video calls, OSRM routing for Uzbekistan behind an "
            "APISIX gateway, MinIO S3 on several sites with one standard for buckets and policies, Keycloak "
            "for single sign-on, a private Docker registry."
        ),
        "role_ru": "Автор · DevOps",
        "role_en": "Author · DevOps",
        "period_ru": "2024 — н.в.",
        "period_en": "2024 — now",
        "highlights_ru": lines(
            "LiveKit + TURN с дашбордами потребления по ключам",
            "OSRM за APISIX: ключ, квоты и метрики на каждый проект",
            "MinIO: провижининг бакетов, пользователей и квот скриптами",
            "Перенос sobor.uz с облачного S3 на свой MinIO: 66 тыс. объектов",
        ),
        "highlights_en": lines(
            "LiveKit + TURN with per-key usage dashboards",
            "OSRM behind APISIX: a key, quotas and metrics per project",
            "MinIO: buckets, users and quotas provisioned by scripts",
            "Moved sobor.uz from a cloud S3 to my own MinIO: 66k objects",
        ),
        "project_url": "https://livekit.glob.uz",
        "skills": ["LiveKit", "WebRTC", "OSRM", "MinIO / S3", "Keycloak", "Docker", "Nginx"],
    },
    {
        "rank": 140,
        "slug": "ticket-booking",
        "category": "education",
        "status": LIVE,
        "title_ru": "Билеты на мероприятия и закрытые клубы",
        "title_en": "Event ticketing and paid clubs",
        "summary_ru": "Продажа билетов с выбором мест, бейджи, проверка на входе и Telegram-боты платного доступа",
        "summary_en": "Ticket sales with seat maps, badges, entrance checks and Telegram bots selling paid access",
        "description_ru": (
            "Система для мероприятий: события и спикеры, схема зала с рядами и местами, бронирование и "
            "продажа билетов, сканирование на входе, бейджи и заявки в amoCRM. Рядом — Telegram-боты для "
            "продажи доступа в закрытые сообщества с одноразовыми ссылками-приглашениями (Ayol Club)."
        ),
        "description_en": (
            "A system for events: events and speakers, a hall map with rows and seats, booking and ticket "
            "sales, entrance scanning, badges and amoCRM leads. Alongside — Telegram bots selling access to "
            "private communities with one-time invite links (Ayol Club)."
        ),
        "role_ru": "Backend-разработчик",
        "role_en": "Backend developer",
        "period_ru": "2024 — 2025",
        "period_en": "2024 — 2025",
        "highlights_ru": lines(
            "Схема зала, бронирование мест и проверка билетов на входе",
            "Тарифы и оплата через Payme, Click, Atmos, Octo и Alif",
            "Генерация бейджей, заявки в amoCRM, SMS-уведомления",
            "Telegram-боты на aiogram: продажа доступа и одноразовые инвайт-ссылки",
        ),
        "highlights_en": lines(
            "Hall maps, seat booking and ticket checks at the entrance",
            "Tariffs and payments via Payme, Click, Atmos, Octo and Alif",
            "Badge generation, amoCRM leads, SMS notifications",
            "aiogram Telegram bots: paid access and one-time invite links",
        ),
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Платёжные шлюзы",
            "Telegram-боты (aiogram)",
        ],
    },
    {
        "rank": 150,
        "slug": "365psy",
        "category": "education",
        "status": LIVE,
        "title_ru": "365psy — маркетплейс психологов",
        "title_en": "365psy — marketplace for psychologists",
        "summary_ru": "Каталог специалистов, профили и онбординг, сессии и вход через email, Google и Apple",
        "summary_en": "A catalogue of specialists, profiles and onboarding, sessions and sign-in with email, Google and Apple",
        "description_ru": (
            "Backend маркетплейса психологов 365psy: каталог и профили специалистов, онбординг, сессии, "
            "авторизация по email, через Google и Apple, мультиязычность. Два React-фронтенда работают "
            "поверх моего API."
        ),
        "description_en": (
            "The backend of the 365psy marketplace for psychologists: a catalogue and profiles of "
            "specialists, onboarding, sessions, sign-in with email, Google and Apple, multiple languages. "
            "Two React frontends run on top of my API."
        ),
        "role_ru": "Backend-разработчик",
        "role_en": "Backend developer",
        "period_ru": "2025 — 2026",
        "period_en": "2025 — 2026",
        "highlights_ru": lines(
            "Спроектировал и написал backend: 26 из 27 коммитов",
            "Вход по email, через Google и Apple",
            "Каталог, профили и онбординг специалистов",
        ),
        "highlights_en": lines(
            "Designed and wrote the backend: 26 of 27 commits",
            "Sign-in with email, Google and Apple",
            "Catalogue, profiles and onboarding of specialists",
        ),
        "project_url": "https://365psy.app",
        "skills": ["Python", "Django", "Django REST Framework", "Celery", "PostgreSQL", "Docker"],
    },
    {
        "rank": 160,
        "slug": "tezshifo",
        "category": "education",
        "status": DEVELOPMENT,
        "title_ru": "Tez Shifo — платформа клиник",
        "title_en": "Tez Shifo — clinic platform",
        "summary_ru": "Мультитенантная запись к врачам: пациенты, врачи, клиники, расписание, приёмы и отзывы",
        "summary_en": "Multi-tenant doctor booking: patients, doctors, clinics, schedules, appointments and reviews",
        "description_ru": (
            "Вторая версия платформы Tez Shifo: мультитенантный backend на django-template — пациенты, "
            "врачи, клиники, расписание, запись, оплата и отзывы — и два React-приложения: кабинет пациента "
            "с записью в пять шагов и медкартой и админка клиники."
        ),
        "description_en": (
            "Version two of the Tez Shifo platform: a multi-tenant backend on django-template — patients, "
            "doctors, clinics, schedules, booking, payments and reviews — and two React apps: a patient "
            "portal with five-step booking and a medical record, and a clinic admin."
        ),
        "role_ru": "Full-stack разработчик",
        "role_en": "Full-stack developer",
        "period_ru": "2026",
        "period_en": "2026",
        "highlights_ru": lines(
            "Backend v2: 54 из 55 коммитов",
            "Кабинет пациента: поиск врача, запись в пять шагов, медицинская карта",
            "Админка клиники на React 19, TanStack и shadcn/ui",
        ),
        "highlights_en": lines(
            "Backend v2: 54 of 55 commits",
            "Patient portal: doctor search, five-step booking, a medical record",
            "Clinic admin on React 19, TanStack and shadcn/ui",
        ),
        "skills": [
            "Python",
            "Django",
            "Django REST Framework",
            "PostgreSQL",
            "React",
            "TypeScript",
            "Firebase",
            "Docker",
        ],
    },
    {
        "rank": 170,
        "slug": "stv-uz",
        "category": "media",
        "status": LIVE,
        "title_ru": "STV — архив телепередач",
        "title_en": "STV — TV show archive",
        "summary_ru": "Архив передач самаркандского телеканала STV: видео, фотоархив, участники и события по годам",
        "summary_en": "The show archive of the STV channel in Samarkand: video, photo archive, people and events by year",
        "description_ru": (
            "Для самаркандского телеканала STV написал backend архива передач: видео, фотоархив, участники "
            "и события по годам. Позже добавил в новый backend портала stv.uz стандарт /deep-health/ и "
            "проверки в CI."
        ),
        "description_en": (
            "For the STV channel in Samarkand I wrote the backend of the show archive: video, photo archive, "
            "people and events by year. Later I added the /deep-health/ standard and CI checks to the new "
            "stv.uz backend."
        ),
        "role_ru": "Backend-разработчик",
        "role_en": "Backend developer",
        "period_ru": "2023 — 2026",
        "period_en": "2023 — 2026",
        "highlights_ru": lines(
            "Backend архива передач: 24 из 24 коммитов", "Deep-health и CI-проверки для нового портала"
        ),
        "highlights_en": lines("Archive backend: 24 of 24 commits", "Deep-health and CI checks for the new portal"),
        "project_url": "https://stv.uz",
        "skills": ["Python", "Django", "PostgreSQL", "GitLab CI"],
    },
    {
        "rank": 180,
        "slug": "darakchi-uz",
        "category": "media",
        "status": LIVE,
        "title_ru": "Darakchi.uz — новостной портал",
        "title_en": "Darakchi.uz — news portal",
        "summary_ru": "Сайт популярной газеты «Даракчи» с подпиской на печатное издание",
        "summary_en": "The website of the popular Darakchi newspaper with print subscriptions",
        "description_ru": (
            "Онлайн-версия газеты «Даракчи»: новости, журнал и подписка на печатное издание. Я заложил "
            "каркас backend на своём шаблоне и отвечаю за серверы проекта; основную бизнес-логику писал "
            "коллега."
        ),
        "description_en": (
            "The online edition of the Darakchi newspaper: news, a magazine and print subscriptions. I laid "
            "the backend foundation on my template and own the project servers; a colleague wrote most of "
            "the business logic."
        ),
        "role_ru": "Backend · DevOps",
        "role_en": "Backend · DevOps",
        "period_ru": "2024 — н.в.",
        "period_en": "2024 — now",
        "highlights_ru": lines("Каркас backend на django-template", "Серверная инфраструктура и деплой"),
        "highlights_en": lines("Backend foundation on django-template", "Server infrastructure and deploys"),
        "project_url": "https://darakchi.uz",
        "skills": ["Django", "PostgreSQL", "Docker", "Nginx"],
    },
    {
        "rank": 190,
        "slug": "uzbekkino",
        "category": "culture",
        "status": ARCHIVED,
        "title_ru": "Сайт Агентства кинематографии Узбекистана",
        "title_en": "Cinematography Agency of Uzbekistan website",
        "summary_ru": "CMS и API госагентства: новости, фильмы, руководство, документы, открытые данные и обращения",
        "summary_en": "CMS and API of a government agency: news, films, leadership, documents, open data and appeals",
        "description_ru": (
            "Сайт Агентства кинематографии Узбекистана (Uzbekkino): новая структура и дизайн, мобильная "
            "версия, рассылка новостей, обращения граждан с отслеживанием статуса. Backend — CMS и API "
            "госоргана: новости и фильмы, руководство и структура, нормативные и антикоррупционные "
            "документы, открытые данные и открытый бюджет, тендеры, госпрограммы, международное "
            "сотрудничество. Сопровождал сайт и хостинг до 2024 года; сейчас заказчик сайт отключил."
        ),
        "description_en": (
            "The website of the Cinematography Agency of Uzbekistan (Uzbekkino): a new structure and design, "
            "a mobile version, a news mailing list, citizens' appeals with status tracking. The backend is "
            "the agency's CMS and API: news and films, leadership and structure, regulatory and "
            "anti-corruption documents, open data and open budget, tenders, state programmes, international "
            "cooperation. I maintained the site and hosting until 2024; the client has since taken the site "
            "offline."
        ),
        "role_ru": "Backend-разработчик",
        "role_en": "Backend developer",
        "period_ru": "2023 — 2024",
        "period_en": "2023 — 2024",
        "highlights_ru": lines(
            "Backend CMS и API: 75 из 75 коммитов",
            "Разделы открытых данных, открытого бюджета, тендеров и документов",
            "Обращения граждан с отслеживанием статуса и рассылка новостей",
            "Хостинг и сопровождение",
        ),
        "highlights_en": lines(
            "CMS and API backend: 75 of 75 commits",
            "Open data, open budget, tenders and documents sections",
            "Citizens' appeals with status tracking and a news mailing list",
            "Hosting and maintenance",
        ),
        "skills": ["Python", "Django", "Django REST Framework", "PostgreSQL", "Nginx"],
    },
    {
        "rank": 200,
        "slug": "tiffest",
        "category": "culture",
        "status": ARCHIVED,
        "title_ru": "Ташкентский международный кинофестиваль",
        "title_en": "Tashkent International Film Festival",
        "summary_ru": "Сайт кинофестиваля: backend на Django, редизайн, мобильная версия и сопровождение",
        "summary_en": "The film festival website: Django backend, redesign, mobile version and maintenance",
        "description_ru": (
            "Сайт Ташкентского международного кинофестиваля (tiffest.uz): участвовал в разработке backend на "
            "Django и переносе данных со старой версии, в 2024 году для Национального центра развития "
            "кинематографии выполнил редизайн, мобильную версию, новые функции и сопровождение. Сейчас сайт "
            "отключён."
        ),
        "description_en": (
            "The website of the Tashkent International Film Festival (tiffest.uz): I worked on the Django "
            "backend and the data migration from the old version, and in 2024 delivered a redesign, a mobile "
            "version, new features and maintenance for the National Cinematography Development Centre. The "
            "site is offline now."
        ),
        "role_ru": "Backend-разработчик",
        "role_en": "Backend developer",
        "period_ru": "2022 — 2024",
        "period_en": "2022 — 2024",
        "highlights_ru": lines(
            "Backend сайта фестиваля и перенос данных со старой версии",
            "Редизайн и мобильная версия (2024)",
            "Ежемесячное сопровождение",
        ),
        "highlights_en": lines(
            "Festival site backend and the data migration from the old version",
            "Redesign and mobile version (2024)",
            "Monthly maintenance",
        ),
        "skills": ["Python", "Django", "PostgreSQL", "Nginx"],
    },
    {
        "rank": 210,
        "slug": "uzit-dictionary",
        "category": "personal",
        "status": LIVE,
        "title_ru": "UzIt — узбекско-итальянский словарь",
        "title_en": "UzIt — Uzbek–Italian dictionary",
        "summary_ru": "API мобильного словаря: слова, переводы и офлайн-база для приложения",
        "summary_en": "The API of a mobile dictionary: words, translations and an offline database for the app",
        "description_ru": (
            "Backend мобильного словаря: узбекские и итальянские слова, переводы, импорт из Excel и "
            "публикация SQLite-базы для офлайн-режима приложения. В 2026 году перевёл проект на "
            "django-template, контейнеризовал и перенёс на новый сервер так, что установленные приложения "
            "ничего не заметили."
        ),
        "description_en": (
            "The backend of a mobile dictionary: Uzbek and Italian words, translations, Excel import and a "
            "published SQLite database for the app's offline mode. In 2026 I moved it onto django-template, "
            "containerised it and migrated it to a new server without the installed apps noticing."
        ),
        "role_ru": "Backend · DevOps",
        "role_en": "Backend · DevOps",
        "period_ru": "2024 — н.в.",
        "period_en": "2024 — now",
        "highlights_ru": lines(
            "API словаря и раздача офлайн-базы через nginx (X-Accel-Redirect)",
            "Импорт слов из Excel",
            "Переезд на новый сервер с побайтовой сверкой ответов API",
        ),
        "highlights_en": lines(
            "Dictionary API and offline database delivery through nginx (X-Accel-Redirect)",
            "Word import from Excel",
            "A server move verified byte-for-byte against the old API responses",
        ),
        "skills": ["Python", "Django", "Django REST Framework", "PostgreSQL", "Docker", "Nginx"],
    },
    {
        "rank": 220,
        "slug": "englishkids",
        "category": "personal",
        "status": DEVELOPMENT,
        "title_ru": "EnglishKids — кабинет преподавателя",
        "title_en": "EnglishKids — teacher's workspace",
        "summary_ru": "Библиотека материалов, конструктор планов уроков, журнал занятий и AI-помощник для уроков с детьми",
        "summary_en": "A materials library, a lesson-plan builder, a lesson log and an AI helper for teaching kids",
        "description_ru": (
            "Платформа для преподавателя английского для детей 2–7 лет: библиотека материалов, конструктор "
            "планов уроков, журнал занятий и AI-помощник на собственных языковых моделях с резервом на "
            "Claude API. Статический лендинг и кабинет на django-template с HTMX."
        ),
        "description_en": (
            "A platform for an English teacher of children aged 2–7: a materials library, a lesson-plan "
            "builder, a lesson log and an AI helper on our own language models with the Claude API as a "
            "fallback. A static landing page and a workspace on django-template with HTMX."
        ),
        "role_ru": "Автор",
        "role_en": "Author",
        "period_ru": "2026",
        "period_en": "2026",
        "skills": ["Python", "Django", "HTMX", "Celery", "PostgreSQL", "LLM-шлюз"],
    },
    {
        "rank": 230,
        "slug": "react-and-project-templates",
        "category": "open-source",
        "status": OPEN_SOURCE,
        "title_ru": "react-template и project-template",
        "title_en": "react-template and project-template",
        "summary_ru": "Фронтенд-шаблон на React 19 и монорепо «backend + SPA + ops» с общим OpenAPI-контрактом",
        "summary_en": "A React 19 frontend starter and a backend + SPA + ops monorepo with a shared OpenAPI contract",
        "description_ru": (
            "react-template — стартовый фронтенд к django-template: React 19, TypeScript, Vite, TanStack "
            "Router и Query, Tailwind 4, i18n на трёх языках, Vitest и Docker-образ с конфигурацией в "
            "рантайме. project-template собирает backend, SPA и ops-слой в один монорепозиторий с общим "
            "OpenAPI-контрактом и готовностью к Kubernetes."
        ),
        "description_en": (
            "react-template is the frontend starter for django-template: React 19, TypeScript, Vite, TanStack "
            "Router and Query, Tailwind 4, i18n in three languages, Vitest and a Docker image configured at "
            "runtime. project-template puts the backend, the SPA and the ops layer into one monorepo with a "
            "shared OpenAPI contract, ready for Kubernetes."
        ),
        "role_ru": "Автор",
        "role_en": "Author",
        "period_ru": "2026",
        "period_en": "2026",
        "repository_url": "https://github.com/igorkhaylov/project-template",
        "skills": ["React", "TypeScript", "Docker", "GitHub Actions"],
    },
    {
        "rank": 240,
        "slug": "django-stdimage",
        "category": "open-source",
        "status": OPEN_SOURCE,
        "title_ru": "django-stdimage — поддерживаемый форк",
        "title_en": "django-stdimage — maintained fork",
        "summary_ru": "Библиотека изображений для Django 5+: WebP-варианты и DRF-сериализаторы",
        "summary_en": "An image field library for Django 5+: WebP variations and DRF serializers",
        "description_ru": (
            "Поддерживаю форк django-stdimage: совместимость со storage API Django 5+, варианты в WebP, "
            "DRF-сериализаторы, настройка вариантов по умолчанию и обновлённый CI. Релизы v1.0.0–v1.2.0 "
            "используются в django-template."
        ),
        "description_en": (
            "I maintain a fork of django-stdimage: compatibility with the Django 5+ storage API, WebP "
            "variations, DRF serializers, default variations from settings and a refreshed CI. Releases "
            "v1.0.0–v1.2.0 are used by django-template."
        ),
        "role_ru": "Мейнтейнер",
        "role_en": "Maintainer",
        "period_ru": "2026",
        "period_en": "2026",
        "repository_url": "https://github.com/igorkhaylov/django-stdimage",
        "skills": ["Python", "Django"],
    },
]


class Command(BaseCommand):
    help = "Populate the site with the owner's profile, numbers, focus areas, resume, stack and projects."

    @transaction.atomic
    def handle(self, *args, **options):
        profile_data = {k: v for k, v in PROFILE.items() if k != "full_name_ru"}
        profile, _created = Profile.objects.update_or_create(
            full_name_ru=PROFILE["full_name_ru"], defaults=profile_data
        )
        self.stdout.write(self.style.SUCCESS(f"Profile: {profile}"))

        for data in SOCIAL_LINKS:
            SocialLink.objects.update_or_create(profile=profile, url=data["url"], defaults=data)
        self.stdout.write(f"Social links: {len(SOCIAL_LINKS)}")

        for section, rank, value_ru, value_en, label_ru, label_en, note_ru, note_en in STATS:
            Stat.objects.update_or_create(
                section=section,
                rank=rank,
                defaults={
                    "value_ru": value_ru,
                    "value_en": value_en,
                    "label_ru": label_ru,
                    "label_en": label_en,
                    "note_ru": note_ru,
                    "note_en": note_en,
                    "is_published": True,
                },
            )
        self.stdout.write(f"Stats: {len(STATS)}")

        for data in FOCUS_AREAS:
            FocusArea.objects.update_or_create(section=data["section"], title_ru=data["title_ru"], defaults=data)
        self.stdout.write(f"Focus areas: {len(FOCUS_AREAS)}")

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
            for index, (name_ru, name_en, is_featured) in enumerate(group_data["skills"], start=1):
                Skill.objects.update_or_create(
                    name_ru=name_ru,
                    defaults={
                        "name_en": name_en,
                        "group": group,
                        "is_featured": is_featured,
                        "rank": index * 10,
                    },
                )
                skills_total += 1
        self.stdout.write(f"Skills: {skills_total} in {len(SKILL_GROUPS)} groups")

        categories = {}
        for data in PROJECT_CATEGORIES:
            category, _ = ProjectCategory.objects.update_or_create(slug=data["slug"], defaults=data)
            categories[category.slug] = category
        self.stdout.write(f"Project categories: {len(PROJECT_CATEGORIES)}")

        known_skills = set(Skill.objects.values_list("name_ru", flat=True))
        for data in PROJECTS:
            missing = set(data["skills"]) - known_skills
            if missing:
                raise ValueError(f"Project {data['slug']}: unknown skills {sorted(missing)}")
            defaults = {k: v for k, v in data.items() if k not in ("slug", "category", "skills")}
            defaults.setdefault("is_featured", False)
            defaults["category"] = categories[data["category"]]
            project, _ = Project.objects.update_or_create(slug=data["slug"], defaults=defaults)
            project.skills.set(Skill.objects.filter(name_ru__in=data["skills"]))
        self.stdout.write(f"Projects: {len(PROJECTS)}")

        self.stdout.write(self.style.SUCCESS("Done. Covers and gallery images are added through the admin."))
