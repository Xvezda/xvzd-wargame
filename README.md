BoB 8th Vulnerability Analysis Track CTF
========================================

1. Install docker, docker-compose, git. (Skip if already installed)
```sh
sudo apt-get update
sudo apt-get install docker.io docker-compose git
```

2. Clone git repository
```sh
git clone https://github.com/Xvezda/xvzd-wargame.git wargame
cd wargame
```

3. Run docker compose
```sh
sudo docker-compose up -d
```

Known Issue
-----------
Error - Docker compose version is too low.
`upported config option for services service: ...`

Solve
`sudo docker-compose -f docker-compose-1.2.0.yml up -d`

