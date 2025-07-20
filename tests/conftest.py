import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-llm-evaluations", action="store_true", default=False, help="run llm evaluations"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-llm-evaluations"):
        return

    skip = pytest.mark.skip(reason="need --run-llm-evaluations option to run")
    for item in items:
        if "llm_evaluation" in item.keywords:
            item.add_marker(skip)
