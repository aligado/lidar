import fetch from '@/utils/fetch'

export function getLogTable(path) {
  return fetch({
    url: '/list',
    method: 'get',
    params: { path }
  })
}

export function getCar() {
  return fetch({
    url: '/car',
    method: 'get',
  })
}

export function loadPara() {
  return fetch({
    url: '/config',
    method: 'get',
  })
}

export function savePara(configData) {
  return fetch({
    url: '/config',
    method: 'post',
    data: {
      configData
    },
  })
}

export function shutdown() {
  return fetch({
    url: '/shutdown',
    method: 'get',
  })
}

export function poweron() {
  return fetch({
    url: '/poweron',
    method: 'get',
  })
}

export function makeLog(logfloder) {
  return fetch({
    url: '/make',
    method: 'get',
    params: { logfloder }
  })
}
