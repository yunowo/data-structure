pyuic5 main.ui -o generated/main.py --from-imports
pyuic5 encode.ui -o generated/encode.py
pyuic5 freq.ui -o generated/freq.py
pyrcc5 res.qrc -o generated/res_rc.py