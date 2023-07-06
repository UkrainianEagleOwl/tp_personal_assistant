from setuptools import setup

setup(
    name='Assist bot',
    version='0.01 alpha',
    description='Personal assistant bot',
    author='Our Team',
    url='https://github.com/UkrainianEagleOwl/tp_personal_assistant/tree/97c820e0779d54e488d5d824cce404b06bb4e654',
    packages=['re'],
    entry_points={
        'console_scripts': [
            'Assist bot=tp_personal_assistant.src.main:main',
        ],
    },
)
