<template>
  <div class="app-container">
    <div>
      <el-button size="middle" type="success" @click="getRelease">刷新</el-button>
    </div>    
    <div class="play-left">
      <div class="table">
        <el-table :data="releaseList" border fit highlight-current-row>
          <el-table-column :min-width="20" align="center" label='ID'>
            <template scope="scope">
              {{scope.$index}}
            </template>
          </el-table-column>
          <el-table-column :min-width="100" label="文件" align="center">
            <template scope="scope">
              {{scope.row.file}}
            </template>
          </el-table-column>
          <el-table-column :min-width="60" label="操作" align="center">
            <template scope="scope">
              <el-button size="small" type="success" @click="getFile(scope.row.file)">查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <div class="play-right">
      <div class="table">
        <el-table :data="carList" border fit highlight-current-row>
          <el-table-column :min-width="20" align="center" label='ID'>
            <template scope="scope">
              {{scope.$index}}
            </template>
          </el-table-column>
          <el-table-column :min-width="100" label="信息" align="center">
            <template scope="scope">
              {{scope.row.info}}
            </template>
          </el-table-column>
          <el-table-column :min-width="60" label="操作" align="center">
            <template scope="scope">
              <el-button size="small" type="warning" @click="dialogCanvasVisible = true">查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <el-dialog title="info" :visible.sync="dialogCanvasVisible" width="100%" fullscreen=false>
      <!--
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
      -->
  </el-dialog>
  </div>
</template>

<script>
import { getFile, getRelease, getCar, poweron, shutdown } from '@/api/logtable'

let cnt = 0
export default {
  data() {
    return {
      dialogCanvasVisible: false,
      drawInterval: null,
      frame: null,
      analysis: 'null',
      releaseList: [
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
    getFile(file) {
      getFile(file)
        .then(res => {
          console.log(res)
          this.carList = []
          for (let index in res.data) {
            this.carList.push({'info': res.data[index]})
          }
        }, error => {
          console.log(error)
        })
    },
    getRelease() {
      getRelease()
        .then(res => {
          console.log(res)
          this.releaseList = []
          for (let index in res.data) {
            this.releaseList.push({'file': res.data[index]})
          }
        }, error => {
          console.log(error)
        })
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
    this.getRelease()
  }, 
  beforeDestroy() {
    clearInterval(this.drawInterval)
  }
}
</script>

<style>
.play-left {
  float:left;
  padding-right: 20px;
  width: 500px;
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

