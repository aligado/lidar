<template>
  <div class="app-container">
    <div>
      <el-button size="middle" type="success" @click="getList">刷新</el-button>
      <el-button size="middle" type="success" @click="getDadPath">上级目录</el-button>
      {{ path }}
    </div>

    <div class="table">
    <el-table :data="list" border fit highlight-current-row>
      <el-table-column :min-width="40" align="center" label='ID'>
        <template scope="scope">
          {{scope.$index}}
        </template>
      </el-table-column>
      <el-table-column :min-width="140" label="info">
        <template scope="scope">
          {{scope.row.file}}
          <el-tag>{{scope.row.type}}</el-tag>
          <el-tag v-if="scope.row.type=='logfloder'">{{scope.row.playready}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :min-width="100" label="operation" align="center">
        <template scope="scope">
          <el-button v-if="scope.row.type=='floder'" size="small" type="success" @click="openFloder(scope.row.file)">open
          </el-button>
          <el-button  size="small" type="success" @click="playLog(scope.row.file)">play
          </el-button>
          <el-button v-if="scope.row.type=='logfloder'" size="small" type="danger" @click="makeLog(scope.row.file)">init
          </el-button>
          <!--
          <el-button  size="small" type="danger" @click="makeLog(scope.row.floder)">delete
          </el-button>
          -->
        </template>
      </el-table-column>
    </el-table>
    </div>
  </div>
</template>

<script>
import { getLogTable, makeLog } from '@/api/logtable'

export default {
  data() {
    return {
      list: null,
      listLoading: false,
      path: '',
      pathview: []
    }
  },
  created() {
    // this.getList()
  },
  mounted() {
    setTimeout(()=>{
      this.getList()
    }, 200)
    // this.getList()
  },
  methods: {
    getList() {
      getLogTable(this.path).then(res => {
          this.list = res.data
          console.log(res)
        },
        error =>{
          console.log(error)
          //this.getList()
        })
    },
    playLog(floder) {
      floder = this.path + '/' + floder
      console.log(floder)
      this.$store.dispatch('SetLog', floder)
      this.$router.push({ name:'playLog'})
    },
    makeLog(floder) {
      floder = this.path + '/' + floder
      console.log(floder)
      makeLog(floder)
        .then((res)=> {
          console.log(res.data)
          this.getList()
        },
        error =>{
          console.log(error)
        })
    },
    updatePath() {
      this.path = ''
      for (let i=0; i<this.pathview.length; i++){
        this.path += '/'+this.pathview[i]
      }
    },
    getDadPath() {
      if (!this.pathview.length) return
      this.pathview.pop()
      this.updatePath()
      this.getList()
    },
    openFloder(floder) {
      this.pathview.push(floder)
      this.updatePath()
      this.getList()
    },
  }
}
</script>

<style>
.table {
  width: 800px;
}
</style>
