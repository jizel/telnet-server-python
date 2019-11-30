from setuptools import setup, find_packages

setup(
    name = "final_project",
    version = "0.9",
    author = "Jiri Zelezny",
    author_email = "ferum89@gmail.com",
    url = 'https://msivak.fedorapeople.org/python/#(55)',    
    license = "GPLv2+",
    keywords = "server telnet grep",
    description = "PV248 final project 2015",    
    scripts = ["final.py", "parse_args.py", "server.py"],
    packages = find_packages()
)
