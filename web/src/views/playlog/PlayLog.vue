<template>
  <div class="app-container">
    <div class="play-left">
      <canvas id="myCanvas" width="1280" height="720" style="border:1px solid #c3c3c3;">
          Your browser does not support the canvas element.
      </canvas>
      <div class="block">
        <el-slider @change="onSlider" v-model="playState.slider" :min="playState.sliderMin" :max="playState.sliderMax"></el-slider>
      </div>
      <div class="log-panel">
        <div class="log-panel-left">
          <h1>play log</h1>
        </div>
        <div class="log-panel-middle">
          <screen :lane-warning="screen.laneWarning"></screen>
        </div>
        <div class="log-panel-right">
          <div class="play-control">
            <el-button-group>
              <el-button type="primary" @click="onPrevious" class=""><<</el-button>
              <el-button type="primary" @click="onBackward" class=""><</el-button>
              <el-button type="primary" @click="onPlay" class="">{{playState.icon}}</el-button>
              <el-button type="primary" @click="onForward" class="">></el-button>
              <el-button type="primary" @click="onNext" class="">>></el-button>
              <el-button type="primary" >跳帧{{playState.step}}</el-button>
              <el-button type="primary" >当前帧{{num}}</el-button>
              <el-button type="primary" @click="setInterval" class="">间隔</el-button>
              <el-input style="width: 60px;" placeholder="interval" v-model="playState.interval"></el-input>
            </el-button-group>
            <!--
            <el-button style="margin-left: 10px;"type="primary"  >jump</el-button>
            <el-input style="width: 80px;" placeholder="step" v-model="playState.jump"> </el-input>
            -->
          </div>
        </div>
      </div>
    </div>
    <div class="play-right">
      <pre> {{oneLogInfo}} </pre>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Screen from "./Screen"
