# Build the guides and serve them. The host needs Docker and nothing else:
# no Python, no MkDocs, no prebuilt site/ directory.
FROM python:3.12-slim AS build

WORKDIR /src

# libcairo2 and the pango libraries are what the social plugin draws the Open
# Graph cards with; without them its import fails and the build stops.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash findutils git \
        libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-imaging.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-imaging.txt

# Draw the cards. The image build has the libraries above, so unlike a laptop it
# can always do this.
ENV SOCIAL_CARDS=true

COPY mkdocs.yml ./
COPY overrides ./overrides
COPY static ./static
COPY scripts ./scripts
# Keep in step with the top-level pages scripts/build.sh stages; a missing one
# fails the strict build below with a broken nav entry.
COPY README.md capabilities.md glossary.md working-with-ai.md ./
COPY guides ./guides
# scripts/add_dates.py reads commit dates, so the build needs the history. Last,
# because it changes on every commit and would otherwise bust the layers above.
COPY .git ./.git

# Fails the image build on a broken internal link, because mkdocs runs --strict.
RUN ./scripts/build.sh

FROM nginx:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/site /usr/share/nginx/html
