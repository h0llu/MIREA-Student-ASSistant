from setuptools import setup

setup(name="MIREA-Student-ASSistant",
      version='0.1.0',
      author='Gennady Govzheev, Alexander Zverev, Artem Anikin',
      description="Telegram student's bot-assistant",
      url='https://github.com/h0llu/mirea-bot-project',
      license='MIT',
      keywords='mirea MIREA bot timetable student schedule',
      packages=open('requirements.txt', 'r').read().splitlines(),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown'
)