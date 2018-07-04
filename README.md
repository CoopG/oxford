# Python Client for Oxford Dictionaries API

## Setup

Set up the virtual environment

```console
$ pipenv --three
$ pipenv install
$ bash setup.sh <scripts_directory>
```

And enter the details when prompted to make a `.gitignore`d script and a symlink to it in your `scripts_directory`, which you can run from anywhere to look up (German) words by typing `de <entry> <lexicalCategory>`.

For smoother local development you can export the credentials manually or store them in a `.env` and load them with `pipenv shell` before running `setup.sh`.
