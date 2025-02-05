set -e

if [ "$1" = "install" ]; then
    pip3 install -r requirements.txt
    if [ "$EUID" -ne 0 ]; then
        echo "Root priviliges are required to install this app."
        exit 1
    fi
    OUTFILE="/usr/bin/cliflappy"
    cp game.py $OUTFILE
    chmod +x $OUTFILE
    mkdir -p /usr/share/applications
    mkdir -p /usr/share/pixmaps
    cp assets/icon.png /usr/share/pixmaps/cliflappy.png
    cp assets/cliflappy.desktop /usr/share/applications
fi

if [ "$1" = "run" ]; then
    pip3 install -r requirements.txt
    python3 game.py
fi

if [ "$1" = "uninstall" ]; then
    if [ "$EUID" -ne 0 ]; then
        echo "Root priviliges are required to install this app."
        exit 1
    fi
    rm /usr/bin/cliflappy
    rm /usr/share/pixmaps/cliflappy.png
    rm /usr/share/applications/cliflappy.desktop
fi