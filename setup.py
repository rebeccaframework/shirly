from setuptools import setup, find_packages

requires = [
    "pyramid",
    "pyramid-tm",
    "pyramid-who",
    "pyramid-fanstatic",
    "pyramid-simpleform",
    "sqlahelper",
    "repoze.who",
    "repoze.who.plugins.sa",
    "waitress",
    "js.jquery",
    "js.jqueryui",
    "js.tinymce",
    "js.bootstrap",
]

tests_require = [
    "nose",
    "webtest",
    "coverage",
    "tox",
    "mock",
]

points = {
    'console_scripts': [
        'add_user=shirly.scripts:add_user',
    ],
}

setup(
    name="shirly",
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": tests_require,
        "docs": ["sphinx"],
        "dev": ["alembic"],
        "mysql": ["pymysql"],
    },
    test_suite="shirly",
    package_dir={"": "src"},
    entry_points=points,
)
