import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="streamlit-nej-datepicker",
    version="1.0.3",
    author="Alireza Nejadipour",
    author_email="nejadipour@gmail.com",
    description="A simple and configurable datepicker for Streamlit with support of both Gregorian and Jalali calendar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nejadipour/streamlit-nej-datepicker",
    project_urls={
        "Bug Tracker": "https://github.com/nejadipour/streamlit-nej-datepicker/issues",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
        "jdatetime",
        "pydantic >= 2.0"
    ],
)
