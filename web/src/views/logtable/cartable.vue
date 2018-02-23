<template>
  <div class="app-container">
    <div class="play-left">
      <div class="canvas-container">
          <canvas id="cv" class="cv" width="900" height="400">
              Your browser does not support the canvas element.
          </canvas>
          <div class="car-info">
            {{analysis}}
          </div>
          <div class="clear">
          </div>
      </div>
      <div class="play-control">
        <el-button-group>
          <el-button type="danger" class="" @click="poweron">power on</el-button>
          <el-button type="danger" class="" @click="shutdown">shut down</el-button>
          <el-button type="primary" class="" @click="play">play</el-button>
        </el-button-group>
      </div>
    </div>
    <div class="play-right">
      <div class="table">
      <el-table :data="carList" border fit highlight-current-row>
        <el-table-column :min-width="40" align="center" label='ID'>
          <template scope="scope">
            {{scope.$index}}
          </template>
        </el-table-column>
        <el-table-column :min-width="140" label="车型" align="center">
          <template scope="scope">
            {{scope.row.info}}
          </template>
        </el-table-column>
        <el-table-column :min-width="100" label="数量" align="center">
          <template scope="scope">
          </template>
        </el-table-column>
      </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { getCar, poweron, shutdown } from '@/api/logtable'

let cnt = 0
export default {
  data() {
    return {
      drawInterval: null,
      frame: null,
      analysis: 'null',
      typeList: [
        '小型客车',
        '大型客车',
        '小型货车',
        '中型货车',
        '大型货车',
        '特大货',
        '拖拉机',
        '摩托车'
      ],
      carList: [
      ],
      carQueue: []
    }
  },
  methods: {
    async play() {
      let res = await getCar()
      res = res.data
      console.log(res)
      for (let i=0; i<res.length; i++) {
        this.carQueue.push(res[i])
        console.log(res[i])
        this.carList.push({
          'info': res[i],
        })
      }
      if (this.carQueue.length > 0) {
        this.analysis = this.carQueue.shift()
        this.drawCar( this.analysis )
      }
    },
    poweron() {
      poweron()
        .then(res => {
          console.log(res)
        }, error => {
          console.log(error)
        })
    },
    shutdown() {
      shutdown()
        .then(res => {
          console.log(res)
        }, error => {
          console.log(error)
        })
    },
    drawCar(car) {
      var canvas = document.getElementById('cv');
      if (canvas.getContext) {
          var ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
          ctx.fillStyle = "red"
          let pointNum = car.info_list.length
          for (var j=0; j<pointNum; j++) {
            let tempX = 20+(j+1)*10 
            let tempY = 400-car.info_list[j]/2 
            ctx.fillRect(tempX, tempY, 2, 2);
          }
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
    for (let i=0; i<this.typeList.length; i++) {
      this.carList.push({
        'info': this.typeList[i],
        'num': 0
      })
    }
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
.car-info {
  float: left;
  width: 902px;
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
  width: 600px;
}
</style>

