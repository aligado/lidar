<template>
  <div class="app-container">
    <div class="play-left">
      <div class="canvas-container">
          <canvas id="cv0" class="cv" width="300" height="150">
              Your browser does not support the canvas element.
          </canvas>
          <canvas id="cv1" class="cv" width="300" height="150">
              Your browser does not support the canvas element.
          </canvas>
          <canvas id="cv2" class="cv" width="300" height="150">
              Your browser does not support the canvas element.
          </canvas>
          <div class="info">
            车道1
            {{analysis0}}
          </div>
          <div class="info">
            车道2
            {{analysis1}}
          </div>
          <div class="info">
            车道3
            cv2
            {{analysis2}}
          </div>
          <div class="clear">
          </div>
          <canvas id="cv3" class="cv" width="300" height="150">
              Your browser does not support the canvas element.
          </canvas>
          <canvas id="cv4" class="cv" width="300" height="150">
              Your browser does not support the canvas element.
          </canvas>
          <canvas id="cv5" class="cv" width="300" height="150">
              Your browser does not support the canvas element.
          </canvas>
          <div class="info">
            车道4
            {{analysis3}}
          </div>
          <div class="info">
            车道5
            {{analysis4}}
          </div>
          <div class="info">
            车道6
            {{analysis5}}
          </div>
          <div class="clear">
          </div>
          <canvas id="lidar" width="900" height="200">
              Your browser does not support the canvas element.
          </canvas>
          <div class="clear">
          </div>
      </div>
      <div class="play-control">
        <el-button-group>
          <el-button type="primary" class="" @click="start">播放</el-button>
          <el-button type="primary" class="" @click="play">单步</el-button>
          <!--
          <el-button type="primary" class="" @click="start">start</el-button>
          <el-button type="primary" class="" @click="play">play</el-button>
          <el-button type="primary" class="" @click="over">pause</el-button>
          -->
        </el-button-group>
      </div>
    </div>
    <div class="play-right">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="雷达ID">
          <el-input v-model="form.lidar_id"></el-input>
        </el-form-item>
        <el-form-item label="雷达高度">
          <el-input v-model="form.lidar_height"></el-input>
        </el-form-item>
        <el-form-item label="补偿角度">
          <el-input-number v-model="form.lidar_fix_angle" controls-position="right" :min="-60" :max="60"></el-input-number>
        </el-form-item>
        <el-form-item v-for="index in range" :key="index" :label="'车道'+(index+1)">
          <el-col :span="3">
            min:
          </el-col>
          <el-col :span="5">
            <el-input v-model.number="form.lane_min[index]"></el-input>
          </el-col>
          <el-col :span="3">
            max:
          </el-col>
          <el-col :span="5">
            <el-input v-model.number="form.lane_max[index]"></el-input>
          </el-col>
          <el-col :span="3">
            hor:
          </el-col>
          <el-col :span="5">
            <el-input v-model.number="form.lane_horizon[index]"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="savePara">保存</el-button>
          <el-button @click="loadPara">读取</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { getLidar } from '@/api/playlidar'
import { getCar, poweron, shutdown, loadPara, savePara } from '@/api/logtable'

let cnt = 0

const defaultPara = {
    "lidar_id": 1,
    "host": "192.168.0.1",
    "port": 2111,
    "bufsize": 2048, 
    "lidar_fix_angle": 0,
    "lane_num": 6, 
    "lane_min": [-1050, -800, -400, 0, 560, 800],
    "lane_max": [-800, -560, 0, 400, 800, 1200],
    "lane_horizon": [588, 600, 600, 600, 600, 600],
    "threshold_num": 5,
    "threshold_height": 12,
    "unuse_height": 6666,
    "car_threshold": 60,
    "lidar_height": 800,
    "lidar_hz": 25,
    "lidar_resolution": 0.5,
    "lidar_start_angle": 0,
    "lidar_end_angle": 0,
    "localpath": "/home/ubuntu/ServerLog",
    "ftppath": "/"
}

