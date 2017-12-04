const getters = {
  sidebar: state => state.app.sidebar,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  playingLog: state => state.common.playingLog,
  roles: state => state.user.roles
}
export default getters
