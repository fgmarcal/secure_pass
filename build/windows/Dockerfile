FROM debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    WINEDEBUG=-all \
    WINEPREFIX=/wine \
    PYTHON_VERSION=3.11.7

RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        wine \
        wine32 \
        wine64 \
        xauth \
        xvfb \
        zip \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q "https://www.python.org/ftp/python/${PYTHON_VERSION}/python-${PYTHON_VERSION}-amd64.exe" -O /tmp/python-installer.exe \
    && xvfb-run -a bash -c 'wineboot --init || true; wineserver -w; wine reg add "HKEY_CURRENT_USER\\Software\\Wine" /v Version /t REG_SZ /d win10 /f; wine start /wait /unix /tmp/python-installer.exe /quiet InstallAllUsers=0 Include_launcher=0 Include_test=0; wineserver -w; wine C:\\users\\root\\AppData\\Local\\Programs\\Python\\Python311\\python.exe --version; wine C:\\users\\root\\AppData\\Local\\Programs\\Python\\Python311\\python.exe -m pip install --upgrade pip setuptools wheel pyinstaller' \
    && rm /tmp/python-installer.exe

COPY build/windows/build-in-container.sh /usr/local/bin/build-windows-in-container
RUN chmod +x /usr/local/bin/build-windows-in-container

WORKDIR /src
ENTRYPOINT ["build-windows-in-container"]
