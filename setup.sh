#!/bin/bash
PROJ_DIR=$(pwd)
VENV_DIR=$(pipenv --venv)

for var in URL ID KEY DJANGO_URL DJANGO_USER DJANGO_PASS; do
  if ! [[ -v $var ]];
  then
    echo "Please enter the Application $var"
    read $var
  fi
done

cat << EOF > .de.sh
#!/bin/bash
cd $PROJ_DIR
source $VENV_DIR/bin/activate

# conf
export URL=$URL
export ID=$ID
export KEY=$KEY
export DJANGO_URL=$DJANGO_URL
export DJANGO_USER=$DJANGO_USER
export DJANGO_PASS=$DJANGO_PASS

# args
export entry=\$1

ipython -i oxford.ipy
EOF

chmod u=rwx .de.sh

if [[ -n $1 ]]
then
  cd $1
  ln -s $PROJ_DIR/.de.sh de
fi
