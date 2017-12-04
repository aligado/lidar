const common = {
  state: {
    playingLog: ''
  },

  mutations: {
    SET_LOG: (state, log) => {
      state.playingLog = log
    }
  },

  actions: {
    SetLog({ commit }, log) {
      // console.log('set', log)
      commit('SET_LOG', log)
    }
  }
}

export default common
