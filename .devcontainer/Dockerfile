FROM mcr.microsoft.com/devcontainers/base:debian

# Copy uv binaries directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx