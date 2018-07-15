# Python CLI for Oxford Dictionaries API with Django App Integration

## Setup

Set up the virtual environment

```console
$ pipenv --three
$ pipenv install
$ bash setup.sh <scripts_directory>
```

And enter the details when prompted to make a `.gitignore`d script and a symlink to it in your `scripts_directory`, which you can run from anywhere to look up (German) words by typing `de <entry>`.

For smoother local development you can export the credentials manually or store them in a `.env` and load them with `pipenv shell` before running `setup.sh`.

Running the script spawns IPython with the rendered response and uploads the data to the Django App. From IPython, more words can be looked up by typing `e <entry>`
