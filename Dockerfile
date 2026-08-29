# Build the guides and serve them. The host needs Docker and nothing else:
# no Python, no MkDocs, no prebuilt site/ directory.
FROM python:3.12-slim AS build

WORKDIR /src

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash findutils git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mkdocs.yml ./
COPY overrides ./overrides
COPY static ./static
COPY scripts ./scripts
COPY README.md capabilities.md ./
COPY guides ./guides
# scripts/add_dates.py reads commit dates, so the build needs the history. Last,
# because it changes on every commit and would otherwise bust the layers above.
COPY .git ./.git

# Fails the image build on a broken internal link, because mkdocs runs --strict.
RUN ./scripts/build.sh

FROM nginx:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/site /usr/share/nginx/html
