import fetch from '@/utils/fetch'

export function getLidar() {
  return fetch({
    url: '/frame',
    method: 'get',
  })
}
