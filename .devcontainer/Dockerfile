FROM mcr.microsoft.com/devcontainers/base:debian

# Copy uv binaries directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

# Ensure binaries are executable and owned by the vscode user
RUN chmod +x /bin/uv /bin/uvx \
    && chown vscode:vscode /bin/uv /bin/uvx

# Optional: If you want uv available in the python environment immediately
# ENV PATH="/home/vscode/.local/bin:${PATH}"