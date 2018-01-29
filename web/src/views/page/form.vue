<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="200px">
      <el-form-item label="雷达ID">
        <el-input v-model="form.id"></el-input>
      </el-form-item>
      <el-form-item label="雷达高度">
        <el-input v-model="form.height"></el-input>
      </el-form-item>
      <el-form-item v-for="index in range" :key="index" :label="'车道'+(index+1)">
        <el-col :span="11">
          <el-input v-model.number="form.lane_min[index]"></el-input>
        </el-col>
        <el-col class="line" :span="2">- </el-col>
        <el-col :span="11">
          <el-input v-model.number="form.lane_max[index]"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="备注">
        <el-input type="textarea" v-model="form.desc"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="cancel">保存</el-button>
        <el-button @click="cancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      range: [0, 1, 2, 3, 4, 5],
      form: {
        id: 'hello wrold',
        height: 0,
        lane_min: [-1199, -800, -400, 0, 400, 800],
        lane_max: [-800, -400, 0, 400, 800, 1200],
        desc: ''
      },
      formCopy: null
    }
  },
  mounted() {
    this.formCopy = JSON.parse(JSON.stringify(this.form))
  },
  methods: {
    cancel() {
      console.log(this.form)
      this.form = JSON.parse(JSON.stringify(this.formCopy))
    }
  }
}
</script>
