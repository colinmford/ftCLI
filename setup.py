import setuptools

setuptools.setup(
    name='ftcli',
    version='0.2.3',
    description='ftCLI',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['ftcli=ftcli.ftcli:main']},
    install_requires=[
        'fonttools>=4.21.1',
        'brotli',
        'click',
        'colorama',
        'skia-pathops',
        'zopfli',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    zip_safe=False
)
