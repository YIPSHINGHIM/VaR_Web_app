
cd ..
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

cd PROJECT/Server
python manage.py runserver 5000