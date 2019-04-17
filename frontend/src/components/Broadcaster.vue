<style lang="scss">
@import '../assets/css/panel.css';
</style>
<template>
  <div class="main">
    <div class="frame">
      <div class="header">
        <div class="title">
          <img src= "../assets/imgs/stardew-cloud.png" /> <span>Weather Picker</span>
        </div>
        <div class="title-sub">
          Broadcaster Panel
        </div>
      </div>
      <div class="body">
          <p><a class="button" @click="newVote">Start a new vote</a></p>
          <p><a class="button" @click="endVote">End vote &amp; process winner</a></p>
      </div>
    </div>
  </div>
</template>

<script>
const ROOT_URL = 'https://lhr2ss6lzf.execute-api.us-east-2.amazonaws.com/prod/';
let channelID= '';
let userID = '';
let token = '';
const twitch = window.Twitch.ext;
let voteID = '';

export default {
  name: 'Panel',
  data () {
    return {
      weatherCondition: '',
      vote: ''
    }
  },
  methods: {
    newVote(){
      fetch (`${ROOT_URL}process_new_vote?channel_id=${channelID}`,{
        method: 'GET',
        headers: new Headers({'Content-Type': 'application/json'},
          ),
        }).then(data => data.json()).then(result => {
          voteID = result['new_vote_id'];
          let pubMessage = {'type': 'new', 'message': 'A new vote has started!', 'vote_id': voteID};
          twitch.send('broadcast', 'application/json', JSON.stringify(pubMessage));
      });
    },
    endVote(){
      fetch (`${ROOT_URL}process_winner?channel_id=${channelID}&vote_id=${voteID}`,{
        method: 'GET',
        headers: new Headers({'Content-Type': 'application/json'},
          ),
        }).then(data => data.json()).then(result => {
          let pubMessage = {'type': 'end',
                            'message': 'Voting Ended!',
                            'winning_weather': result['winning_weather']
                           }
          twitch.send('broadcast', 'application/json',JSON.stringify(pubMessage));
        });
    },
    getVoteID(){
      fetch (`${ROOT_URL}vote?channel_id=${channelID}`,{
        method: 'GET',
        headers: new Headers({'Content-Type': 'application/json'},
        ),
      }).then(data => data.json()).then(result => {
        voteID = result['vote_id'];
      });
    },
  },
  async beforeMount() {
    await twitch.onAuthorized((auth) => {
      userID = auth.userId;
      channelID = auth.channelId;
      token = auth.token;
      this.getVoteID();
    });
  }
}
</script>