export default {
  data() {
    return {
      range: [0, 1, 2, 3, 4, 5],
      form: {
        lidar_id: 1,
        lidar_height: 0,
        lane_min: [-1199, -800, -400, 0, 400, 800],
        lane_max: [-800, -400, 0, 400, 800, 1200],
        lane_horizon: [-800, -400, 0, 400, 800, 1200],
        lidar_fix_angle: 0,
      },
      configData: defaultPara,
      formCopy: null,
      drawInterval: null,
      frame: null,
      height: [[], [], [], [], [], []],
      analysis: ['null', 'null', 'null', 'null', 'null', 'null'],
      analysis0: 'null',
      analysis1: 'null',
      analysis2: 'null',
      analysis3: 'null',
      analysis4: 'null',
      analysis5: 'null',
      oo: 1,
    }
  },
  methods: {
    savePara() {
      console.log(this.form)
      this.configData.lidar_id =  this.form.lidar_id
      this.configData.lidar_height = this.form.lidar_height
      this.configData.lidar_fix_angle =this.form.lidar_fix_angle
      this.configData.lane_min =this.form.lane_min
      this.configData.lane_max =this.form.lane_max
      this.configData.lane_horizon =this.form.lane_horizon
      savePara(this.configData)
        .then(res => {
          console.log(res.data)
        }, error => {
          console.log(error)
        })
    },
    loadPara() {
      loadPara()
        .then(res => {
          this.configData = res.data
          const data = res.data
          console.log(data)
          this.form.lidar_id = data.lidar_id 
          this.form.lidar_height = data.lidar_height
          this.form.lidar_fix_angle = data.lidar_fix_angle
          this.form.lane_min = data.lane_min 
          this.form.lane_max = data.lane_max
          this.form.lane_horizon = data.lane_horizon
          console.log(this.form)
        }, error => {
          console.log(error)
        })
    },
    play() {
      getLidar().then(res => {
          console.log(res.data)
          this.frame = res.data
          console.log('this.frame.analysis', this.frame.analysis)
          for (let i=0; i<6; i++) {
            if (res.data.analysis[i].hasOwnProperty('info_list')) {
              if (i==0) this.analysis0 = JSON.stringify(this.frame.analysis[i])
              if (i==1) this.analysis1 = JSON.stringify(this.frame.analysis[i])
              if (i==2) this.analysis2 = JSON.stringify(this.frame.analysis[i])
              if (i==3) this.analysis3 = JSON.stringify(this.frame.analysis[i])
              if (i==4) this.analysis4 = JSON.stringify(this.frame.analysis[i])
              if (i==5) this.analysis5 = JSON.stringify(this.frame.analysis[i])
            }
          }
          console.log('analysis', this.analysis)
          this.draw()
        },
        error =>{
          console.log(error)
        })
    },
    drawRule(ctx) {
      ctx.beginPath()
      const step = parseInt(ctx.canvas.width/32)
      // console.log(step)
      for (let i =0; i<ctx.canvas.width; i+=step) {
        ctx.moveTo(i, ctx.canvas.height);
        ctx.lineTo(i, ctx.canvas.height - 10);

        ctx.font = "Bold 12px Arial"; 
        ctx.textAlign = "center";
        ctx.fillStyle = "#CC0000"; 
        ctx.fillText((i/step-16), i,ctx.canvas.height - 10 ); 
        ctx.lineWidth = 2;
      }
      ctx.closePath();
      ctx.strokeStyle = "#CC0000"; // 设置线的颜色
      ctx.lineWidth = 2;
      ctx.stroke(); // 进行线的着色，这时整条线才变得可见
    },
    drawLane() {
      let height = this.frame.height
      for (let i=0; i<6; i++) {
        var canvas = document.getElementById('cv'+i);
        this.height[i].push(this.frame.height[i])
        if (this.height[i].length>100) {
          this.height[i].shift()
        }
        if (canvas.getContext) {
            var ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
            ctx.fillStyle = "red"
            for (var j=0; j<this.height[i].length; j++) {
              let tempX = (j+1)*3 
              let tempY = this.height[i][j]/5
              ctx.fillRect(tempX, tempY, 1, 1);
            }
        }
      }
    },
    draw() {
      var canvas = document.getElementById('lidar');
      if (canvas.getContext) {
          // console.log('draw')
          var ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
          ctx.fillStyle = "red"
          let lx = this.frame.x
          let ly = this.frame.y
          this.drawRule(ctx)
          this.drawLane()
          for (var i=0; i<lx.length; i++) {
            let tempX = (lx[i]+1600)*9/32
            let tempY = ly[i]/4
            ctx.fillRect(tempX, tempY, 1, 1);
          }
          cnt += 1
      }
    },
    fort() {
      var canvas = document.getElementById('cv0');
      if (canvas.getContext) {
          var ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, 100, 100)
          ctx.fillStyle = "red"
          for (var i=0; i<100-cnt; i++) {
              ctx.fillRect(i, i, 1, 1);
          }
          /*
          ctx.beginPath();
          ctx.moveTo(0,0);
          ctx.lineTo(99,0);
          ctx.lineTo(99,99);
          ctx.lineTo(0,99);
          ctx.fill();
          */
          cnt += 1
      }
    },
    start() {
      clearInterval(this.drawInterval)
      this.drawInterval = setInterval(() => {
        this.play()
        }, 50)
    }, 
    over() {
      clearInterval(this.drawInterval)
    }
  },
  mounted() {
    /*
    this.drawInterval = setInterval(() => {
      this.play()
      }, 30)
    */
  }, 
  beforeDestroy() {
    clearInterval(this.drawInterval)
  }
}
</script>

<style>
.play-left {
  float:left;
  width: 915px;
}

.canvas-container {
  width: 910px
}
.cv {
  float: left;
  border: 1px solid #c3c3c3;
}
.info {
  float: left;
  width: 302px;
  border: 1px solid #c3c3c3;
  word-wrap: break-word;
}
.clear {
  height: 5px;
  width: 1280px;
  overflow: auto;
}
#lidar {
  float: left;
  border: 1px solid #c3c3c3;
  margin-bottom: 10px
}
.play-control {
  padding-top: 40px
}
.play-right {
  float: left;
  width: 400px
}
</style>

