from setuptools import setup, find_packages

setup(
    name='Jarvis',
    version='0.1a1',
    description='Personal assistant bot',
    author='Python Forces',
    url='https://github.com/UkrainianEagleOwl/tp_personal_assistant/tree/97c820e0779d54e488d5d824cce404b06bb4e654',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Jarvis=base_team_project.main:main',
        ],
    },
)
