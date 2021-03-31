import setuptools
from sphinx.setup_command import BuildDoc


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

cmdclass = {'build_sphinx': BuildDoc}
name = 'MIREA-Student-ASSistant'
version = '0.0.1'


setuptools.setup(
    name=name,
    version=version,
    cmdclass=cmdclass,
    author='Gennady Govzheev, Alexander Zverev, Artem Anikin',
    description='Telegram student bot-assistant',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/h0llu/mirea-bot-project',
    license='MIT',
    keywords='mirea MIREA bot timetable student schedule',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'source_dir': ('setup.py', 'doc/source'),
            'build_dir': ('setup.py', 'doc/build')}}
)