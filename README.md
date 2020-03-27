# Stardew Valley Game Integration Extension

This Extension was built for the Twitch Dev Tour 2019 and showcases how viewers can vote on the in-game weather instead of relying on the game’s default weather algorithm. It has three main components: a frontend UI for the viewer and broadcaster, backend code (EBS) to manage voting and a game mod to manipulate the game state. 

<img src="https://github.com/twitchdev/stardew-valley-extension/blob/master/discovery/screenshoted035da6-a71f-4b62-b72e-17f62e6d7304.png" height="300">

## Building the Frontend

The frontend is written in Vue.js. 

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

## Building the Backend

The backend is written in Python and designed for a serverless setup via AWS Lambda. We’ve provided a Cloud Formation script if you’d like to deploy on AWS.
First, you need install the [SAM toolkit](https://aws.amazon.com/serverless/sam/)

Then run `sam deploy -t databases.yaml` followed by `sam deploy -t functions.yaml` within the templates folder.

## The Game Mod

The interaction between Stardew valley running on the computer and our backend is controlled by a game mod. This mod handles polling the backend to check if a new weather condition is available, as well as forcing the weather change. The mod can be downloaded on [Curse Forge](https://www.curseforge.com/stardewvalley/mods/twitch-in-stardew-valley/files).


