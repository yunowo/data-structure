pyuic5 main.ui -o ../generated/main.py --from-imports
pyuic5 encode.ui -o ../generated/encode.py --from-imports
pyuic5 about.ui -o ../generated/about.py --from-imports
pyrcc5 res.qrc -o ../generated/res_rc.py