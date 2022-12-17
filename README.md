# Pending

## Cliente

1. Posibilidad de chat individual
2. Create mobile version

## Servidor
1. Añadir comando 'exitbye' que elimine de la lista a un usuario.
2. Después de X tiempo eliminar usuarios de la lista 
3. Change set to database connection


# Deploying the app in Android Phone

This has been tested in Ubuntu 20.04. If you are using Windows you can use Google Colab to create the apk file with less headache.

First, we need to install **buildozer** in order to convert the .py files to .apk:

    # With our virtual environment activated we execute the next
    pip install --upgrade buildozer
    sudo apt update
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    pip3 install --upgrade Cython==0.29.19 virtualenv
    export PATH=$PATH:~/.local/bin

Now, we need to create the *buildozer.spec* file. To do so, we will execute the next:

    buildozer init

Once the spec is created, we build the apk:

    buildozer -v android debug

If everything has run correctly, a message similar to this should appear:

    # Android packaging done!
    # APK myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk available in the bin directory