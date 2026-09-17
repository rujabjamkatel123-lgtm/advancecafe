import os


# =========================================================
# FLASK SECRET KEY
# =========================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-change-in-production"
)

SECURE_SESSION_COOKIE = os.environ.get(
    "SECURE_SESSION_COOKIE",
    "0"  # Local HTTP development; set SECURE_SESSION_COOKIE=1 on HTTPS production
).lower() in {"1", "true", "yes", "on"}

# Public origin used in printed customer QR codes. Set this to the deployed
# HTTPS site URL, for example: https://your-restaurant.vercel.app
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").strip().rstrip("/")


# =========================================================
# MYSQL DATABASE CONFIGURATION
# =========================================================
#
# The application historically used MYSQL_* names. Vercel deployments may
# use the shorter DB_* names, so both names are accepted. MYSQL_* takes
# precedence when both are present.
#
# Aiven's MySQL service uses a non-standard port and requires TLS. Set these
# values in Vercel Production environment variables:
#   DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def _env(primary_name, fallback_name, default=None):
    value = os.environ.get(primary_name)
    if value is None or value.strip() == "":
        value = os.environ.get(fallback_name, default)
    return value.strip() if isinstance(value, str) else value


MYSQL_HOST = _env("MYSQL_HOST", "DB_HOST")
MYSQL_PORT = int(_env("MYSQL_PORT", "DB_PORT", "25595"))
MYSQL_USER = _env("MYSQL_USER", "DB_USER")
MYSQL_PASSWORD = _env("MYSQL_PASSWORD", "DB_PASSWORD")
MYSQL_DATABASE = _env("MYSQL_DATABASE", "DB_NAME", "defaultdb")

# Fail early with a useful deployment error instead of a less-clear PyMySQL
# connection exception when a required variable was omitted in Vercel.
_missing_database_values = [
    name for name, value in {
        "DB_HOST/MYSQL_HOST": MYSQL_HOST,
        "DB_USER/MYSQL_USER": MYSQL_USER,
        "DB_PASSWORD/MYSQL_PASSWORD": MYSQL_PASSWORD,
        "DB_NAME/MYSQL_DATABASE": MYSQL_DATABASE,
    }.items()
    if not value
]

if _missing_database_values:
    raise RuntimeError(
        "Missing database environment variables: "
        + ", ".join(_missing_database_values)
    )
