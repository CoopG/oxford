#!/bin/bash
PROJ_DIR=$(pwd)
VENV_DIR=$(pipenv --venv)

for var in URL ID KEY; do
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

# args
export entry=\$1
export lexicalCategory=\$2

ipython -i oxford.py
EOF

chmod u=rwx .de.sh

if [[ -n $1 ]]
then
  cd $1
  ln -s $PROJ_DIR/.de.sh de
fi
