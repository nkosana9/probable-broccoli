FROM python:3.13

WORKDIR /app

ENV UV_UNMANAGED_INSTALL=/usr/local/bin

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh -o install-uv.sh && \
    chmod +x install-uv.sh && \
    sh ./install-uv.sh && \
    rm install-uv.sh

COPY requirements.txt ./requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

RUN uv pip install --system --no-cache build setuptools && \
    uv pip install --system --no-cache -e .

EXPOSE 8080

CMD ["python", "/app/assignment/wsgi.py", "--host=0.0.0.0", "--port=8080"]
