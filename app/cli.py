import typer

app = typer.Typer(
    name="on-course_bot",
    help="OnCourse bot development commands.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Run OnCourse bot development commands."""


if __name__ == "__main__":
    app()