import { play } from '@/api/playlog'
import { staticUrl } from '@/api/static'
// import logdata from "@/logdata/rec_20170618_083023.json"
// import logdata1 from "@/logdata/rec_20170618_081520.json"
let logdata = []
const url = staticUrl 
export default {
  components: { Screen },
  data() {
    return {
      cxt: {},
      img: {},
      num: 0,
      len: 1,
      oneLogInfo: {'a':123},
      drawing: 0, 
      drawInterval: {},
      playState: {
        icon: "〓",
        slider: 0,
        sliderMax: 1,
        sliderMin: 0,
        step: 1,
        jump: 0,
        interval: 50,
      },
      screen: {
        laneWarning: 0
      }
    };
  },
  computed: {
    ...mapGetters([
      'playingLog',
    ])
  },
  methods: {
    init() {
    },
    onPlay() {
      if (this.playState.icon == "▶") {
        this.playState.icon = "〓"
      } else {
        this.playState.icon = "▶"
      }
    },
    onBackward() {
      this.playState.step -= 1
    },
    onForward() {
      this.playState.step += 1
    },
    onPrevious() {
      if (this.playState.icon == "〓" && !this.drawing){
        this.num -= this.playState.step 
        this.draw()
      }
    },
    onNext() {
      if (this.playState.icon == "〓" && !this.drawing){
        this.num += this.playState.step 
        this.draw()
      }
    },
    onSlider() {
      console.log("slider")
      if (this.playState.icon == "〓" && !this.drawing){
        this.num = this.playState.slider
        this.draw()
      } else {
        this.playState.slider = this.num
      }
    },
    setInterval() {
      clearInterval(this.drawInterval)
      this.drawInterval = setInterval(() => {
        this.play()
        }, this.playState.interval)
    },
    onSubmit() {
      this.$message("submit!");
    },
    draw() {
      let that = this
      this.drawing = 1
      this.playState.slider = this.num
      console.log(this.num);
      console.log(logdata[this.num]);
      function drawRect(rect) {
            let y = parseInt(rect[0])
            let x = parseInt(rect[1])
            let h = parseInt(rect[2])
            let w = parseInt(rect[3])
            let x1 = x+w-1
            let y1 = y+h-1 
            console.log(y, x, h, w)
            that.cxt.moveTo(y, x); // 设置路径起点，坐标为(20,20)
            that.cxt.lineTo(y, x1);
            that.cxt.moveTo(y, x1); // 设置路径起点，坐标为(20,20)
            that.cxt.lineTo(y1, x1);
            that.cxt.moveTo(y1, x1); // 设置路径起点，坐标为(20,20)
            that.cxt.lineTo(y1, x);
            that.cxt.moveTo(y1, x); // 设置路径起点，坐标为(20,20)
            that.cxt.lineTo(y, x);
      }
      function drawLine(line) {
        var a0 = parseFloat(line[0])
        var a1 = parseFloat(line[1])
        var a2 = parseFloat(line[2])
        var a3 = parseFloat(line[3])
        for (let x=520; x<710; x += 20) {
            let y = a0 + a1*x + a2*x*x + a3*x*x*x;
            let x1 = x + 20
            let y1 = parseInt(a0 + a1*x1 + a2*x1*x1 + a3*x1*x1*x1)
            that.cxt.moveTo(y, x); // 设置路径起点，坐标为(20,20)
            that.cxt.lineTo(y1, x1);
        }
      }
      this.oneLogInfo = logdata[this.num]
      if ('lane_warning' in this.oneLogInfo) {
        let tempState = this.oneLogInfo.lane_warning
        this.screen.laneWarning = parseInt(tempState)
      }
      this.img.src = url + logdata[this.num]["img"];
      this.img.onload = () => {
        this.cxt.clearRect(0, 0, this.cxt.canvas.width, this.cxt.canvas.height);
        this.cxt.drawImage(this.img, 0, 0);
        this.cxt.beginPath();
        for (let i=0; i<4; i++) {
          let key = 'lane_line'+i
          if (key in logdata[this.num]) {
            drawLine(logdata[this.num][key].split(','))
          }
            //key = 'lane_line%s' % i
        }
        if ("rect" in logdata[this.num]) {
          console.log("rect")
          drawRect(logdata[this.num]["rect"].split(','))
        }
        if ("b_rect" in logdata[this.num]) {
          console.log("b_rect")
          drawRect(logdata[this.num]["b_rect"].split(','))
        }
        this.cxt.closePath();
        this.cxt.strokeStyle = "#CC0000"; // 设置线的颜色
        this.cxt.lineWidth = 2;
        this.cxt.stroke(); // 进行线的着色，这时整条线才变得可见
        this.drawing = 0
      };
    },
    play() {
      if (this.drawing || this.playState.step == 0 || this.playState.icon == "〓") {
        return
      }
      this.num += this.playState.step
      if (this.num<0 || this.num>=this.len) {
        this.num = 0;
        this.playState.icon = "〓"
      }
      this.draw()
    }
  },
  mounted() {
    console.log('this.log', this.playingLog)
    if (!this.playingLog) {
      return
    }
    play(this.playingLog) 
    // oneAxios.get('/play/1234') 
      .then( (res) => {
        console.log(res)
        logdata = JSON.parse(res.data)
        console.log(logdata[0])
        this.img = new Image();
        let c = document.getElementById("myCanvas");
        this.cxt = c.getContext("2d");
        this.len = logdata.length
        this.playState.sliderMin = 0
        this.playState.sliderMax = this.len-1
        this.drawInterval = setInterval(() => {
          this.playy()
          }, this.playState.interval)
      })
  }, 
  beforeDestroy() {
    clearInterval(this.drawInterval)
  }
};
</script>

<style>
.play-left {
  float:left;
  width: 1282px;
}

.log-panel {
  width: 1282px;
}

.log-panel-left {
  float: left;
  width: 525px;
  background-color: royalblue;
}
.log-panel-middle {
  float: left;
  width: 232px;
}
.log-panel-right {
  float: left;
  width: 525px;
  background-color: chartreuse;
}
.play-right {
  width: 600px;
}
</style>

