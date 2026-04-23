"""App entry point and WSGI configuration."""

import click

from ingestion.app import create_app


@click.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=5000, type=int)
def run(host: str, port: int) -> None:
    """Run the Flask application."""
    app = create_app()
    app.run(host=host, port=port)


if __name__ == "__main__":
    run()
