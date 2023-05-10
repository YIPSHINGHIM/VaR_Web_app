cd ..
python -m venv venv

ABS_SCRIPT_PATH="$(realpath "venv")"
# echo "Value of ABS_SCRIPT_PATH: ${ABS_SCRIPT_PATH}"

# * check venv ready or not 
until [ -d "$ABS_SCRIPT_PATH" ]
do
    echo "waiting the venv ready"
    sleep 5
done
echo "File found"

# * check which os using to activat the venv
case "$(uname -sr)" in

   Darwin*)
     echo 'Mac OS X'
     . venv/bin/activate
     ;;

   Linux*Microsoft*)
     echo 'WSL'  # Windows Subsystem for Linux
     . venv/bin/activate
     ;;

   Linux*)
     echo 'Linux'
     . venv/bin/activate
     ;;

   CYGWIN*|MINGW*|MINGW32*|MSYS*)
     echo 'MS Windows'
     . venv/Scripts/activate
     ;;

   *)
     echo 'Other OS' 
     ;;
esac

pip install --upgrade pip     
cd PROJECT
pip install -r requirements.txt 
cd Server
python manage.py makemigrations api && python manage.py makemigrations && python manage.py migrate
cd frontend
npm i
npm run build
exit


