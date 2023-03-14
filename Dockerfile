# syntax = docker/dockerfile:1.2

# Prepare the base environment.
FROM ubuntu:22.04 as builder_base_oim_leaseslicensing

LABEL maintainer="asi@dbca.wa.gov.au"

ENV DEBIAN_FRONTEND=noninteractive \
	TZ=Australia/Perth \
	EMAIL_HOST="email.server" \
	DEFAULT_FROM_EMAIL='no-reply@dbca.wa.gov.au' \
	NOTIFICATION_EMAIL='none@none.com' \
	NON_PROD_EMAIL='none@none.com' \
	PRODUCTION_EMAIL=False \
	EMAIL_INSTANCE='DEV' \
	SECRET_KEY="ThisisNotRealKey" \
	SITE_PREFIX='lals-dev' \
	SITE_DOMAIN='dbca.wa.gov.au' \
	OSCAR_SHOP_NAME='Parks & Wildlife' \
	BPAY_ALLOWED=False \
	BRANCH=$BRANCH_ARG \
	REPO=$REPO_ARG \
	REPO_NO_DASH=$REPO_NO_DASH_ARG \
	POETRY_VERSION=1.2.1

# Use Australian Mirrors
RUN sed 's/archive.ubuntu.com/au.archive.ubuntu.com/g' /etc/apt/sources.list > /etc/apt/sourcesau.list && \
    mv /etc/apt/sourcesau.list /etc/apt/sources.list
# Use Australian Mirrors

RUN --mount=type=cache,target=/var/cache/apt apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    ca-certificates \
    cron \
    curl \
    gdal-bin \
    gcc \
    git \
    gunicorn \
    htop \
    libmagic-dev \
    libproj-dev \
    libpq-dev \
    libreoffice \
    libspatialindex-dev \
    mtr \
    patch \
    postgresql-client \
    python3-dev \
    python3-pip \
    python3-setuptools \
    rsyslog \
    sqlite3 \
    ssh \
    tzdata \
    vim \
    wget && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates

# install node 16
RUN touch install_node.sh && \
	curl -fsSL https://deb.nodesource.com/setup_16.x -o install_node.sh && \
	chmod +x install_node.sh && ./install_node.sh && \
	apt-get install -y nodejs && \
	ln -s /usr/bin/python3 /usr/bin/python && \
	pip install --upgrade pip

FROM builder_base_oim_leaseslicensing as python_dependencies_leaseslicensing
WORKDIR /app

COPY gunicorn.ini manage.py pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Patch also required on local environments after a venv rebuild
# (in local) patch /home/<username>/park-passes/.venv/lib/python3.8/site-packages/django/contrib/admin/migrations/0001_initial.py admin.patch.additional
#RUN patch /usr/local/lib/python3.8/dist-packages/django/contrib/admin/migrations/0001_initial.py /app/admin.patch.additional

FROM python_dependencies_leaseslicensing as collect_static_leaseslicensing
COPY leaseslicensing ./leaseslicensing
RUN touch /app/.env && \
    python manage.py collectstatic --no-input

FROM collect_static_leaseslicensing as install_build_vue3_leaseslicensing
RUN cd /app/leaseslicensing/frontend/leaseslicensing ; npm ci --omit=dev && \
    cd /app/leaseslicensing/frontend/leaseslicensing ; npm run build


FROM install_build_vue3_leaseslicensing as configure_and_launch_leaseslicensing
COPY .git ./.git
COPY ./timezone /etc/timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    touch /app/rand_hash
COPY ./cron /etc/cron.d/dockercron

RUN chmod 0644 /etc/cron.d/dockercron && \
    crontab /etc/cron.d/dockercron && \
    touch /var/log/cron.log && \
    service cron start

COPY ./startup.sh /
RUN chmod 755 /startup.sh
EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]
