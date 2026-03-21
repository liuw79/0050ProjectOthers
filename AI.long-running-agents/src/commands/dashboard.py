import click
import uvicorn

@click.command()
@click.option("--host", default="0.0.0.0", help="Host address")
@click.option("--port", default=8000, help="Port number")
def dashboard(host, port):
    """启动 Web Dashboard"""
    click.echo(f"Starting dashboard on http://{host}:{port}")
    uvicorn.run("src.web.app:app", host=host, port=port)
