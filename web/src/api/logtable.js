import fetch from '@/utils/fetch'

export function getLogTable(path) {
  return fetch({
    url: '/list',
    method: 'get',
    params: { path }
  })
}

export function makeLog(logfloder) {
  return fetch({
    url: '/make',
    method: 'get',
    params: { logfloder }
  })
}
