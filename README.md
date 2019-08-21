BoB 8th Vulnerability Analysis Track CTF
========================================

How to run
----------

1. Install docker, docker-compose and git.
```sh
sudo apt-get update
sudo apt-get install docker.io docker-compose git
```

2. Clone git repository
```sh
git clone https://github.com/Xvezda/xvzd-wargame.git wargame
cd wargame
```

3. Generate wargame flag
```sh
echo WARGAME_FLAG=FLAG{your_flag_here} > .env
```

4. Run docker compose
```sh
sudo docker-compose up -d
```

Known Issue
-----------
Error - Docker compose version is too low.
```
Unsupported config option for services service: '...'
```

Solve
```sh
sudo docker-compose -f docker-compose-1.2.0.yml up -d
```

