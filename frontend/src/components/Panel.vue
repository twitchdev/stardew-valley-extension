<style lang="scss">
@import '../assets/css/panel.css';
</style>
<template>
  <div class="main">
    <div class="frame">
      <div class="header">
        <div class="title">
          <img src="../assets/imgs/stardew-cloud.png" /> <span>Weather Picker</span>
        </div>
        <div class="title-sub">
          You control the weather in Stardew Valley!
        </div>
      </div>

      <div class="body">
        <div id="error-message" class="message">{{errorMessage}}</div>

      <div v-for="state in states" @click="processVote(state)" class="weather">
        <div class="day" >{{state.day}}</div>
        <img :src="state.image" />
        <span class="vote">
          <img v-if="state.voted" src="../assets/imgs/heart.png"/>
        </span>
      </div>  
        
      </div>
    </div>
  </div>
</template>

<script>
const ROOT_URL = 'https://lhr2ss6lzf.execute-api.us-east-2.amazonaws.com/prod/';
let userID = '';
let channelID= '';
let voteID = '';
const weatherDict = { 0: 'Sunny', 1: 'Rain', 2: 'Wind', 3: 'Storm', 5: 'Snow' };
const twitch = window.Twitch.ext;

export default {
  name: 'Panel',
  data () {
    return {
      weatherCondition: '',
      vote: '',
      errorMessage: 'Select your weather to vote',
      voteID: '',
      states: [
        {
          day: 'Sun',
          image: require('../assets/imgs/stardew-weather-sun.png'),
          voted: false,
          id: 0
        },
        {
          day: 'Rain',
          image: require('../assets/imgs/stardew-weather-rain.png'),
          voted: false,
          id: 1
        },
        {
          day: 'Wind',
          image: require('../assets/imgs/stardew-weather-wind.png'),
          voted: false,
          id: 2
        },
        {
          day: 'Storm',
          image: require('../assets/imgs/stardew-weather-storm.png'),
          voted: false,
          id: 3
        },
        {
          day: 'Snow',
          image: require('../assets/imgs/stardew-weather-snow.png'),
          voted: false,
          id: 5
        },
      ]
    }
  },
  methods: {
    setVoted(day) {
      this.states.forEach(state => {
        state.voted = state.day === day;
      });
    },
    processVote (event) {
      //this.clearVotes();
      this.setVoted(event.day);
      console.log(event);


      fetch (`${ROOT_URL}vote`, {
        method: 'POST',
        headers: new Headers ({ 'Content-Type': 'application/json' }
        ),
        body: JSON.stringify({
          user_id: `${userID}`,
          channel_id: `${channelID}`,
          vote_id: `${this.voteID}`,
          vote_item: event.id
        })
      }).then(data => data.json()).then(result => {
        //console.log(result);
        //twitch.rig.log(result);
        this.errorMessage = result;
      });
    },
    getVoteId () {
      fetch (`${ROOT_URL}vote?channel_id=${channelID}`, {
        method: 'GET'
      }).then(response => response.json()).then(result => {
        this.voteID = result['vote_id'];
      })
    },
    clearVotes () {
      let voteElements = document.getElementsByClassName('vote');
      for (let i = 0; i < voteElements.length; i++) {
        voteElements[i].innerHTML = '';
      }
    }
  },
  created: function () {
    twitch.listen('broadcast', (target, contentType, message) => {
      //twitch.rig.log('Received broadcast ');
      const pubSubMessage = JSON.parse(message);

      switch (pubSubMessage.type) {
        case 'new':
          this.errorMessage = pubSubMessage.message;
          this.voteID = pubSubMessage.vote_id;
          break;
        case 'end':
          this.errorMessage = pubSubMessage.message + ' The winner is ' + weatherDict[pubSubMessage.winning_weather];
          this.clearVotes();
          break;
      }
    });
  },
  async beforeMount () {
    await twitch.onAuthorized((auth) => {
      userID = auth.userId;
      twitch.rig.log(`userID: ${userID}`);
      channelID = auth.channelId;+
      this.getVoteId();
    });
  }
}
</script>
