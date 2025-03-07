# Setup
1. Install [Python](https://www.python.org/downloads/)
2. Install [node.js](https://nodejs.org/en/download/)
3. Install [git](https://git-scm.com/downloads)
4. Clone the repository in your preferred directory
```bash
git clone https://github.com/simoovara/twitch-chat-simulator
```
5. Navigate to the project directory
```bash
cd twitch-chat-simulator
```
6. Navigate to the discordBot directory
```bash
cd discordBot
```
7. Create a virtual environment
```bash
python -m venv .venv
```
8. Activate the virtual environment
```bash
.venv\Scripts\activate
```

9. Assuming you setup everything correctly, you should be able to run the following command to install the required packages
```bash
npm run install:pythonDeps
```

10. Run the project, this will run the discord bot and the websocket server
```bash
npm run start
```

At this point, just open index.html in your browser and everything should be working

