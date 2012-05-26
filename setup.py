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
    "cliff>=0.7",
    "pymysql",
]

tests_require = [
    "nose",
    "webtest",
    "coverage",
]

points = {
    'console_scripts': [
        'shirly=shirly.scripts:main',
    ],
    'shirly.command': [
        'adduser=shirly.scripts:AddUserCommand',
    ],
}

setup(
    name="shirly",
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": tests_require,
        "docs": ["sphinx"],
        "dev": ["alembic", "tox"],
    },
    test_suite="shirly",
    package_dir={"": "src"},
    entry_points=points,
)
