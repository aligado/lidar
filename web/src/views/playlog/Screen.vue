<template>
  <div class="screen-container">
    <car class="car"></car>
    <div class="pot"></div>
    <div class="digit-left">
      <p>8</p>
    </div>
    <div class="digit-right">
      <p>8</p>
    </div>
    <laneleft v-show="laneLeftOn" class="laneleft"></laneleft>
    <laneright v-show="laneRightOn" class="laneright"></laneright>
  </div>
</template>

<script>
  import {Howl} from 'howler' 
  import car from './svg/car';
  import laneleft from './svg/laneleft';
  import laneright from './svg/laneright';
  import { staticUrl } from '@/api/static'

  export default {
    components: { car, laneleft, laneright },
    props: {
      laneLeftState: {
        type: Boolean,
        default: false
      },
      laneRightState: {
        type: Boolean,
        default: false
      },
      laneWarning: {
        type: Number,
        default: 0
      }
    },
    data() {
      return {
        sound: {
          ldw: null,
          fcw: null
        }
      }
    },
    computed: {
      laneLeftOn: function() {
        return (this.laneWarning & 0x1)>0
      },
      laneRightOn: function() {
        return (this.laneWarning & 0x2)>0
      }
    },
    watch:{
      laneWarning(newLaneWarning) {
        console.log('newLaneWarning', newLaneWarning)
        /*
        if (newLaneWarning == 5) {  // emit: start left warning
          this.soundPlay('ldw', 1)
        } else if (newLaneWarning == 6) {  // emit: start right warning
          this.soundPlay('ldw', 1)
        } else if (newLaneWarning == 4) {  // emit: stop warning
          this.soundPlay('ldw', 0)
        }
        */
        if (newLaneWarning == 0) {  // emit: start left warning
          this.soundPlay('ldw', 0)
        } else {  // emit: start right warning
          this.soundPlay('ldw', 1)
        }
      }
    },
    mounted() {
      let LDWmp3 = staticUrl + 'webstatic/' + 'LDW.mp3'
      let FCWmp3 = staticUrl + 'webstatic/' + 'FCW.mp3'
      this.sound.ldw = new Howl({
        src: [LDWmp3],
        loop: true
      })
      this.sound.fcw = new Howl({
        src: [FCWmp3],
        loop: true
      })
    },
    methods: {
      soundPlay(sound, type) {
        console.log('soundPlay', sound, type)
        if (type) {
          if (!this.sound.ldw.playing()) this.sound.ldw.play()
        } else {
          this.sound.ldw.stop()
        }
      }
    },
    beforeDestroy() {
      this.sound.ldw.stop()
      this.sound.fcw.stop()
    }
  }
</script>

<style>
  .screen-container {
    width: 232px;
    height: 232px;
    background: rgb(33, 33, 33);
    border-radius: 232px;
    position: relative;
  }
  .car {
    position: absolute;
    top: 125px;
    right: 66px;
  }
  .pot {
    position: absolute;
    top: 100px;
    right: 111px;
    width: 10px;
    height: 10px;
    border-radius: 10px;
    background:white;
  }

  .digit-left {
    position: absolute;
    top: -50px;
    left: 80px;
    font-family: 'ddt';
    font-size: 80px;
    color: white;
  }

  .digit-right {
    position: absolute;
    top: -50px;
    right: 75px;
    font-family: 'ddt';
    font-size: 80px;
    color: white;
  }
  .laneleft {
    position: absolute;
    top: -5px;
    left: 5px;
    height:240px; 
  }
  .laneright {
    position: absolute;
    top: -5px;
    right: 5px;
    height:240px; 
  }
</style>

