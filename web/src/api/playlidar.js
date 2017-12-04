import fetch from '@/utils/fetch'

export function getLidar(oo) {
  return fetch({
    url: '/list',
    method: 'get',
    params: { oo }
  })
}
